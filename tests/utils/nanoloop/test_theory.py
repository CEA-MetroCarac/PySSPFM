"""
Test theory methods
"""

from examples.utils.nanoloop.ex_theory import example_theory


# class TestTheory(unittest.TestCase):


def test_theory():
    """ Test example_file """

    figs = example_theory()
    assert len(list(figs)) == 3
