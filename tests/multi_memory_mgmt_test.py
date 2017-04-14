#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

import pycurl
import unittest
import gc
import flaky

debug = False

@flaky.flaky(max_runs=3)
class MultiMemoryMgmtTest(unittest.TestCase):
    def test_opensocketfunction_collection(self):
        self.check_callback(pycurl.M_SOCKETFUNCTION)
    
    def test_seekfunction_collection(self):
        self.check_callback(pycurl.M_TIMERFUNCTION)
    
    def check_callback(self, callback):
        # Note: extracting a context manager seems to result in
        # everything being garbage collected even if the C code
        # does not clear the callback
        object_count = 0
        gc.collect()
        # gc.collect() can create new objects... running it again here
        # settles tracked object count for the actual test below
        gc.collect()
        object_count = len(gc.get_objects())
        
        c = pycurl.CurlMulti()
        c.setopt(callback, lambda x: True)
        del c
        
        gc.collect()
        new_object_count = len(gc.get_objects())
        # it seems that GC sometimes collects something that existed
        # before this test ran, GH issues #273/#274
        self.assertTrue(new_object_count in (object_count, object_count-1))
