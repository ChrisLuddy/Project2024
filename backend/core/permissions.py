# core/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

class IsFundAdmin(BasePermission):
    """
    Allows access only to users with the 'fund_admin' role.
    """
    def has_permission(self, request, view):
        if request.user is None or request.user.is_anonymous:
            raise NotAuthenticated("Authentication credentials were not provided.")
        if request.user.role == 'fund_admin':
            return True
        raise PermissionDenied("You do not have the required FundAdmin permissions.")

class IsFundManager(BasePermission):
    """
    Allows access only to users with the 'fund_manager' role.
    """
    def has_permission(self, request, view):
        if request.user is None or request.user.is_anonymous:
            raise NotAuthenticated("Authentication credentials were not provided.")
        if request.user.role == 'fund_manager':
            return True
        raise PermissionDenied("You do not have the required FundManager permissions.")

class IsFundAdminOrFundManager(BasePermission):
    """
    Allows access to users with 'fund_admin' or 'fund_manager' roles.
    """
    def has_permission(self, request, view):
        if request.user is None or request.user.is_anonymous:
            raise NotAuthenticated("Authentication credentials were not provided.")
        if request.user.role in ['fund_admin', 'fund_manager']:
            return True
        raise PermissionDenied("You do not have the required permissions (FundAdmin or FundManager).")