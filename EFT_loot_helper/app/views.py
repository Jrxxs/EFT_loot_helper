from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings


@api_view(('GET',))
@cache_page(60 * 5)
def default_view(request):
    # items_keys = cache.key_prefix
    data = cache.get("items", None)
    return Response(data={"data": data}, status=HTTP_200_OK)


class RetrieveItemView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        item = cache.get("item__"+id)
        print(settings.BASE_DIR)
        print(settings.STATIC_ROOT)
        return Response(data={"item": item}, status=HTTP_200_OK)


class GetRatingOfItemsView(APIView):
    permission_classes = [AllowAny]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'html/index.html'

    def get(self, request):
        items = cache.get("items")
        data = {}
        traders = {}

        def get_best_price_for_cell_of_item(sellFor, item_cells, traders):
            best_price_for_cell = 0
            best_trader = None
            price = 0

            for j in sellFor:
                
                cellPrice = j["priceRUB"] // item_cells

                if cellPrice == 0 or cellPrice <= best_price_for_cell:
                    continue
                else:
                    best_price_for_cell = cellPrice
                    price = j["priceRUB"]

                trader_name = j["source"].replace(" ", "_").lower()

                if ("trader_" + trader_name) not in traders:
                    cached_trader = cache.get("trader_" + trader_name)
                    traders["trader_" + trader_name] = cached_trader

                best_trader = traders["trader_" + trader_name]
            
            return (price, best_price_for_cell, best_trader, traders)

        def set_tiers(data: list) -> dict:
            tier_levels = {
                'S': None,
                'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None,
            }
            tier_gap = items_value // len(tier_levels)
            
            for i, val in enumerate(tier_levels):
                tier_levels[val] = {
                    "max_cost": data[i*tier_gap][1]["bestCellPrice"]["cellPrice"],
                    "min_cost": data[(i+1)*tier_gap][1]["bestCellPrice"]["cellPrice"],
                    "items": dict(data[i*tier_gap:(i+1)*tier_gap]),
                    }
            
            return tier_levels

        for i in items:

            if i["sellFor"] == []:
                continue

            item_cells = i["width"] * i["height"]
            sellFor = i["sellFor"]
            price, best_price_for_cell, best_trader, traders = get_best_price_for_cell_of_item(
                                                                    sellFor, item_cells, traders)
            
            if best_trader is None:
                continue

            result_price = {"bestTrader": best_trader["imageLink"], "price": price, "cellPrice": best_price_for_cell}
            data["item_"+i["id"]] = {'name': i['name'],'imageLink': i["image8xLink"], "bestCellPrice": result_price}
        
        items_value = 250
        data = sorted(data.items(), key=lambda x:x[1]["bestCellPrice"]["cellPrice"], reverse=True)[:items_value]

        data = set_tiers(data)
        # сделать фильтр топ 250 предметов и раскидать их на 7 тиров
        # можно добавить параметр минимальной цены, чтобы брать предметы выше неё и также раскидывать на тиры
        # примерная формула:    цена_тира = (МАКС_цена - МИН_цена) / 7
        #                       уровень_i = МИН_цена + цена_тира * i
        # также можно добавить полученные данные в кэш, чтобы не считать их для каждого пользователя
        return Response(data={"data": data}, status=HTTP_200_OK)