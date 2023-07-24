from django.utils.translation import gettext as _
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions


class TinyResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5


class Map(dict):
    """
    Convert dict to obj
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


err_msgs = Map({
    'FIELDS_REQUIRED': _('Field(s) required: {fields}'),
    'OBJECT_NOT_EXISTS': _('Invalid or not existing object.'),
    'INVALID_ADMIN': _('Please authorize with a valid admin.'),
    'INVALID_CRED': _('Invalid credentials.'),
    'INVALID_PASSWORD': _('Empty or invalid password'),
    'USER_NOT_EXIST': _('User does not exist.'),
    'SEARCH_KEY_NOT_EXISTS': _('"search_key": This parameter is required.'),
    'SEARCH_VALUE_NOT_EXISTS': _('"search_value": This parameter is required.'),
    'OK': _('Success!')
})


# Custom permissions
class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' if hasattr(view,
                                                  'action') else request.method == 'POST' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update', 'partial_update'] if hasattr(view,
                                                                                  'action') else request.method in [
            'GET', 'PUT', 'PATCH'] and obj.id == request.user.id or request.user.is_staff


class AnonListOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous GET
        - allow authenticated POST for staff
    """

    def has_permission(self, request, view):
        return view.action == 'retrieve' if hasattr(view,
                                                    'action') else request.method == 'GET' or request.user and request.user.is_staff


class ListAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request, view):
        return view.action != 'list' if hasattr(view,
                                                'action') else request.method != 'GET' or request.user and request.user.is_staff
