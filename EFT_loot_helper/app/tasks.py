from django.core.cache import cache
from django.conf import settings
from celery import shared_task
from math import inf
from time import sleep
import requests
import os

from .query import REQUEST_TO_TARKOV_API
# import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='myapp.log', level=logging.INFO)


@shared_task
def periodic_eft_api_query():

    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers,
                             json={'query': REQUEST_TO_TARKOV_API})
    
    if response.status_code != 200:
        # проверить, крашнется ли окончательно в периодической задаче,
        # если код ответа будет не 200
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, REQUEST_TO_TARKOV_API))
    
    data = response.json()["data"]

    _set_traders_in_cache(data["traders"])
    _set_barters_in_cache(data["barters"])
    _set_items_in_cache(data["items"])
    
    print("Cache has been refreshed.")


def _set_traders_in_cache(traders: list[dict]) -> None:
    for i in traders:
        name = i.pop("normalizedName")
        i["imageLink"] = f"pictures/traders/{name}.webp"
        cache.set("trader__" + name, i)
    cache.set("trader__flea-market",
              {"name": "Flea market", "imageLink": "pictures/traders/flea-market-portrait.webp"})
    
def _set_barters_in_cache(barters: list[dict]) -> None:
    for i in barters:
        id = i['id']
        cache.set("barter__" + id, i)
    cache.set("barters", barters)

def _set_items_in_cache(items: list[dict]) -> None:
    for i in items:
        id = i['id']

        bestPrice, bestTrader = _get_best_price_of_item(i["sellFor"])
        i["bestPrice"] = bestPrice
        i["bestTrader"] = bestTrader

        bestBuyPrice, bestBuyTrader = _get_min_buy_cost(i["buyFor"])
        i["bestBuyPrice"] = bestBuyPrice
        i["bestBuyTrader"] = bestBuyTrader

        cache.set("item__" + id, i)

    cache.set("items", items)


def _get_best_price_of_item(sellFor):

    if sellFor == []:
        return (0, None)

    best_trader = None
    price = 0

    for j in sellFor:

        if j["priceRUB"] == 0 or j["priceRUB"] <= price:
            continue
        else:
            price = j["priceRUB"]

        best_trader = j["vendor"]["normalizedName"]
    
    if best_trader is not None:
        best_trader = cache.get("trader__" + best_trader)
    
    return (price, best_trader)

def _get_min_buy_cost(buyFor):

    if buyFor == []:
        return (0, None)

    best_trader = None
    price = inf

    for j in buyFor:

        if j["priceRUB"] > price:
            continue
        else:
            price = j["priceRUB"]

        best_trader = j["vendor"]["normalizedName"]
    
    if best_trader is not None:
        best_trader = cache.get("trader__" + best_trader)
    
    return (price, best_trader)