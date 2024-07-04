from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.cache import cache_page
from .models import CachedItem
from .services import get_cached_item_by_id, get_all_cached_items, get_barter_profit, get_barters, get_tier_list


@api_view(('GET',))
@cache_page(60 * 5)
def default_view(request):
    data = get_all_cached_items()
    if data is None:
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(data={"data": data}, status=HTTP_200_OK)


class RetrieveItemView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        item = get_cached_item_by_id(id)
        if item is None:
            if CachedItem.objects.filter(itemId=id).exists():
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=HTTP_404_NOT_FOUND)
        else:
            return Response(data={"item": item}, status=HTTP_200_OK)


class GetRatingOfItemsView(APIView):
    permission_classes = [AllowAny]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'html/index.html'

    def get(self, request):
        items = get_all_cached_items()
        if items is None:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        items_value = 250

        data = get_tier_list(items, items_value)
        
        return Response(data={"data": data}, status=HTTP_200_OK)


class GetBarters(APIView):
    permission_classes = [AllowAny]

    def get(self, reuquest):
        barters = get_barters()
        if barters is None:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        for i in barters:
            i = get_barter_profit(i)

        return Response(data={"data": barters}, status=HTTP_200_OK)