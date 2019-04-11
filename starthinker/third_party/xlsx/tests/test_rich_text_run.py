# vim: fileencoding=utf8 sw=2 ts=2 et
import os
import unittest

from xlsx import Workbook

class TestRichTextRun(unittest.TestCase):
  def setUp(self):
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    'fixtures'))
    self.workbook = Workbook(os.path.join(fixtures_dir, 'richtextrun.xlsx'))
    return

  def testRichTextRun(self):
    sheetRtr = self.workbook['rtr']
    self.assertEqual(sheetRtr['A1'].value, 'ab')
    return

if '__main__' == __name__:
  unittest.main()
