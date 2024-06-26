REQUEST_TO_TARKOV_API = """
query X {
  items (lang: ru) {
    id
    name
    basePrice
    width
    height
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
        source
    }
    buyFor {
        price
        currency
        priceRUB
        source
    }
  }
  traders () {
    name
    imageLink
  }
}
"""
