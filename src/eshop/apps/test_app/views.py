from .api_router import api_router


@api_router.get('/index/')
def index():
    return {'hello': 'world'}
