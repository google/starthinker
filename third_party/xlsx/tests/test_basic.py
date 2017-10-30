# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest

import six

from xlsx import Workbook

class WorkbookTestCase(unittest.TestCase):

    def setUp(self):
        """ Getting all file from fixtures dir """
        self.workbooks = {}
        fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    'fixtures'))
        xlsx_files = os.listdir(fixtures_dir)
        for filename in xlsx_files:
            self.workbooks[filename] = Workbook(
                os.path.join(fixtures_dir, filename))

    def test_basic(self):
        """ These test will run for all test files """

        for filename, workbook in self.workbooks.items():
            for sheet in workbook:
                assert hasattr(sheet, 'id')
                assert isinstance(sheet.name, six.string_types)
                assert isinstance(sheet.rows(), dict)
                assert isinstance(sheet.cols(), dict)

                for row_num, cells in six.iteritems(sheet.rows()):
                    assert isinstance(row_num, int)
                    assert isinstance(cells, list)
                    for cell in cells:
                        assert hasattr(cell, 'id')
                        assert hasattr(cell, 'column')
                        assert hasattr(cell, 'row')
                        assert hasattr(cell, 'value')
                        assert cell.row == row_num

    def test_test1(self):
        """ Specific test for `testdata/test1.xslx` file including
        unicode strings and different date formats
        """
        workbook = self.workbooks['test1.xlsx']

        self.assertEqual(workbook[1].name, 'рускии')
        self.assertEqual(workbook[2].name, '性 文化交流 例如')
        self.assertEqual(workbook[3].name, 'تعد. بحق طائ')

        for row_num, cells in six.iteritems(workbook[1].rows()):
            if row_num == 1:
                self.assertEqual(cells[0].value, 'лорем ипсум')
                self.assertEqual(cells[1].value, '2')
            if row_num == 2: #Test date fields
                self.assertEqual(cells[0].value, (2010, 11, 12, 0, 0, 0))
                self.assertEqual(cells[1].value, (1987, 12, 20, 0, 0, 0))
                self.assertEqual(cells[2].value, (1987, 12, 20, 0, 0, 0))
                self.assertEqual(cells[3].value, (1987, 12, 20, 0, 0, 0))
                break

        # Cell A1 in '性 文化交流 例如'
        self.assertEqual(workbook[2].cols()['A'][0].value,
                         '性 文化交流 例如')
        self.assertEqual(workbook[2].cols()['A'][1].value,
                         'エム セシビ め「こを バジョン')

    def test_dcterms_modified(self):
        self.assertTrue(self.workbooks['test1.xlsx'].dcterms_modified is None)
        self.assertEqual(self.workbooks['modified_date.xlsx'].dcterms_modified,
                         '2012-07-01T05:04:12Z')

    def test_cell_str(self):
        workbook = self.workbooks['test1.xlsx']
        cell = workbook[2].cols()['A'][0]
        value = '<Cell [A1] : "性 文化交流 例如" (None)>'
        # Python 2 returns bytestring (str type), Python 3 returns unicode (str type).
        if six.PY2:
            self.assertEqual(str(cell), value.encode('utf-8'))
        else: # Python 3.
            self.assertEqual(str(cell), value)

    def test_cell_unicode(self):
        workbook = self.workbooks['test1.xlsx']
        cell = workbook[2].cols()['A'][0]
        value = '<Cell [A1] : "性 文化交流 例如" (None)>'
        # Both Python 2 and 3 should return the same (unicode, or str on Python 3) here.
        self.assertEqual(cell.__unicode__(), value)

    def test_dates(self):
        # tests out different date formats
        workbook = self.workbooks['test_dates.xlsx']
        self.assertEqual(workbook[1]['B1'].value, '1')
        self.assertEqual(workbook[1]['B2'].value, (2012, 8, 13, 0, 0, 0))
        self.assertEqual(workbook[1]['B3'].value, (1900, 3, 1, 0, 0, 0))
        self.assertEqual(workbook[1]['B4'].value, (2200, 12, 31, 0, 0, 0))
        self.assertEqual(workbook[1]['B5'].value, (2012, 8, 13, 12, 11, 0))


class FileHandleWorkbookTestCase(WorkbookTestCase):
    """
    Run all the same tests in WorkbookTestCase, but using open file handles
    instead of file paths.
    """

    def setUp(self):
        """ Getting all file from fixtures dir """
        self.workbooks = {}
        fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    'fixtures'))
        xlsx_files = os.listdir(fixtures_dir)
        for filename in xlsx_files:
            filepath = os.path.join(fixtures_dir, filename)
            self.workbooks[filename] = Workbook(open(filepath, 'rb'))


if __name__ == '__main__':
    unittest.main()
