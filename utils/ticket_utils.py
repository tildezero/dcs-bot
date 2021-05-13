from replit import db

base_prices = {
   "1": db['price-1-completion'],
   "2": db['price-2-completion'],
   "3": db['price-3-completion'],
   "4": db['price-4-completion'],
   "5": db['price-5-completion'],
   "6": db['price-6-completion'],
   "7": db['price-7-completion']
}

s_price = {
  "5": db['price-5-s'],
  "6": db['price-6-s'],
  "7": db['price-7-s']
}

s_plus_price = {
  "5": db['price-5-s+'],
  "6": db['price-6-s+'],
  "7": db['price-7-s+']
}

bulk_base_prices = {
   "1": db['bulk-price-1-completion'],
   "2": db['bulk-price-2-completion'],
   "3": db['bulk-price-3-completion'],
   "4": db['bulk-price-4-completion'],
   "5": db['bulk-price-5-completion'],
   "6": db['bulk-price-6-completion'],
   "7": db['bulk-price-7-completion']
}

bulk_s_price = {
  "5": db['bulk-price-5-s'],
  "6": db['bulk-price-6-s'],
  "7": db['bulk-price-7-s']
}


async def give_price(floor: str, score: str, bulk: bool = False):
  if bulk:
    if floor == "1" or floor == "2" or floor == "3" or floor == "4":
      return f"{bulk_base_prices[floor]} (there is no s or s+ scores for the floor you requested)"
    else: 
      if score.lower() == "completion":
        return bulk_base_prices[floor]
      if score.lower() == "s":
        return bulk_s_price[floor]
      if score.lower() == "s+":
        if floor == "5":
          return db['bulk-price-5-s+']
        if floor == "6":
          return db['bulk-price-6-s+']
        if floor == "7":
          return db['bulk-price-7-s+']


  if floor == "1" or floor == "2" or floor == "3" or floor == "4":
    return f"{base_prices[floor]} (there is no s or s+ scores for the floor you requested)"
  else: 
    if score.lower() == "completion":
      return base_prices[floor]
    if score.lower() == "s":
      return s_price[floor]
    if score.lower() == "s+":
      return s_plus_price[floor]

      return s_plus_price[floor]


