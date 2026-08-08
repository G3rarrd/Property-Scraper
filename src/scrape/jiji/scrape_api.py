import httpx




def scrape_api(url: str) :
    response = httpx.get(url)

    print(response.status_code)

    print(response.text)
    
    
if __name__ == "__main__":
    url = "https://jiji.ng/api_web/v1/listing?slug=houses-apartments-for-rent&init_page=true&page=10000&webp=false&lsmid=1786124665141"
    scrape_api(url)