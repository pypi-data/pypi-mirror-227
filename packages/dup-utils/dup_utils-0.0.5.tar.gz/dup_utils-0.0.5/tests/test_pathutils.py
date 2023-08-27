import unittest

import src.dup_utils.core.pathutils as pathutils


class PathutilsTestCase(unittest.TestCase):
    def test_join_path(self):
        self.assertEqual(
            pathutils.join_path("conf", "test", abs=False), "conf/test"
        )
