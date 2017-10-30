# -*- coding: cp1252 -*-

##
#
# THIS IS AN EXERPT FROM XLRD's (https://github.com/python-excel/xlrd) FORMATTING.PY
#
#
# Module for formatting information.
#
# <p>Copyright © 2005-2012 Stephen John Machin, Lingfo Pty Ltd</p>
# <p>This module is part of the xlrd package, which is released under
# a BSD-style licence.</p>
##

# No part of the content of this file was derived from the works of David Giffin.

# 2010-10-30 SJM Added space after colon in "# coding" line to work around IBM iSeries Python bug
# 2009-05-31 SJM Fixed problem with non-zero reserved bits in some STYLE records in Mac Excel files
# 2008-08-03 SJM Ignore PALETTE record when Book.formatting_info is false
# 2008-08-03 SJM Tolerate up to 4 bytes trailing junk on PALETTE record
# 2008-05-10 SJM Do some XF checks only when Book.formatting_info is true
# 2008-02-08 SJM Preparation for Excel 2.0 support
# 2008-02-03 SJM Another tweak to is_date_format_string()
# 2007-12-04 SJM Added support for Excel 2.x (BIFF2) files.
# 2007-10-13 SJM Warning: style XF whose parent XF index != 0xFFF
# 2007-09-08 SJM Work around corrupt STYLE record
# 2007-07-11 SJM Allow for BIFF2/3-style FORMAT record in BIFF4/8 file

from __future__ import unicode_literals
import re


date_chars = 'ymdhs' # year, month/minute, day, hour, second
date_char_dict = {}
for _c in date_chars + date_chars.upper():
    date_char_dict[_c] = 5
del _c, date_chars

skip_char_dict = {}
for _c in '$-+/(): ':
    skip_char_dict[_c] = 1

num_char_dict = {
    '0': 5,
    '#': 5,
    '?': 5,
    }

non_date_formats = {
    '0.00E+00':1,
    '##0.0E+0':1,
    'General' :1,
    'GENERAL' :1, # OOo Calc 1.1.4 does this.
    'general' :1,  # pyExcelerator 0.6.3 does this.
    '@'       :1,
    }

fmt_bracketed_sub = re.compile(r'\[[^]]*\]').sub


def is_date_format_string(fmt):
    # Heuristics:
    # Ignore "text" and [stuff in square brackets (aarrgghh -- see below)].
    # Handle backslashed-escaped chars properly.
    # E.g. hh\hmm\mss\s should produce a display like 23h59m59s
    # Date formats have one or more of ymdhs (caseless) in them.
    # Numeric formats have # and 0.
    # N.B. u'General"."' hence get rid of "text" first.
    # TODO: Find where formats are interpreted in Gnumeric
    # TODO: u'[h]\\ \\h\\o\\u\\r\\s' ([h] means don't care about hours > 23)
    state = 0
    s = ''
    ignorable = lambda key: key in skip_char_dict
    for c in fmt:
        if state == 0:
            if c == '"':
                state = 1
            elif c in r"\_*":
                state = 2
            elif ignorable(c):
                pass
            else:
                s += c
        elif state == 1:
            if c == '"':
                state = 0
        elif state == 2:
            # Ignore char after backslash, underscore or asterisk
            state = 0
        assert 0 <= state <= 2
    s = fmt_bracketed_sub('', s)
    if s in non_date_formats:
        return False
    state = 0
    separator = ";"
    got_sep = 0
    date_count = num_count = 0
    for c in s:
        if c in date_char_dict:
            date_count += date_char_dict[c]
        elif c in num_char_dict:
            num_count += num_char_dict[c]
        elif c == separator:
            got_sep = 1
    # print num_count, date_count, repr(fmt)
    if date_count and not num_count:
        return True
    if num_count and not date_count:
        return False
    return date_count > num_count
