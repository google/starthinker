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

import re
from datetime import datetime

MARKUP_TO_HTML = re.compile(r'\[(.*?)\]\((.*?)\)', flags=re.IGNORECASE)
MARKUP_TO_TEXT = re.compile(r'\[(.*?)\]\((.*?)\)', flags=re.IGNORECASE)


class EmailTemplate:

  def __init__(self, template={}):
    self.content_html = ''
    self.content_text = ''

    self.style = {
        'background':
            template.get('style', {}).get('background', '#f2f2f2'),
        'foreground':
            template.get('style', {}).get('foreground', '#ffffff'),
        'text':
            template.get('style', {}).get('text', '#414347'),
        'link':
            template.get('style', {}).get('link', '#4285f4'),
        'font':
            template.get('style',
                         {}).get('font',
                                 'Roboto, Helvetica, Arial sans-serif;'),
        'align':
            template.get('style', {}).get('align', 'left'),
    }

    self.subject = template.get('subject', '')
    self.logo = template.get('logo', '')
    self.footer = template.get('footer', [])
    self.copyright = template.get('copyright',
                                  'Copyright &copy; %d' % datetime.today().year)

    if template:
      self.template(template)

  def template(self, template):

    if 'body' in template:
      self.template(template['body'])
    if 'greeting' in template:
      self.greeting(**template['greeting'])
    if 'header' in template:
      self.header(template['header'])
    if 'image' in template:
      self.image(**template['image'])
    if 'paragraph' in template:
      self.paragraph(template['paragraph'])
    if 'button' in template:
      self.button(**template['button'])
    if 'table' in template:
      self.table(**template['table'])
    if 'list' in template:
      self.list(template['list'])
    if 'sections' in template:
      for s in template['sections']:
        self.section(True, background=s.get('background', None))
        self.template(s)
        self.section()
    if 'grid' in template:
      self.grid(True)
      for r in template['grid']:
        self.row(True)
        for c in r:
          self.column(len(r))
          self.template(c)
          self.column()
        self.row()
      self.grid()

  def _header_css(self):
    return ('width:100%%;margin:10px 0px 20px '
            '0px;padding:0px;border:0px;text-align:%(align)s;color:%(text)s;font-family:%(font)s;font-size:22px;line-height:30px;font-weight:500;letter-spacing:-0.31px;border:0px;') % self.style

  def _text_css(self):
    return ('width:100%%;margin:10px '
            '0px;padding:0px;border:0px;font-weight:normal;text-align:%(align)s;color:%(text)s;font-family:%(font)s;font-size:15px;line-height:26px;') % self.style

  def _link_css(self):
    return 'color:%(link)s;text-decoration:none;' % self.style

  def _button_css(self):
    return ('display:inline-block;margin:10px '
            'auto;border-radius:3px;-webkit-border-radius:3px;-moz-border-radius:3px;padding:11px'
            ' '
            '19px;background-color:%(link)s;color:%(background)s;font-family:%(font)s;font-size:16px;font-weight:bold;letter-spacing:-0.31px;text-decoration:none;text-align:center;') % self.style

  def _table_css(self):
    return 'color:%(text)s;font-family:%(font)s;font-size:12px;line-height:16px;' % self.style

  def markup_to_html(self, markup):
    return MARKUP_TO_HTML.sub(
        r'<a href="\2" style="%s">\1</a>' % self._link_css(),
        markup).replace('\n', '<br/><br/>')

  def markup_to_text(self, markup):
    return MARKUP_TO_TEXT.sub(r'\1 (\2)', markup).replace('\n', '<br/><br/>')

  def section(self, on=False, background=None):
    value = {
        'image':
            'background-image:url(\'%s\');background-repeat:no-repeat;background-size:contain;'
            % background if background else '',
        'align':
            self.style['align']
    }

    # HTML
    if on:
      self.content_html += ('<div style="margin:0px '
                            '15px;padding:1px;text-align:%(align)s;%(image)s">') % value
    else:
      self.content_html += '</div>'
      self.content_text += '\n'

  def align(self, text_align):
    self.style['align'] = text_align

  def greeting(self, name='', salutation='Hi'):
    if name:
      # HTML
      self.content_html += '<p style="%s">%s %s,<p>' % (self._text_css(),
                                                        salutation, name)

      # Text
      self.content_text += '%s %s,\n\n' % (salutation, name)

    else:
      # HTML
      self.content_html += '<p style="%s">%s,<p>' % (self._text_css(),
                                                     salutation)

      # Text
      self.content_text += '%s,\n\n' % salutation

  def header(self, text):
    # HTML
    self.content_html += '<p style="%s">%s</p>' % (self._header_css(),
                                                   self.markup_to_html(text))

    # Text
    self.content_text += '\n--------------------------------------------------\n\n%s\n\n' % self.markup_to_text(
        text)

  def paragraph(self, text):

    # HTML
    self.content_html += '<p style="%s">%s<p>' % (
        self._text_css(), self.markup_to_html(text)
        #MARKUP_TO_HTML.sub(r'<a href="\2" style="%s">\1</a>' % self._link_css(), text).replace('\n', '<br/><br/>')
    )

    # Text
    #self.content_text += '%s\n\n' % MARKUP_TO_TEXT.sub(r'\1 (\2)', text).replace('\n', '<br/><br/>')
    self.content_text += '%s\n\n' % self.markup_to_text(text)

  def image(self, src, link=None):
    # HTML
    if link:
      self.content_html += '<a href="%s">' % link
    self.content_html += ('<img src="%s" '
                          'style="max-width:100%%;width:auto;height:auto;margin:10px'
                          ' auto;padding:0px;border:0px;"/>') % src
    if link:
      self.content_html += '</a>'

    # Text
    self.content_text += 'IMAGE: %s\n' % src
    if link:
      self.content_text += 'LINK: %s\n\n' % link

  def button(self, text, link, big=False):
    # HTML
    self.content_html += ('<p style="width:100%%;margin:0px '
                          '0px;padding:0px;border:0px;"><a href="%s" '
                          'style="%s">%s</a></p>') % (
        link, self._button_css(), text)

    # Text
    self.content_text += '%s: %s' % (text, link)

  def grid(self, on=False):
    if on:
      self.content_html += ('<table style="width:100%;margin:20px '
                            '0px;padding:0px;border:0px;border-spacing:0px '
                            '20px;">')
    else:
      self.content_html += '</table>'

  def row(self, on=False):
    if on:
      self.content_html += '<tr>'
    else:
      self.content_html += '</tr>'

  def column(self, number=0):
    if number:
      width = int(100 / number)
      self.content_html += ('<td '
                            'style="width:%d%%;padding:10px;text-align:center;vertical-align:top;">') % width
    else:
      self.content_html += '</td>'

  def display(self, header, paragraph, image, link, button):
    # HTML
    self.grid(True)
    self.row(True)

    if image:
      self.column(True)
      self.image(image, link)
      self.column()

    self.column(True)
    if header:
      self.header(header)
    if paragraph:
      self.paragraph(paragraph)
    if button:
      self.button(button, link)
    self.column()

    self.row()
    self.grid()

  def list(self, elements):
    # HTML
    border = 0
    self.content_html += ('<table style="margin:20px auto 0px '
                          'auto;padding:0px;border:0px;border-collapse:collapse;">')
    for element in elements:
      self.content_html += ('<tr><td '
                            'style="padding:10px;text-align:%s;border-top:%dpx '
                            'solid #ccc;%s">%s</td></tr>') % (
          self.style['align'], border, self._table_css(),
          self.markup_to_html(element))
      border = 1
    self.content_html += '</table>'

    # Text
    self.content_text += '\n\n'
    for element in elements:
      self.content_text += '  - %s\n' % self.markup_to_text(element)
    self.content_text == '\n'

  def table(self, schema, rows):
    aligns = {
        'BOOLEAN': 'center',
        'INTEGER': 'right',
        'FLOAT': 'right',
        'STRING': 'left',
        'URL': 'center'
    }

    # HTML
    self.content_html += ('<table style="width:100%;margin:20px '
                          '0px;padding:0px;border:0px;border-collapse:collapse;">')
    self.content_html += '<tr>'

    # headers
    for header in schema:
      self.content_html += ('<td '
                            'style="padding:10px;text-align:%s;border-bottom:1px'
                            ' solid #ccc;font-weight:bold;%s">%s</td>') % (
          aligns.get(header['type'], 'left'), self._table_css(), header['name'])
    self.content_html += '</tr>'

    # rows
    for row in rows:
      self.content_html += '<tr>'
      for column, header in enumerate(schema):
        value = row[column]
        # change links into clickable buttons ( do we want to make up our own schema here? for images too? )
        if isinstance(value, str) and value.startswith('http'):
          value = ('<a href="%s" style="border-radius:50px;padding:1px '
                   '12px;%s">&rarr;</a>') % (
              value, self._button_css())
        self.content_html += ('<td '
                              'style="padding:10px;text-align:%s;border-bottom:1px'
                              ' solid #ccc;%s">%s</td>') % (
            aligns.get(header['type'], 'left'), self._table_css(), value)
      self.content_html += '</tr>'

    self.content_html += '</table>'

    # Text
    for row in rows:
      self.content_text += '--------------------------------------------------\n'
      for column, header in enumerate(schema):
        self.content_text += '%s: %s\n' % (header['name'], row[column])
      self.content_text += '\n'

  def get_subject(self):
    return self.subject

  def get_html(self):
    logo = ''
    if self.logo:
      logo += ('<p style="width:100%%;margin:10px auto;padding:0.1em '
               '0px;border:0px;text-align:left;">')
      logo += '<img src="%s" style="margin:10px 0px;padding:0px;border:0px"/>' % self.logo
      logo += '</p>'

    footer = ''
    if self.footer:
      footer += ('<p style="width:100%;margin:30px '
                 'auto;padding:0px;border:0px;text-align:center;">')
      for f in self.footer:
        footer += ('<a href="%s" style="display:inline-block;margin: '
                   '0px;padding:0px '
                   '10px;color:%s;font-family:%s;font-size:15px;font-weight:normal;line-height:32px;text-decoration:none;">%s</a>') % (
            f['link'], self.style['text'], self.style['font'], f['text'])
      footer += '</p>'
    if self.copyright:
      footer += ('<p style="width:100%%;margin:20px '
                 'auto;padding:0px;border:0px;font-weight:bold;text-align:center;color:%(text)s;font-family:%(font)s;font-size:15px;line-height:32px;">') % self.style
      footer += self.copyright
      footer += '</p>'

    return """
      <html>
        <body>
          <div style="width:100%%;padding:40px 0px;margin:0px;background-color:%s;">
            <div style="max-width:600px;width:100%%;padding:0px;margin:0px auto;">
              %s
              <table style="width:100%%;margin:0px auto;text-align:left;background-color:%s">
                <tr><td>%s</td></tr>
              </table>
              %s
            </div>
          </div>
        </body>
      </html>
    """ % (self.style['background'], logo, self.style['foreground'],
           self.content_html, footer)

  def get_text(self):
    footer = ''
    if self.footer:
      footer += '\n--------------------------------------------------\n'
      for f in self.footer:
        footer += '\n%s: %s' % (f['text'], f['link'])
    if self.copyright:
      footer += '\n\n--------------------------------------------------\n\n%s' % self.copyright

    return self.content_text + footer


if __name__ == '__main__':

  t = EmailTemplate()
  t.header('This Is A Header')
  t.paragraph(
      'A paragraph is a few sentences of text.  Although you can use HTML, it will break the text version.'
  )
  t.display('Section Header', 'A section paragraph is a few sentences of text.',
            'http://www.image.com/image.jpg', 'http://www.google.com',
            'A Button')
  t.table([
      {
          'name': 'Column A',
          'type': 'STRING'
      },
      {
          'name': 'Column B',
          'type': 'INTEGER'
      },
      {
          'name': 'Column C',
          'type': 'BOOLEAN'
      },
      {
          'name': 'Column D',
          'type': 'FLOAT'
      },
      {
          'name': 'Column E',
          'type': 'URL'
      },
  ], [
      ['First', 1, True, 1.1, 'http://www.google.com'],
      ['Second', 2, False, 2.2, 'http://www.google.com'],
      ['Third', 3, True, 3.3, 'http://www.google.com'],
  ])
  print(t.get_html())
  print(t.get_text())
