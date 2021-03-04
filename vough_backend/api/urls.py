from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from api import views
from api.routes import CustomRouter

# Personalização de Roteador para endpoints apenas de listagem, recuperação e exclusão
routers = CustomRouter()
routers.register("orgs", views.OrganizationViewSet)


urlpatterns = [
    # Rotas da documentação swagger-ui
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(), name='swagger-ui'),

    # rotas de listagem, recuperação e exclusão da API
    path('api/', include(routers.urls))
]
