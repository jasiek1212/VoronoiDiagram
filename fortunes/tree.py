from .fortune_algorithm import BeachlineItemType


def get_first_left_parent(item):
    current = item
    while current.parent is not None and current.parent.left == current:
        current = current.parent
    assert current.parent is None or current.parent.item_type == BeachlineItemType.Edge
    return current.parent


def get_first_right_parent(item):
    current = item
    while current.parent is not None and current.parent.right == current:
        current = current.parent
    assert current.parent is None or current.parent.item_type == BeachlineItemType.Edge
    return current.parent


def get_first_left_leaf(item):
    if item.left is None:
        return None
    current = item.left
    while current.right is not None:
        current = current.right
    assert current.item_type == BeachlineItemType.Arc
    return current


def get_first_right_leaf(item):
    if item.right is None:
        return None
    current = item.right
    while current.left is not None:
        current = current.left
    assert current.item_type == BeachlineItemType.Arc
    return current


def delete_beachline_item(item):
    if item is None:
        return
    delete_beachline_item(item.left)
    delete_beachline_item(item.right)


def count_beachline_items(root):
    if root is None:
        return 0
    left_count = count_beachline_items(root.left)
    right_count = count_beachline_items(root.right)
    return left_count + right_count + 1



def check_no_references_to_item(root, item):
    if root is None or root.item_type == BeachlineItemType.Arc:
        return
    
    assert root.parent != item
    assert root.left != item
    assert root.right != item

    check_no_references_to_item(root.left, item)
    check_no_references_to_item(root.right, item)

