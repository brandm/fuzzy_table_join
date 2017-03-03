#!/usr/bin/env python3
# * fuzzy_table_join.py --- Join tables on fuzzy strings
#   - Copyright (C) 2017-2017 Michael Brand <michael.ch.brand at gmail.com>
#   - Licensed under GPLv3, see http://www.gnu.org/licenses/gpl-3.0.html
#   - URL: http://github.com/brandm/fuzzy_table_join

# * Commentary:
"""Proof of concept to join tables on fuzzy strings with
difflib.get_close_matches in Python 3.
"""
#   - Written with flake8 with "ignore =
#     E129,E201,E241,E271,E302,E305,E306,W503".
#   - Written with the live-py-plugin (Eclipse, Emacs and PyCharm) for
#     Python live coding.
#   - Supports Emacs Outshine mode.
#   - TODO
#     - [-] df1_mutation[on] seems wrong.
#       - [X] Annotate new column for closest match.
#       - [X] join_fuzzy(df1, field1, df2, field2, cutoff)
#       - [ ] Allow no match.
#       - [ ] Annotate new column for alternate matches.
#       - [ ] Annotate new column for number of matches.
#     - [ ] Balance cutoff.
#     - [ ] O(n**2) vs. order.

# * Code:

# * Setup
import difflib
import pandas as pd
import random
import string

# * Input data for test
_df1 = pd.DataFrame(
    [
        ['a1', "Foo1"],
        ['b1', "Bar1"],
    ],
    columns=["Id1", "Name1"])

_df2 = pd.DataFrame(
    [
        ['a2', "Bar2"],
        ['b2', "Foo2"],
    ],
    columns=["Id2", "Name2"])


# * Functions
def join_fuzzy(df1, field1, df2, field2, cutoff):
    df1_mutation = df1.copy()
    random.seed(20170323)
    df1_matched_name = "Matched2-" + ''.join(
        random.choice(string.ascii_letters) for _ in range(5))
    df1_mutation[df1_matched_name] = df1_mutation[field1].map(
        lambda cell:
        difflib.get_close_matches(cell, df2[field2], n=1, cutoff=cutoff)[0])
    return df1_mutation.merge(
        df2, how='outer', left_on=df1_matched_name, right_on=field2)


# * Main
print(_df1, '\n')
print(_df2, '\n')
print(join_fuzzy(_df1, "Name1", _df2, "Name2", 0.7))


# * Live coding
def live_coding():
    import sys # Trigger E261 with this comment to verify that flake8 works
    print(sys.version)
    print(sys.stdout.encoding)


if __name__ == '__live_coding__':
    live_coding()

# * File config
#   Local Variables:
#     coding: us-ascii-unix
#     fill-column: 76
#   End:
