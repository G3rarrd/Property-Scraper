import traceback
from typing import Optional


def first(items: list, default=None):
    return items[0] if items else default


def text(node, query: str) -> Optional[str]:
    result = node.xpath(query)
    return result[0].strip() if result else None


def texts(node, query: str) -> list[str]:
    return [t.strip() for t in node.xpath(query) if t and t.strip()]


def attribute(node, query: str) -> Optional[str]:
    return first(node.xpath(query))


def children(node, query: str):
    return node.xpath(query)

def extract_agent_name(property_card):
    #
    agent_name = property_card.xpath(
        'normalize-space(.//p[contains(@class,"text-foreground-strong")])'
    )

    if not agent_name:
        agent_name = property_card.xpath(
            'normalize-space(.//use[@href="#i-building-2"]/ancestor::svg/following-sibling::text()[1])'
        )

    return agent_name

def extract_listing_badge(property_card):
    listing_badge = property_card.xpath(
    'normalize-space(.//span[contains(@class,"bg-accent-bg")])'
    )

    if not listing_badge:
        listing_badge = property_card.xpath(
            'normalize-space(.//span[.//use[@href="#i-gem"]])'
        )
    return listing_badge

def parse_property(property_card) -> dict | None:
    try:
        link = attribute(property_card, ".//a[@aria-label]/@href")
        full_link = (
            f"https://nigeriapropertycentre.com{link}"
            if link else None
        )

        title = text(
            property_card,
            ".//h3/text()"
        )

        listing_type = text(
            property_card,
            ".//p[contains(@class,'text-primary')]/text()"
        )
        
        listing_badge = extract_listing_badge(property_card)

        thumbnail = attribute(
            property_card,
            ".//img/@src"
        )

        price = text(
            property_card,
            './/span[contains(@class,"font-bold") and contains(@class,"tabular-nums")]/text()'
        )

        period = text(
            property_card,
            './/span[contains(@class,"text-sm") and contains(@class,"font-semibold")][starts-with(normalize-space(), "/")]/text()'
        )

        address = property_card.xpath(
            'normalize-space(.//svg[use[@href="#i-map-pin"]]/following-sibling::span[1])'
        )

        if not address:
            address = property_card.xpath(
                'normalize-space(.//svg[use[@href="#i-map-pin"]]/following-sibling::text()[1])'
            )

        description = property_card.xpath(
            'normalize-space(.//p[contains(@class,"text-foreground-muted")])'
        )

        features_node = property_card.xpath(
            './/div[contains(@class,"gap-x-4")]//span[contains(@class,"inline-flex")]'
        )
        
        features = [
            " ".join(node.text_content().split())
            for node in features_node
        ]


        agent_name = extract_agent_name(property_card)
            

        return {
            "title": title,
            "listing_type": listing_type,
            "listing_badge": listing_badge,
            "price": price,
            "period": period,
            "address": address,
            "description": description,
            "thumbnail": thumbnail,
            "link": full_link,
            "agent_name": agent_name,
            "features": features,
        }

    except Exception as e:
        print(f"Error parsing property: {e}")
        traceback.print_exc()
        return None