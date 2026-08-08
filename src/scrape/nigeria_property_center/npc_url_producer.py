def npc_url_producer(listing_type : str, start : int, end : int):
    # listing type should either be for-rent or for-sale
    url = f"https://nigeriapropertycentre.com/{listing_type}/"
    return [f"{url}?page={i}&sort=2" for i in range(start, end + 1)]
    