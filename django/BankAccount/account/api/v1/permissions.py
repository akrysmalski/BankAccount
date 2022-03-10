from rest_framework.permissions import BasePermission



class IsSelf(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user and \
            not request.user.is_anonymous and \
            int(view.kwargs['pk']) in request.user.accounts
        )