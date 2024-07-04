from typing import Optional
from django.core.cache import cache


def get_cached_item_by_id(id: str) -> Optional[dict]:
    return cache.get("item__"+id)
    
def get_all_cached_items() -> Optional[dict]:
    return cache.get("items")

def get_barters() -> Optional[dict]:
    return cache.get("barters")


def get_tier_list(items: dict, amount_of_items: int) -> dict:
    data = {}

    for i in items:
        item_data = get_best_price_for_cell_of_item(i)
        if item_data is None:
            continue
        data["item_"+i["id"]] = item_data
    
    # сделать фильтр топ 250 предметов и раскидать их на 7 тиров
    # можно добавить параметр минимальной цены, чтобы брать предметы выше неё и также раскидывать на тиры
    # примерная формула:    цена_тира = (МАКС_цена - МИН_цена) / 7
    #                       уровень_i = МИН_цена + цена_тира * i
    # также можно добавить полученные данные в кэш, чтобы не считать их для каждого пользователя
    data = sorted(data.items(), key=lambda x:x[1]["bestCellPrice"]["cellPrice"], reverse=True)[:amount_of_items]
    data = set_tiers(data, amount_of_items)

    return data

def set_tiers(data: list, number_of_items: int) -> dict:
    tier_levels = {
        'S': None,
        'A': None,
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': None,
    }
    tier_gap = number_of_items // len(tier_levels)
    
    for i, val in enumerate(tier_levels):
        tier_levels[val] = {
            "max_cost": data[i*tier_gap][1]["bestCellPrice"]["cellPrice"],
            "min_cost": data[(i+1)*tier_gap-1][1]["bestCellPrice"]["cellPrice"],
            "items": dict(data[i*tier_gap:(i+1)*tier_gap]),
            }
    
    return tier_levels


def get_best_price_for_cell_of_item(item: dict) -> Optional[dict]:
    
    if item["bestTrader"] is None:
        return None
    
    item_cells = item["width"] * item["height"]
    best_price_for_cell = item["bestPrice"] // item_cells
    result_price = {
        "bestTrader": item["bestTrader"]["imageLink"],
        "bestPrice": item["bestPrice"],
        "cellPrice": best_price_for_cell
    }
    data = {
        'id': item["id"],
        'name': item['name'],
        'shortName': item['shortName'],
        'imageLink': item["image8xLink"],
        "bestCellPrice": result_price
    }
    return data

def get_barter_profit(barter: dict) -> dict:
    barter["trader"] = cache.get("trader__" + barter["trader"]["normalizedName"])
    price_for_required_items = 0
    price_for_reward_items = 0
    price_for_reward_items_buy = 0

    for i in barter["requiredItems"]:
        item = cache.get("item__" + i["item"]["id"])
        count = i["count"]
        i["item"]["bestBuyPrice"] = item["bestBuyPrice"]
        i["item"]["bestBuyTrader"] = item["bestBuyTrader"]

        price_for_required_items += item["bestBuyPrice"] * count

    for i in barter["rewardItems"]:
        item = cache.get("item__" + i["item"]["id"])
        count = i["count"]
        i["item"]["bestPrice"] = item["bestPrice"]
        i["item"]["bestTrader"] = item["bestTrader"]

        price_for_reward_items += item["bestPrice"] * count
        price_for_reward_items_buy += item["bestBuyPrice"] * count
    
    barter["buyPrice"] = price_for_required_items
    barter["sellPrice"] = price_for_reward_items
    
    barter["sellProfit"] = price_for_reward_items - price_for_required_items if price_for_required_items != 0 else None
    barter["buyProfit"] = price_for_reward_items_buy - price_for_required_items if price_for_required_items != 0 else None

    return barter