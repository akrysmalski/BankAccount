from rest_framework.permissions import BasePermission



class IsSelf(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user and \
            not request.user.is_anonymous and \
            str(request.user.pk) == view.kwargs['pk']
        )



class IsSuperUser(BasePermission):

    def has_permission(self, request, *args, **kwargs):

        return bool(request.user and request.user.is_superuser)