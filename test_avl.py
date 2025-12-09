from AVLTree import AVLTree


def assert_avl(tree):
    def dfs(node):
        if node is None or not node.is_real_node():
            return -1
        lh = dfs(node.left)
        rh = dfs(node.right)
        if abs(lh - rh) > 1:
            raise AssertionError(f"Unbalanced at key {node.key}: lh={lh}, rh={rh}")
        expected_height = 1 + max(lh, rh)
        if node.height != expected_height:
            raise AssertionError(
                f"Height mismatch at key {node.key}: got {node.height}, expected {expected_height}"
            )
        return expected_height

    dfs(tree.root)


def assert_children_present(tree):
    """Ensure every real node has explicit (possibly virtual) children."""
    def dfs(node):
        if node is None or not node.is_real_node():
            return
        if node.left is None or node.right is None:
            raise AssertionError(f"Missing child pointer at key {node.key}")
        dfs(node.left)
        dfs(node.right)
    dfs(tree.root)


def test_basic_insert_delete():
    T = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]:
        T.insert(k, str(k))
    assert_avl(T)
    assert [k for k, _ in T.avl_to_array()] == [10, 20, 25, 30, 40, 50]
    assert T.size() == 6

    node, _ = T.search(25)
    T.delete(node)
    assert_avl(T)
    assert T.size() == 5
    node, _ = T.search(30)
    T.delete(node)
    assert_avl(T)
    assert [k for k, _ in T.avl_to_array()] == [10, 20, 40, 50]
    assert T.size() == 4


def test_join_and_split():
    A = AVLTree()
    B = AVLTree()
    for k in [1, 2, 3]:
        A.insert(k, str(k))
    for k in [5, 6, 7]:
        B.insert(k, str(k))

    A.join(B, 4, "4")
    assert_avl(A)
    assert_children_present(A)
    assert [k for k, _ in A.avl_to_array()] == [1, 2, 3, 4, 5, 6, 7]
    assert A.size() == 7
    assert B.root is None and B.size() == 0  # tree2 invalidated

    node, _ = A.search(4)
    left, right = A.split(node)
    assert [k for k, _ in left.avl_to_array()] == [1, 2, 3]
    assert [k for k, _ in right.avl_to_array()] == [5, 6, 7]
    assert left.size() == 3 and right.size() == 3
    assert_avl(left)
    assert_avl(right)
    assert_children_present(left)
    assert_children_present(right)


if __name__ == "__main__":
    test_basic_insert_delete()
    test_join_and_split()
    print("all tests passed")
