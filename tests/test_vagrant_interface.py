"""Tests for vagrant interface"""
import logging
from pprint import pprint
import unittest

import mock

import vagrant_interface


class TestParsingColumns(unittest.TestCase):
    """Tests for the column parsing stuff"""
    def test_it_should_get_column_names(self):
        # Setup
        example = "id       name         provider   state    directory        "
        expected_names = sorted(["id", "name", "provider", "state", "directory"])
        sut = vagrant_interface.VagrantInterface()
        # Test
        output = sut.get_columns(example)
        # assert
        self.assertEqual(sorted(output.keys()), expected_names)

    def test_it_should_work_out_indexes(self):
        # Setup
        header = "first   second  "
        sut = vagrant_interface.VagrantInterface()
        # Test
        output = sut.get_columns(header)
        # assert
        first_indexes = output['first']
        self.assertEqual(first_indexes, (0, 7))
        second_indexes = output['second']
        self.assertEqual(second_indexes, (8, 15))

    def test_it_should_parse_line_based_on_name_and_indexes(self):
        # Setup
        header = "first   second  "
        line =   "dog 1   cat 2   "
        sut = vagrant_interface.VagrantInterface()
        # Test
        columns = sut.get_columns(header)
        data = sut.columns_to_dict(columns, line)
        # Assert
        self.assertEqual(data['first'], "dog 1")
        self.assertEqual(data['second'], "cat 2")

    def test_it_should_parse_line_when_no_trailing_spaces(self):
        # Setup
        header = "first   second  "
        line =   "dog 1   ham"
        sut = vagrant_interface.VagrantInterface()
        # Test
        columns = sut.get_columns(header)
        data = sut.columns_to_dict(columns, line)
        # Assert
        self.assertEqual(data['first'], "dog 1")
        self.assertEqual(data['second'], "ham")

class TestVagrantInterFaceFunctions(unittest.TestCase):
    @mock.patch("vagrant_interface.VagrantInterface.get_vms", mock.Mock(
        return_value=[
            {'directory': 'C:/Users/me/foo',
            'id': '354',
            'name': 'default',
            'provider': 'virtualbox',
            'state': 'poweroff'},
            {'directory': 'C:/Users/me/vagrant-up-github-pages-master',
            'id': '264',
            'name': 'github-pages',
            'provider': 'virtualbox',
            'state': 'poweroff'},
            {'directory': 'C:/Users/me/bar',
            'id': '040',
            'name': 'default',
            'provider': 'virtualbox',
            'state': 'running'}]))
    def test_it_should_count_running_vms(self):
        # Setup
        sut = vagrant_interface.VagrantInterface()
        # Test/Assert
        self.assertEqual(sut.get_running_count(), 1)

    



logging.basicConfig(level=logging.DEBUG)
# unittest.main()


v = vagrant_interface.VagrantInterface()
vms = v.get_vms()
pprint(vms)