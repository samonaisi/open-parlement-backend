from rest_framework.routers import DefaultRouter


class ExtendedRouter(DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    """

    def extend(self, router: DefaultRouter):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)
