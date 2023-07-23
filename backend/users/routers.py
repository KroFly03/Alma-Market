from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        url_map = {}
        bound_methods = super().get_method_map(viewset, method_map)

        for method, action in bound_methods.items():
            if action not in ['reset_username', 'reset_username_confirm', 'set_username', 'set_password']:
                url_map[method] = action

        return url_map
