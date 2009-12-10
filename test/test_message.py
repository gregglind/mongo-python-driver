# Copyright 2009 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test the messages module."""

import unittest
import os
import sys
sys.path[0:0] = [""]

from nose.plugins.skip import SkipTest

class TestComapreUpdate(unittest.TestCase):
    
    def setUp(self):
        import pymongo.message as message
        self.message = message
        
        try:
            import pymongo._cbson as cb
            self.cb = cb
        except ImportError:
            raise SkipTest()

    def test_update_compare(self):
        ''' compare _cbson._update_message to message.update'''
        args = ("coll",True,True,{"name": "a"}, {"$inc": {"n":1}},True)
        
        # sanity checks for import
        self.assert_(id(self.message.update) == id(self.cb._update_message))
        self.assert_(id(self.message.update) != id(self.message._update_py))
        
        # try messages under both systems
        (p1, m1) = self.message._update_py(*args)
        (p2, m2) = self.cb._update_message(*args)
        samelen = len(m1) == len(m2)
        self.assert_(samelen)
        # these bytes are the random request id
        not_same = [4,5,6,7,73,74,75,76]
        bytes_same = [b1 == b2 for (ii,(b1,b2)) in enumerate(zip(m1,m2)) \
                        if ii not in not_same]
        sameish = False not in bytes_same  # since we don't have "all" in py2.4
        self.assert_(sameish)

if __name__ == "__main__":
    unittest.main()