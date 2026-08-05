from lxml import html

from src.extract.nigeria_property_center.rent_parser import parse_property


def test_parse_property_extracts_listing_fields():
    card_html = """
    <article class="group relative overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div class="flex">
        <div class="w-64">
          <img src="/images/example.jpg" alt="Apartment" />
        </div>
        <div class="flex-1 p-4">
          <p class="text-primary font-semibold">Flat / apartment for rent</p>
          <h3 class="text-xl font-bold">2 Bedroom Flat Apartment</h3>
          <div class="flex items-center gap-2 text-sm text-slate-600">
            <span>📍</span>
            <span>Victoria Island, Lagos</span>
          </div>
          <div class="flex gap-4">
            <span class="inline-flex items-center gap-1">2 Beds</span>
            <span class="inline-flex items-center gap-1">2 Baths</span>
            <span class="inline-flex items-center gap-1">1 Parking</span>
          </div>
          <div class="mt-2 flex items-end justify-between">
            <div>
              <span class="font-bold text-[1.5rem] text-slate-900">₦6,500,000</span>
              <span class="text-sm text-slate-500">/yr</span>
            </div>
            <a href="/for-rent/2-bedroom-flat-apartment-victoria-island-lagos">View listing</a>
          </div>
          <div class="border-t pt-2">
            <p>Verified Agent</p>
            <p>Luxury Homes Realty</p>
          </div>
        </div>
      </div>
    </article>
    """

    card = html.fromstring(card_html)
    parsed = parse_property(card)

    assert parsed is not None
    assert parsed["title"] == "2 Bedroom Flat Apartment"
    assert parsed["listing_type"] == "Flat / apartment for rent"
    assert parsed["address"] == "Victoria Island, Lagos"
    assert parsed["bedrooms"] == 2
    assert parsed["bathrooms"] == 2
    assert parsed["parking"] == 1
    assert parsed["currency"] == "₦"
    assert parsed["price_amount"] == 6500000
    assert parsed["price_period"] == "year"
    assert parsed["agent"] == "Luxury Homes Realty"
    assert parsed["link"] == "https://nigeriapropertycentre.com/for-rent/2-bedroom-flat-apartment-victoria-island-lagos"
