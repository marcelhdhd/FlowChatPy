import unittest
import sys
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
import gui.master_window

class TestUIMainWindow(unittest.TestCase):

    def test_main_window(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
