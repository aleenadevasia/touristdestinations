from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # URLs for State model
    path('states/', StateCreateAPIView.as_view(), name='state-create'),
    path('states/<int:pk>/', StateRetrieveAPIView.as_view(), name='state-retrieve'),
    path('states/<int:pk>/update/', StateUpdateAPIView.as_view(), name='state-update'),
    path('states/<int:pk>/delete/', StateDestroyAPIView.as_view(), name='state-delete'),

    # URLs for District model
    # path('districts/', DistrictCreateAPIView.as_view(), name='district-create'),
    # path('districts/<int:pk>/', DistrictRetrieveAPIView.as_view(), name='district-retrieve'),
    # path('districts/<int:pk>/update/', DistrictUpdateAPIView.as_view(), name='district-update'),
    # path('districts/<int:pk>/delete/', DistrictDestroyAPIView.as_view(), name='district-delete'),

    # URLs for Category model
    path('categories/', CategoryCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category-retrieve'),
    path('categories/<int:pk>/update/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDestroyAPIView.as_view(), name='category-delete'),

    # URLs for TouristDestination model
    path('destinations/', TouristDestinationCreateAPIView.as_view(), name='destination-create'),
    path('destinations/<int:pk>/detail/', TouristDestinationRetrieveAPIView.as_view(), name='destination-retrieve'),
    path('destinations/<int:pk>/update/', TouristDestinationUpdateAPIView.as_view(), name='destination-update'),
    path('destinations/<int:pk>/delete/', TouristDestinationDestroyAPIView.as_view(), name='destination-delete'),

    path('search/<str:place_name>/',DestinationSearchViewSet.as_view(),name='search'),
    path('create_destination',views.create_tourist_destination,name='create_destination'),
    path('destination_fetch/<int:id>/',views.destination_fetch,name='destination_fetch'),
    path('destination_update/<int:id>/',views.update_destination,name='destination_update'),
    path('destination_delete/<int:id>/', views.destination_delete, name='destination_delete'),
    path('', views.index, name='index'),
    path('destination_detail/<int:id>/detail/', views.detail_destination, name='detail_destination'),
    path('destination_list/', views.destination_list, name='destination_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
