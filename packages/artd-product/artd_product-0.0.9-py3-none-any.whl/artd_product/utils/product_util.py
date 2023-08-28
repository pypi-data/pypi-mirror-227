from artd_product.models import (
    Category,
)


def get_categories_tree():
    categories = Category.objects.filter(parent=None)
    categories_tree = []
    for category in categories:
        category_tree = {
            "id": category.id,
            "text": category.name,
            "state": {
                "opened": False,
                "selected": False,
            },
            "children": get_children(category),
        }
        categories_tree.append(category_tree)
    return categories_tree


def get_children(category):
    children = Category.objects.filter(parent=category)
    children_tree = []
    for child in children:
        child_tree = {
            "id": category.id,
            "text": category.name,
            "state": {
                "opened": False,
                "selected": False,
            },
            "children": get_children(child),
        }
        children_tree.append(child_tree)
    return children_tree
