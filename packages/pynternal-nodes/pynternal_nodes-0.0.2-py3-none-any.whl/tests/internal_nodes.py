"""
        4
     /  |  \
    1   0   5
   /       / \
  2       6   3
"""

tree = [4, 4, 1, 5, -1, 4, 5]
assert find_internal_nodes_num(tree) == 3


"""
        4
     /  |  \
    1   0   5
           / \
          2   3
"""

tree = [4, 4, 5, 5, -1, 4, 5]
assert find_internal_nodes_num(tree) == 2


"""
        4
     /  |  \
    1   0   5
   /    |  / \
  2     7 6   3
"""

tree = [4, 4, 1, 5, -1, 4, 5, 7]
assert find_internal_nodes_num(tree) == 4


"""
        4
     /     \
    1       0
   /         \
  2           3
"""

tree = [4, 4, 1, 0, -1]
assert find_internal_nodes_num(tree) == 3


"""
        0
"""

tree = [-1]
assert find_internal_nodes_num(tree) == 0


"""
        4
        |
        3
        |
        2
        |
        1
        |
        0
"""

tree = [1, 2, 3, 4, -1]
assert find_internal_nodes_num(tree) == 4

assert find_internal_nodes_num([]) == 0

"""
        0
        |
        1
"""

tree = [-1, 0]
assert find_internal_nodes_num(tree) == 1
