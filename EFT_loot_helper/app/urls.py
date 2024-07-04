from django.urls import path
from .views import default_view, RetrieveItemView, GetRatingOfItemsView, GetBarters


urlpatterns = [
    path('', default_view, name='index'),
    path('item/<str:id>', RetrieveItemView.as_view(), name='retrieve_item'),
    path('rating/', GetRatingOfItemsView.as_view(), name="rating"),
    path('barters/', GetBarters.as_view(), name="barters"),
]