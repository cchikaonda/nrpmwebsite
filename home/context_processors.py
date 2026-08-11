from home.models import SubMenuLink

def submenu_links(request):
    """
    Provide submenu links grouped by parent menu title
    """
    submenu_links_by_parent = {}

    for item in SubMenuLink.objects.all():
        if item.parent_title not in submenu_links_by_parent:
            submenu_links_by_parent[item.parent_title] = []
        submenu_links_by_parent[item.parent_title].append(item)

    return {
        "submenu_links_by_parent": submenu_links_by_parent
    }
