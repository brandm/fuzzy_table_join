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
#     - [X] df1_mutation[on] seems wrong.
#       - [X] Annotate new column for closest match.
#       - [X] join_fuzzy(df1, field1, df2, field2, cutoff)
#       - [X] Allow no match.
#       - [X] Annotate new column for alternate matches.
#       - [X] Annotate new column for number of matches.
#     - [ ] Balance cutoff.
#     - [ ] O(n**2) vs. order.

# * Code:

# * Setup
import difflib
import pandas as pd
import random
import string

random.seed(2017_03_23)

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
        ['b3', "Bar3"],
        ['b4', "Bar4"],
    ],
    columns=["Id2", "Name2"])


# * Functions
def join_fuzzy(df1, field1, df2, field2, cutoff):
    """Fuzzy join df1.field1 on df2.field2, add some columns.
    """

    # Search close matches.
    close_matches = list(df1[field1].map(
        lambda cell:
        difflib.get_close_matches(cell, df2[field2], n=9, cutoff=cutoff)))
    # Enrich df1 by adding columns.
    df1_add_cols = df1.copy()
    # Match: Column with number of matches.
    df1_add_cols[append_rand("Match", 0)] = [len(x) for x in close_matches]
    # Closest: Column with closest match.
    closest_name = append_rand("Closest", 0)
    df1_add_cols[closest_name] = [x[0] if x else '-' for x in close_matches]
    # Alternatives: Column with Python list of alternative matches.
    df1_add_cols[append_rand("Alternatives", 0)] = [
        x[1:] if len(x) >= 2 else '-' for x in close_matches]

    # Join df2 to the enriched df1 on closest match.
    return df1_add_cols.merge(
        df2, how='left', left_on=closest_name, right_on=field2)


def append_rand(s, suffix_len):
    """Return string with appendend "-" and a random suffix.
    """

    if suffix_len:
        return s + "-" + ''.join([random.choice(string.ascii_letters)
                                  for _ in range(suffix_len)])
    else:
        return s


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
