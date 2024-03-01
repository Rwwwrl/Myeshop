from .api_router import api_router


@api_router.get('/index/')
def index():
    return {'hello': 'world'}


@api_router.get('/settings/')
def settings():
    from eshop.settings import SETTINGS

    return {'db_name': SETTINGS.db.db_name}
