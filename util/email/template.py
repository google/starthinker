###########################################################################
#
#  Copyright 2017 Google Inc.
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

from itertools import cycle

class EmailTemplate:

  def __init__(self):
    self.text_align = 'center'
    self.content_html = ''
    self.content_text = ''
    self.segments = [
      { 'foreground':'#222', 'background':'#fafafa' },
      { 'foreground':'#222', 'background':'#f6f6f6' },
      { 'foreground':'#222', 'background':'#f2f2f2' },
    ]
    self.segment = 0

  # only do the look, as this can be applied to various elements with different layouts
  def _header_css(self):
    return 'color:%(foreground)s;font-family:Verdana;font-size:24px;line-height:36px;border:0px;' % self.segment_next(False)


  # only do the look, as this can be applied to various elements with different layouts
  def _text_css(self):
    return 'color:#222;font-family:Verdana;font-size:16px;line-height:24px;'


  # only do the look, as this can be applied to various elements with different layouts ( also used for table headers )
  def _button_css(self, big=False):
    if big:
      return 'display:inline-block;margin:0px auto;border-radius:100px;padding:12px 36px;background-color:%(foreground)s;color:%(background)s;font-family:Verdana;font-size:24px;text-decoration:none;text-align:center;' % self.segment_next(False)
    else:
      return 'display:inline-block;margin:0px auto;border-radius:50px;padding:6px 18px;background-color:%(foreground)s;color:%(background)s;font-family:Verdana;font-size:16px;text-decoration:none;text-align:center;' % self.segment_next(False)


  def _table_css(self):
    return 'color:#222;font-family:Verdana;font-size:12px;line-height:16px;'


  # define colors for each section and cycle them for each section
  def segments_clear(self):
    self.segments = []
    self.segment = 0


  def segments_add(self, foreground_color, background_color):
    self.segments.append({'foreground':foreground_color, 'background':background_color})
    self.segment = 0


  def segment_next(self, advance=True):
    value = self.segments[self.segment % len(self.segments)]
    if advance: 

      # HTML
      if self.segment > 0: self.content_html += '</div>'
      self.content_html += '<div style="background-color:%(background)s;padding:40px 20px;">' % value

      # Text
      self.content_text += '----------------------------------------------------------------'

      self.segment += 1

    return value

  def align(self, text_align):
    self.text_align = text_align

  def greeting(self, name='', salutation='Hi'):
    if name:
      # HTML
      self.content_html += '<p style="width:100%%;margin:0px;padding:0px;border:0px;%s">%s %s,<p>' % (self._text_css(), salutation, name)

      # Text
      self.content_text += '%s %s,\n\n' % (salutation, name)

    else:
      # HTML
      self.content_html += '<p style="width:100%%;margin:0px;padding:0px;border:0px;%s">%s,<p>' % (self._text_css(), salutation)

      # Text
      self.content_text += '%s,\n\n' % salutation


  def header(self, text):
    # HTML
    self.content_html += '<p style="width:100%%;margin:0px 0px 40px 0px;padding:0px;border:0px;text-align:%s;font-weight:bold;%s">%s</p>' % (self.text_align, self._header_css(), text)

    # Text
    self.content_text += '--------------------------------------------------\n\n%s\n\n' % text


  def paragraph(self, text, bold=False):
    # HTML
    self.content_html += '<p style="width:100%%;margin:40px 0px;padding:0px;border:0px;text-align:%s;font-weight:%s;%s">%s<p>' % (self.text_align, 'bold' if bold else 'normal', self._text_css(), text.replace('\n', '<br/><br/>'))

    # Text
    self.content_text += '%s\n\n' % text

    
  def image(self, url, link):
    # HTML
    if link: self.content_html += '<a href="%s">' % link
    self.content_html += '<img src="%s" style="width:100%%;height:auto;margin:10px 0px;padding:0px;border:0px"/>' % url
    if link: self.content_html += '</a>'

    # Text
    self.content_text += 'IMAGE: %s\n' % url
    if link: self.content_text += 'LINK: %s\n\n' % url


  def button(self, text, link, big=False):
    # HTML

    self.content_html += '<p style="width:100%%;margin:40px 0px;padding:0px;border:0px;text-align:%s"><a href="%s" style="%s">%s</a></p>' % (self.text_align, link, self._button_css(big), text)

    # Text
    self.content_text += '%s: %s' % (text, link)


  def section(self, header, paragraph, image, link, button):
    # HTML
    self.content_html += '<table style="width:100%;margin:40px 0px;padding:0px;border:0px">'
    self.content_html += '<tr>'
    if image:
      self.content_html += '<td style="width:45%;padding:10px;text-align:center;vertical-align:top;">'
      if link: self.content_html += '<a href="%s">' % link
      self.content_html += '<img src="%s" style="width:100%%;height:auto;margin:0px;padding:0px;border:0px"/>' % image
      if link: self.content_html += '</a>'
      self.content_html += '</td>'

    self.content_html += '<td style="padding:10px;text-align:left;vertical-align:top;">'

    if header: 
      self.content_html += '<p style="width:100%%;margin:0px;padding:0px;border:0px;font-weight:bold;%s">%s<p>' % (self._header_css(), header)
    if paragraph: 
      self.content_html += '<p style="width:100%%;margin:0px;padding:0px;border:0px;%s">%s<p>' % (self._text_css(), paragraph)
    if link: 
      self.content_html += '<a href="%s" style="%s">%s</a>' % (link, self._button_css(), button)
    self.content_html += '</td>'
    self.content_html += '</tr>'
    self.content_html += '</table>' 

    # Text
    if header: self.content_text += '--------------------------------------------------\n\n%s\n\n' % header
    if image: self.content_text += 'IMAGE: %s\n\n' % image
    self.content_text += '%s\n\n' % paragraph
    if link: self.content_text += '%s: %s\n\n' % (button, link)


  def list(self, elements):
    # HTML
    self.content_html += '<table style="width:100%;margin:40px 0px;padding:0px;border:0px;border-collapse:collapse;">'
    for element in elements:
      self.content_html += '<tr><td style="padding:10px;text-align:left;border-bottom:1px solid #ccc;%s">%s</td></tr>' % (self._table_css(), element)
    self.content_html += '</table>' 

    # Text
    self.content_text == '\n\n'
    for element in elements:
      self.content_text += '  - %s\n' % element
    self.content_text == '\n'


  def table(self, schema, rows):
    aligns = {'BOOLEAN':'center', 'INTEGER':'right', 'FLOAT':'right', 'STRING':'left', 'URL':'center'}

    # HTML
    self.content_html += '<table style="width:100%;margin:40px 0px;padding:0px;border:0px;border-collapse:collapse;">'
    self.content_html += '<tr>'

    # headers
    for header in schema:
      self.content_html += '<td style="padding:10px;text-align:%s;border-bottom:1px solid #ccc;font-weight:bold;%s">%s</td>' % (aligns.get(header['type'], 'left'), self._table_css(), header['name'])
    self.content_html += '</tr>'

    # rows
    for row in rows:
      self.content_html += '<tr>'
      for column, header in enumerate(schema):
        value = row[column]
        # change links into clickable buttons ( do we want to make up our own schema here? for images too? )
        if isinstance(value, basestring) and value.startswith('http'):
          value = '<a href="%s" style="border-radius:50px;padding:1px 12px;%s">&rarr;</a>' % (value, self._button_css())
        self.content_html += '<td style="padding:10px;text-align:%s;border-bottom:1px solid #ccc;%s">%s</td>' % (aligns.get(header['type'], 'left'), self._table_css(), value)
      self.content_html += '</tr>'

    self.content_html += '</table>' 

    # Text
    for row in rows:
      self.content_text += '--------------------------------------------------\n'
      for column, header in enumerate(schema):
        self.content_text += '%s: %s\n' % (header['name'], row[column])
      self.content_text += '\n'


  def get_html(self):
    return '<table style="width:100%%;max-width:600px;margin:0px auto;text-align:left;background-color:fff;"><tr><td>%s%s</td></tr></table>' % (self.content_html, '</div>' if self.segment > 0 else '')


  def get_text(self):
    return self.content_text 


if __name__ == "__main__":

  t = EmailTemplate();
  t.header('This Is A Header')
  t.paragraph('A paragraph is a few sentences of text.  Although you can use HTML, it will break the text version.')
  t.section( 
    'Section Header',
    'A section paragraph is a few sentences of text.',
    'http://www.image.com/image.jpg',
    'http://www.google.com',
    'A Button'
  )
  t.table(
    [
      { "name":"Column A", "type":"STRING" },
      { "name":"Column B", "type":"INTEGER" },
      { "name":"Column C", "type":"BOOLEAN" },
      { "name":"Column D", "type":"FLOAT" },
      { "name":"Column E", "type":"URL" },
    ],
    [
      [ 'First', 1, True, 1.1, 'http://www.google.com' ],
      [ 'Second', 2, False, 2.2, 'http://www.google.com' ],
      [ 'Third', 3, True, 3.3, 'http://www.google.com' ],
    ]
  )
  print t.get_html()
  print t.get_text()
