from urllib.parse import urlparse, parse_qs

def get_page_number(url : str)-> int | None: 
    params = urlparse(url)
    page = parse_qs(params.query).get("page")
    return int(page[0]) if page else None