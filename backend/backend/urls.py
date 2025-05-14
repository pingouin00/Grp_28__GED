from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Document_Management.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("Document_Management/user/register/", CreateUserView.as_view(), name="register"),
    path("Document_Management/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("Document_Management/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("Document_Management-auth/", include("rest_framework.urls")),
    path("Document_Management/", include("Document_Management.urls")),
]

# configuration pour servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

