from django.contrib.auth.models import AbstractUser

from apps.commons.mixins import HasOwnerMixin


class User(AbstractUser, HasOwnerMixin):
    """
    Custom user model derived from AbstractUser.
    Attributes:
        - username (str): The user's username.
        - first_name (str): The user's first name.
        - last_name (str): The user's last name.
        - email (str): The user's email.
        - is_active (bool): Whether the user is active.
        - is_staff (bool): Whether the user is staff.
        - is_superuser (bool): Whether the user is a superuser.
    """

    def get_owner(self):
        return self
