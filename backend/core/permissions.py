# core/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsFundAdmin(BasePermission):
    """
    Allows access only to users in the FundAdmin group.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.groups.filter(name='FundAdmin').exists()):
            raise PermissionDenied("You do not have the required FundAdmin permissions.")
        return True


class IsFundManager(BasePermission):
    """
    Allows access only to users in the FundManager group.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.groups.filter(name='FundManager').exists()):
            raise PermissionDenied("You do not have the required FundManager permissions.")
        return True

class IsFundAdminOrFundManager(BasePermission): 
    """
    Allows access to users in the FundManager group or FundAdmin group.
    """
    def has_permission(self, request, view):
        return request.user and ( request.user.groups.filter(name='FundAdmin').exists() or request.user.groups.filter(name='FundManager').exists() )