'''
Created on Jan 1, 2017

Contains functions for iterating over a tree of numbers to determine
the maximum sum from top to bottom.

@author: Mitchell Lee
'''


class NumTree(object):
    """Contains a tree of numbers.
    """

    def __init__(self, root):
        """Constructs a new NumTree.

        Args:
            root: A NumNode.
        """
        self.root = root


class NumNode(object):
    """Contains a tree node value.
    """

    def __init__(self, value):
        """Constructs a new Node.

        Args:
            value: An integer.
        """
        self.value = value
        self.left = None
        self.right = None


def create_num_tree(nums):
    """Constructs a NumTree from a sequence of numbers.

    Args:
        nums: A list of lists, where each nested list contains a sequence
            of numbers, and the length of each consecutive nested list
            increases by one.

    Returns:
        A NumTree containing all numbers.
    """
    pass


def find_max_sum(tree):
    """Returns the maximum sum from the top to the bottom of the tree.

    Args:
        tree: A NumTree.

    Returns:
        The maximum sum from the top to the bottom of the tree.
    """
    pass