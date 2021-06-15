###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import os
import json
import time
import numpy
import uuid
import mimetypes

import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.http import MediaFileUpload

from starthinker.util.sheets import sheets_read
from starthinker.util.bigquery import query_to_rows
from starthinker.util.storage import object_put
from starthinker.util.google_api import API_YouTube

from starthinker.config import BUFFER_SCALE
CHUNKSIZE = int(10 * 1024000 * BUFFER_SCALE)  # scale is controlled in config.py


def hex_to_rgb(value, alpha=None):
  # if string assume hex format ( supports both #ffffff and #fff notation )
  if isinstance(value, str):
    value = value.lstrip('#')
    hlen = len(value)
    rgba = [
        int(value[i:i + int(hlen / 3)], 16)
        for i in range(0, hlen, int(hlen / 3))
    ]
    if alpha:
      rgba.append(int(alpha * 255))
  # probably already a tuple just pass the value
  else:
    rgba = value
  return tuple(rgba)


def get_text_image(effect):

  # get a font ( from standard library )
  fnt = ImageFont.truetype('%s.ttf' % effect['text']['font'],
                           effect['text']['size'])

  # determine size of text
  img = Image.new('RGBA', (1, 1))
  draw = ImageDraw.Draw(img)
  size = draw.multiline_textsize(
      effect['text']['message'],
      font=fnt,
      spacing=int(effect['text']['size'] / 2))

  # make a blank image for the text and draw the text
  #print('S', size)
  txt = Image.new('RGBA', size, (255, 255, 255, 0))
  d = ImageDraw.Draw(txt)
  #print('S', effect['text']['color'])
  d.text((0, 0),
         effect['text']['message'],
         font=fnt,
         fill=hex_to_rgb(effect['text']['color'], effect.get('opacity')),
         align=effect['text']['align'])

  return numpy.array(txt)


def get_effects(video, effect):

  if 'image' in effect:
    clip = (mp.ImageClip(effect['image']['file_or_url']))

    clip = clip.set_start(effect['duration']['start'])
    clip = clip.set_duration(effect['duration']['end'] -
                             effect['duration']['start'])
    clip = clip.set_pos(
        (effect['position']['width'], effect['position']['height']))

    if effect.get('fade', {}).get('in'):
      clip = clip.crossfadein(effect['fade']['in'])

    if effect.get('fade', {}).get('out'):
      clip = clip.crossfadeout(effect['fade']['out'])

    if effect.get('position', {}).get('rotate'):
      clip = clip.rotate(effect['position']['rotate'])

    yield clip

  if 'text' in effect:

    # Requires working installation of ImageMagick
    try:
      clip = mp.TextClip(
          txt=effect['text']['message'],
          color=effect['text'].get('color', '#666666'),
          font=effect['text'].get('font', 'Courier'),
          fontsize=effect['text'].get('size', 12),
          align=effect['text'].get('align', 'center'),
          kerning=effect['text'].get('kerning', 0))

    # Alternate method using Pillow - no need to set position text is already positioned within image
    except:
      clip = (mp.ImageClip(get_text_image(effect)))

    clip = clip.set_start(effect['duration']['start'])
    clip = clip.set_duration(effect['duration']['end'] -
                             effect['duration']['start'])
    clip = clip.set_pos(
        (effect['position']['width'], effect['position']['height']))

    if effect.get('fade', {}).get('in'):
      clip = clip.crossfadein(effect['fade']['in'])

    if effect.get('fade', {}).get('out'):
      clip = clip.crossfadeout(effect['fade']['out'])

    if effect.get('position', {}).get('rotate'):
      clip = clip.rotate(effect['position']['rotate'])

    yield clip

  elif 'audio' in effect:
    clip = (mp.AudioClip(effect['audio']['file_or_url']))

    clip = clip.set_start(effect['duration']['start'])
    clip = clip.set_duration(effect['duration']['end'] -
                             effect['duration']['start'])

    yield clip


def edit_video(video):
  clips = [mp.VideoFileClip(video['file_or_url'])]

  for effect in video['effects']:
    clips.extend(get_effects(clips[0], effect))

  video = mp.CompositeVideoClip(clips)

  return video


def save_video(config, task, out, clip):
  # write to user defined local file
  if out.get('file'):
    clip.write_videofile(
        out['file'], codec='libx264', audio_codec='aac',
        logger=None)  # logger needed or fmmpeg writes to stderr

  # for storage, write to temporary file ( no alternative with moviepy ), then upload
  if out.get('storage', {}).get('file'):
    temporary_file_name = '/tmp/%s_%s' % (uuid.uuid1(), out['storage']['file'])
    clip.write_videofile(
        temporary_file_name, codec='libx264', audio_codec='aac',
        logger=None)  # logger needed or fmmpeg writes to stderr
    with open(temporary_file_name, 'rb') as temporary_file:
      object_put(
          config, task['auth'],
          '%s:%s' % (out['storage']['bucket'], out['storage']['file']),
          temporary_file,
          mimetype=mimetypes.guess_type(out['storage']['file'],
                                        strict=False)[0])
    os.remove(temporary_file_name)

  if out.get('dcm'):
    print('DCM not implemented yet.')

  # for youtube, write to temporary file ( no alternative with moviepy ), then upload
  if out.get('youtube', {}).get('title'):
    temporary_file_name = '/tmp/%s_%s' % (uuid.uuid1(), out['storage']['file'])
    clip.write_videofile(
        temporary_file_name, codec='libx264', audio_codec='aac',
        logger=None)  # logger needed or fmmpeg writes to stderr

    body = {
        'snippet': {
            'title': out['youtube']['title'],
            'description': out['youtube']['description'],
            'tags': out['youtube']['tags'],
            'categoryId': out['youtube']['category']
        },
        'status': {
            'privacyStatus': out['youtube']['privacy']
        }
    }
    try:
      API_YouTube(config, task['auth']).videos().insert(
          part=','.join(body.keys()),
          body=body,
          media_body=MediaFileUpload(
              temporary_file_name, chunksize=CHUNKSIZE,
              resumable=True)).upload()
    finally:
      os.remove(temporary_file_name)


def rows_to_videos(rows):
  videos = {}
  for row in rows:
    videos.setdefault(
        row[0], {
            'file_or_url': row[0],
            'effects': [],
            'out': {
                'youtube': {
                    'title': row[17],
                    'description': row[18],
                    'category': int(row[19]) if row[19] else None,
                    'tags': row[20].split(',') if row[20] else None,
                    'privacy': row[21].lower() if row[21] else None,
                },
                'dcm': row[22],
                'storage': {
                    'bucket': row[23],
                    'file': row[24],
                }
            }
        })['effects'].append({
            'duration': {
                'start': float(row[1]),
                'end': float(row[2])
            },
            'fade': {
                'in': float(row[3]),
                'out': float(row[4])
            },
            'opacity': float(row[5]),
            'position': {
                'height': int(row[6]),
                'width': int(row[7]),
                'angle': int(row[8])
            },
            'image': {
                'file_or_url': row[9]
            },
            'text': {
                'color': row[10],
                'font': row[11],
                'size': int(row[12]),
                'align': row[13],
                'kerning': int(row[14]),
                'message': row[15]
            }
        })
  return videos.values()


def videos_from_sheets(config, task):
  rows = sheets_read(config, task['auth'], task['sheets']['sheet'], task['sheets']['tab'],
                     'A3:Y')
  return rows_to_videos(rows)


def videos_from_bigquery(config, task):
  rows = query_to_rows(config, task['auth'],
                       task['bigquery'].get('project', config.project), task['bigquery']['dataset'],
                       'SELECT * FROM %s;' % task['bigquery']['table'])
  return rows_to_videos(rows)


def video(config, task):
  if config.verbose:
    print('Video')

  videos = []

  if task.get('sheets', {}).get('tab'):
    videos.extend(videos_from_sheets(config, task))

  if task.get('bigquery', {}).get('table'):
    videos.extend(videos_from_bigquery(config, task))

  if task.get('file_or_url'):
    videos.append(task)

  for video in videos:
    clip = edit_video(video)
    save_video(config, task, video['out'], clip)
