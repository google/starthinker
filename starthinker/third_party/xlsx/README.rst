python-xlsx
===========

A small footprint xlsx reader that understands shared strings and can process
excel dates.


Requirements
------------

No external requirements.  Supports Python versions 2.6+ and 3.2+.


Usage
-----

::

    book = Workbook('filename or filedescriptor') #Open xlsx file
    for sheet in book:
        print sheet.name
        # for larger workbooks, use sheet.rowsIter() instead of
        # sheet.rows().iteritems()
        for row, cells in sheet.rows().iteritems(): # or sheet.cols()
            print row # prints row number
            for cell in cells:
                print cell.id, cell.value, cell.formula

    # or you can access the sheets by their name:

    some_sheet = book['some sheet name']
    ...


Alternatives
------------

To my knowledge there are other python alternatives:

 * https://bitbucket.org/ericgazoni/openpyxl/
 * https://github.com/leegao/pyXLSX
