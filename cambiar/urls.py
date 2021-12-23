from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import(
    PostDeleteView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    UserCreateView,
    like
)

urlpatterns = [
    path('signup', UserCreateView.as_view(template_name="usuarios/usuario_signup.html"), name='signup'),
    path('login', auth.LoginView.as_view(template_name="usuarios/usuario_login.html", redirect_authenticated_user=False), name='login'),
    path('logout', auth.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('accounts', include('allauth.urls')),
    path('', PostListView.as_view(),name='list'),
    path('post/create/', PostCreateView.as_view(),name='create'),
    path('post/<slug>', PostDetailView.as_view(),name='detail'),
    path('post/<slug>/update', PostUpdateView.as_view(),name='update'),
    path('post/<slug>/delete', PostDeleteView.as_view(),name='delete'),
    path('like/<slug>/', like, name='like')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)