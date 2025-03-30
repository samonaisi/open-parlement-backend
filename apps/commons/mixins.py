class HasOwnerMixin:
    """
    Mixin for models that have an owner.
    """

    def get_owner(self):
        raise NotImplementedError
