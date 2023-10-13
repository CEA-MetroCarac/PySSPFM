"""
Test raw_file_reader methods
"""

from examples.toolbox.ex_raw_file_reader import example_raw_file_reader


# class TestSignalViewer(unittest.TestCase):


def test_raw_file_reader_spm():
    """ Test example_raw_file_reader for 'spm' file """

    example_raw_file_reader('spm')


def test_raw_file_reader_txt():
    """ Test example_raw_file_reader for 'txt' file """

    example_raw_file_reader('txt')


def test_raw_file_reader_csv():
    """ Test example_raw_file_reader for 'csv' file """

    example_raw_file_reader('csv')


def test_raw_file_reader_xlsx():
    """ Test example_raw_file_reader for 'xlsx' file """

    example_raw_file_reader('xlsx')
