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
            increases by one. Must contain at least list.

    Returns:
        A NumTree containing all numbers.
    """
    if len(nums) == 0:
        raise Exception("List of lists must be non-empty")

    # A cache of Node objects by index in nums and index into their
    # respective list of numbers.
    node_cache = {}

    def traverse_tree(nums, num_list_level, num_list_index):
        """Helper function that creates a NumTree.
        """
        if (num_list_level in node_cache and
            num_list_index in node_cache[num_list_level]):
            return node_cache[num_list_level][num_list_index]
        else:
            if num_list_level not in node_cache:
                node_cache[num_list_level] = {}

            if num_list_index not in node_cache[num_list_level]:
                node_cache[num_list_level][num_list_index] = {}

            node = NumNode(nums[num_list_level][num_list_index])

            # Store the node in the cache
            node_cache[num_list_level][num_list_index] = node

            # Create left and right nodes
            if num_list_level != len(nums) - 1:
                node.left = traverse_tree(nums,
                                          num_list_level + 1,
                                          num_list_index)
                node.right = traverse_tree(nums,
                                           num_list_level + 1,
                                           num_list_index + 1)

            return node

    return NumTree(traverse_tree(nums, 0, 0))


def find_max_sum(tree):
    """Returns the maximum sum from the top to the bottom of the tree.

    Args:
        tree: A NumTree.

    Returns:
        The maximum sum from the top to the bottom of the tree.
    """
    pass