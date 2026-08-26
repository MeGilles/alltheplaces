from typing import Iterable

from locations.categories import Categories, apply_category
from locations.items import Feature
from locations.storefinders.stockist import StockistSpider
from locations.hours import OpeningHours, DELIMITERS_FR, DAYS_FR
import re


class GoldUnionFRSpider(StockistSpider):
    name : str = "gold_union_fr"
    item_attributes : set = {"brand": "Gold Union", "brand_wikidata": "Q131622916"}
    key : str = "u20465"

    def parse_item(self, item: Feature, location: dict) -> Iterable[Feature]:
        item["branch"] = item.pop("name")
        
        item["opening_hours"] = OpeningHours()
        for custom_fields in (location.get("custom_fields") or []):
            opening = (custom_fields.get("name") or "").strip().lower()
            if opening == "ouverture":
                opening_hours = (custom_fields.get("value") or "").strip()                
                opening_hours = re.sub(r"(\d{1,2})h(\d{2})", r"\1:\2", opening_hours)
                item["opening_hours"].add_ranges_from_string(opening_hours, DAYS_FR, delimiters=DELIMITERS_FR)

        apply_category(Categories.SHOP_GOLD_BUYER, item)
        yield item
