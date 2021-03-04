from rest_framework.routers import Route, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A router for APIs that uses trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]
