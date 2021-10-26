from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from home.api.v1.serializers import SignupSerializer, PostModelSerializer, PostLikeSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import IsAuthenticated

from home.models import Post

User = get_user_model()


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    permission_classes = [AllowAny, ]
    http_allow_methods = ['POST']

    def create(self, request):
        context = {
            "non_field_errors": [
                _('Unable to log in with provided credentials.')
            ]
        }
        email = request.data.get('email')
        password = request.data.get('password')
        kwargs = {'email': email}
        try:
            user = User.objects.get(**kwargs)
            if not user.is_active:
                return Response({'error': 'User is not activate'}, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.pk,
                        'email': user.email,
                        'name': user.name,
                        'is_active': user.is_active
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist as e:
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class PostModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return Post.objects.filter(post_owner=self.request.user)

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'], post_owner=self.request.user)

    @action(detail=False, methods=['GET'])
    def like(self, request):
        try:
            serializer = PostLikeSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            post = Post.objects.get(id=serializer.validated_data['post_id'])
            post.like_count = post.like_count + 1
            post.save()
            return Response({'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


