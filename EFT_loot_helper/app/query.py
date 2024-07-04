QUERY_ITEMS = """
items (lang: ru) {
    id
    name
    shortName
    basePrice
    width
    height
    backgroundColor
    types
    updated
    image8xLink
    inspectImageLink
    lastLowPrice
    lastOfferCount
    fleaMarketFee
    sellFor {
        price
        currency
        priceRUB
        vendor {
            normalizedName
        }
    }
    buyFor {
        price
        currency
        priceRUB
        vendor {
            normalizedName
        }
    }
  }
"""

QUERY_TRADERS = """
  traders {
    name
    normalizedName
    imageLink
  }
"""

QUERY_BARTERS = """
barters (lang: ru) {
    id
    trader {
      id
      name
      normalizedName
    }
    level
    requiredItems {
      item {
        id
        shortName
      }
      count
      quantity
    }
    rewardItems {
      item {
        id
        shortName
      }
      count
      quantity
    }
    buyLimit
  }
"""

REQUEST_TO_TARKOV_API = """
query X {""" + QUERY_ITEMS + QUERY_TRADERS + QUERY_BARTERS +"""
}
"""