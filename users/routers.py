from rest_framework.routers import DynamicRoute, Route, SimpleRouter


class CustomRouter(SimpleRouter):

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{lookup}/{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy'
                },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{lookup}/{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]