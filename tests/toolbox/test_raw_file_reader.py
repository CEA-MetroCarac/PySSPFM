"""
Test raw_file_reader methods
"""

from pytest import skip

from examples.toolbox.ex_raw_file_reader import example_raw_file_reader
from PySSPFM.utils.raw_extraction import NanoscopeError


# class TestSignalViewer(unittest.TestCase):


# Error when Nanoscope Analysis wheel is not installed
def test_raw_file_reader_spm():
    """ Test example_raw_file_reader for 'spm' file """
    try:
        example_raw_file_reader('spm')
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")


def test_raw_file_reader_txt():
    """ Test example_raw_file_reader for 'txt' file """

    example_raw_file_reader('txt')


def test_raw_file_reader_csv():
    """ Test example_raw_file_reader for 'csv' file """

    example_raw_file_reader('csv')


def test_raw_file_reader_xlsx():
    """ Test example_raw_file_reader for 'xlsx' file """

    example_raw_file_reader('xlsx')
