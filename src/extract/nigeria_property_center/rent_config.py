from dataclasses import dataclass

@dataclass(frozen=False)
class RentField:
    title: str
    listing_type: str
    listing_badge: str
    price: float
    period: str
    address: str
    description: str
    thumbnail: str
    full_link: str
    agent_name: str
    features: list
        