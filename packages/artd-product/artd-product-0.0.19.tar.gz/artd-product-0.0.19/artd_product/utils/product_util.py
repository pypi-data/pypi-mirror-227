from artd_product.models import (
    Category,
)


def get_categories_tree(category_id=None):
    if category_id is None:
        categories = Category.objects.filter(parent=None)
    else:
        categories = Category.objects.filter(id__gte=category_id)
    categories_tree = []
    for category in categories:
        category_tree = {
            "id": category.id,
            "text": category.name,
            "state": {
                "opened": True,
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
            "id": child.id,
            "text": child.name,
            "state": {
                "opened": True,
                "selected": False,
            },
            "children": get_children(child),
        }
        children_tree.append(child_tree)
    return children_tree
