from __future__ import annotations

from typing import Any

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested.routers import NestedMixin


class TruncatedNestedSimpleRouter(NestedMixin, SimpleRouter):
    """Nested router that uses exactly the lookup name as the kwarg,
    without appending the parent's lookup_field (e.g. 'pk').

    This produces <*_id> instead of <*_id_pk> in URL patterns.
    """

    def __init__(
        self,
        parent_router: SimpleRouter | DefaultRouter | NestedMixin,
        parent_prefix: str,
        *args: Any,
        lookup: str = 'pk',
        **kwargs: Any,
    ) -> None:
        self.parent_router = parent_router
        self.parent_prefix = parent_prefix
        self.nest_count = getattr(parent_router, 'nest_count', 0) + 1
        self.nest_prefix = lookup
        self.use_regex_path = kwargs.get('use_regex_path', True)

        SimpleRouter.__init__(self, *args, **kwargs)

        if 'trailing_slash' not in kwargs:
            self.trailing_slash = parent_router.trailing_slash

        parent_registry = [
            registered
            for registered in self.parent_router.registry  # type: ignore[union-attr]
            if registered[0] == self.parent_prefix
        ]
        try:
            _parent_prefix, parent_viewset, parent_basename = parent_registry[0]
        except IndexError as e:
            raise RuntimeError('parent registered resource not found') from e

        self.check_valid_name(self.nest_prefix)

        # Build parent lookup regex using exactly `nest_prefix` as the kwarg name,
        # without appending the parent's lookup_field.
        parent_lookup_regex = f'(?P<{self.nest_prefix}>[^/.]+)'

        self.parent_regex = f'{parent_prefix}/{parent_lookup_regex}/'
        if not self.parent_prefix and self.parent_regex[0] == '/':
            self.parent_regex = self.parent_regex[1:]
        if hasattr(parent_router, 'parent_regex'):
            self.parent_regex = parent_router.parent_regex + self.parent_regex

        nested_routes = []
        for route in self.routes:
            route_contents = route._asdict()
            escaped_parent_regex = self.parent_regex.replace('{', '{{').replace('}', '}}')

            if self.use_regex_path:
                route_contents['url'] = route.url.replace('^', '^' + escaped_parent_regex)
            else:
                route_contents['url'] = escaped_parent_regex + route_contents['url']

            nested_routes.append(type(route)(**route_contents))

        self.routes = nested_routes
