#!/usr/bin/python

import unittest
import shutil
import os
import pyment.pyment as pym

myelem = '    def my_method(self, first, second=None, third="value"):'
mydocs = '''        """This is a description of a method.
        It is on several lines.
        Several styles exists:
            -javadoc,
            -reST,
            -cstyle.
        It uses the javadoc style.

        @param first: the 1st argument.
        with multiple lines
        @type first: str
        @param second: the 2nd argument.
        @return: the result value
        @rtype: int
        @raise: KeyError

        """'''
inifile = 'origin_test.py'
jvdfile = 'javadoc_test.py'
rstfile = 'rest_test.py'


class DocStringTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # prepare test file
        shutil.copyfile(inifile, jvdfile)
        fs = open(jvdfile, 'r')
        ft = open(rstfile, 'w')
        txt = fs.read()
        txt = txt.replace("@return", ":returns")
        txt = txt.replace("@raise", ":raises")
        txt = txt.replace("@", ":")
        ft.write(txt)
        fs.close()
        ft.close()
        print("setup")

    @classmethod
    def tearDownClass(cls):
        os.remove(jvdfile)
        os.remove(rstfile)
        print("end")

    def testParsedJavadoc(self):
        p = pym.PyComment(inifile)
        p._parse()
        self.failUnless(p.parsed)

    def testSameOutJavadocReST(self):
        pj = pym.PyComment(jvdfile)
        pr = pym.PyComment(rstfile)
        pj._parse()
        pr._parse()
        self.assertEqual(pj.get_output_docs(), pr.get_output_docs())


def main():
    unittest.main()

if __name__ == '__main__':
    main()

