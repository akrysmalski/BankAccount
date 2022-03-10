from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from base.models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import IsSelf, IsSuperUser



class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-create_date')

    serializer_class = UserSerializer

    action_permissions = {
        'list': (IsSuperUser, ), 
        'create': (IsSuperUser, ), 
        'destroy': (IsSuperUser, ), 
        'update': (IsSuperUser, ),
        'retrieve': (IsSelf, ), 
        'partial_update': (IsSelf, ), 
        'change_password': (IsSelf, )
    }


    def get_permissions(self):

        return [
            permission() for permission \
                in self.action_permissions.get(self.action, [IsAuthenticated])
        ]


    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):

        user = self.get_object()

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():

            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response(status=status.HTTP_200_OK)
            
            else:
                return Response(
                    {'detail': 'Wrong old password'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )