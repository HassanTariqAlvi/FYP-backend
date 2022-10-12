from app.exceptions import DeletionFailed
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class AbstractBaseView(viewsets.ModelViewSet, object):
    model = None
    post_message = None
    put_message = None
    delete_message = None
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': self.post_message})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'status_code': status.HTTP_200_OK, 'message': self.put_message})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'status_code': status.HTTP_204_NO_CONTENT, 'message': self.delete_message})
        except:
            raise DeletionFailed(detail="Deletion failed. Please try again!")

    def perform_create(self, serializer):
        user = self.request.user
        self.model.objects.create(user, **serializer.validated_data)

    def perform_update(self, serializer):
        user = self.request.user
        id = serializer.data['id']
        self.model.objects.update(user, id, **serializer.validated_data)
