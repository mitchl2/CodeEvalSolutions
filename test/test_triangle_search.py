'''
Created on Jan 2, 2017

@author: Mitchell Lee
'''


import unittest

import triangle_search


class TestTriangleSearch(unittest.TestCase):
    def test_create_num_tree(self):
        """Tests the create_num_tree function.
        """
        nums = [[5], [9, 6], [4, 6, 8], [0, 7, 1, 5]]
        num_tree = triangle_search.create_num_tree(nums)

        self.assertEqual(num_tree.root.value,
                         5,
                         "Expected value (%d) differs from actual (%d)"
                         % (5, num_tree.root.value))

        self.assertEqual(num_tree.root.left.value,
                         9,
                         "Expected value (%d) differs from actual (%d)"
                         % (9, num_tree.root.left.value))

        self.assertEqual(num_tree.root.right.value,
                         6,
                         "Expected value (%d) differs from actual (%d)"
                         % (6, num_tree.root.right.value))

        self.assertEqual(num_tree.root.right.left.right.value,
                         1,
                         "Expected value (%d) differs from actual (%d)"
                         % (1, num_tree.root.right.left.right.value))