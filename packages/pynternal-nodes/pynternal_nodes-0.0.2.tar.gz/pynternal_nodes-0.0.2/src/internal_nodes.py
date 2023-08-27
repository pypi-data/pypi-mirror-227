def find_internal_nodes_num(tree):
    tree = set(tree)
    tree.discard(-1)
    return len(tree)
