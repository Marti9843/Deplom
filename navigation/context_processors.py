def navigation_items(request):
    nav_items = [
        {'name': 'Головна', 'url': 'home'},
        {'name': 'Про нас', 'url': 'about'},
        {'name': 'Послуги', 'url': 'services:fitness'},
        {'name': 'Контакти', 'url': 'contact'},
    ]
    return {'nav_items': nav_items}