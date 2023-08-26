import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

from util_lib.utils import reallypath

from bdrc_irat.PsParser import  PsArgs, PsParser
from bdrc_irat import build_work_list


class MyTestCase(unittest.TestCase):
    test_data_file_entries: [] = ['IW1', 'I21', 'DUPLICATE']

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_parser_container_arguments(self):
        expected_container: str = "expectedContainer"
        expected_infile: Path = Path(self.test_dir, "expectedInfile")

        # Not strictly needed, but the file needs to exist for the parser
        with open(expected_infile, "w") as outf:
            outf.write("dontmatter\n")

        testargs = ["prog", "-c", expected_container, "-w", "w1", "w2,", "w3", "-i", str(expected_infile)]
        with patch.object(sys, 'argv', testargs):
            ns = PsArgs()
            pp = PsParser()
            pp.parse_args(ns)
            from util_lib.utils import reallypath
            self.assertEqual(ns.container, reallypath(expected_container), "Container doesnt match")
            self.assertEqual(len(ns.work_rids), 3, "work_rids not expected")
            self.assertEqual(ns.input_list_file.name, str(expected_infile))

    def test_parser_no_container_arguments(self):
        """
        Test parser when no container given
        :return:
        """
        expected_infile: Path = Path(self.test_dir, "expectedInfile")

        open(expected_infile,'w').close()

        testargs = ["prog", "-w", "w1", "w2,", "w3", "-i", str(expected_infile)]
        # Not strictly needed, but the file needs to exist for the parser
        # with open(expected_infile, "w") as outf:
        #     outf.write("dontmatter\n")

        with patch.object(sys, 'argv', testargs):
            ns = PsArgs()
            pp = PsParser()
            pp.parse_args(ns)
            self.assertEqual(len(ns.work_rids), 3, "work_rids not expected")

    def test_parser_works_only(self):
        """
        Test the parser when only works are given
        :return:
        """
        testargs = ["prog", "-w", "w1", "w2,", "w3"]
        with patch.object(sys, 'argv', testargs):
            ns = PsArgs()
            pp = PsParser()
            pp.parse_args(ns)
            self.assertEqual(len(ns.work_rids), 3, "work_rids not expected")

    def test_build_work_list_from_container_infile(self):
        test_source_data: Path = Path(self.test_dir, "test_works")

        with open(str(test_source_data), "w") as outf:
            for x in self.test_data_file_entries:
                outf.write(x + "\n")

            # io.TextIOWrapper(outf).writelines(self.test_data_file_entries)
            # This leaves the \n in the result
            # outf.writeline(self.test_data_file_entries, '\n')

        testargs: [] = ["prog", "-c", "SomeContainer", "-w", "w1", "DUPLICATE", "w3", "-i", str(test_source_data)]
        with patch.object(sys, 'argv', testargs):
            ns = PsArgs()
            pp = PsParser()
            pp.parse_args(ns)
            result_list: [] = build_work_list(ns)

            # No duplicates ("DUPLICATE")
            self.assertEqual(len(result_list), 5)
            self.assertTrue(Path(reallypath("SomeContainer"), "IW1") in result_list)
            self.assertTrue(Path(reallypath("SomeContainer"), "I21") in result_list)
            self.assertTrue(Path(reallypath("SomeContainer"), "DUPLICATE") in result_list)
            self.assertTrue(Path(reallypath("SomeContainer"), "w1") in result_list)
            self.assertTrue(Path(reallypath("SomeContainer"), "w3") in result_list)


if __name__ == '__main__':
    unittest.main()
