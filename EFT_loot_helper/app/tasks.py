from django.core.cache import cache
from django.conf import settings
from celery import shared_task
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
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': REQUEST_TO_TARKOV_API})
    
    if response.status_code != 200:
        # проверить, крашнется ли окончательно в периодической задаче,
        # если код ответа будет не 200
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, REQUEST_TO_TARKOV_API))
    
    data = response.json()["data"]

    items = data["items"]
    traders = data["traders"]

    for i in traders:
        i["name"] = i["name"].lower().replace(" ", "_")
        name = i.pop("name")
        if name == 'btr_driver':
            cache.set("trader_" + name, {'imageLink': os.path.join(settings.STATIC_URL, 'pictures/unknown-trader.webp')})
        else:
            cache.set("trader_" + name, i)
        # print(name, cache.get("trader_" + name))
    cache.set("trader_fleamarket", {'imageLink': os.path.join(settings.STATIC_URL, 'pictures/flea-market-portrait.webp')})

    cache.set("items", items)
    for i in items:
        id = i.pop("id")
        cache.set("item__" + id, i)
    
    print("Cache has been refreshed.")


# def basic_counter():
#     n = 1
#     while True:
#         yield n
#         n += 1

# simple_generator = basic_counter()
# @shared_task
# def my_periodic_task_setter():
#     cache.set("test_value", next(simple_generator))

# @shared_task
# def my_periodic_task_getter():
#     tv = cache.get("test_value")
#     print(f"Test value is {tv}")