import re

import chompjs

from locations.categories import Categories, apply_category
from locations.json_blob_spider import JSONBlobSpider


class SynlabFRSpider(JSONBlobSpider):
    name = "synlab_fr"
    item_attributes = {
        "brand": "Synlab",
        "brand_wikidata": "Q106847432",
    }
    start_urls = ["https://www.synlab.fr/trouver-un-laboratoire/"]

    def extract_json(self, response):
        return chompjs.parse_js_object(
            response.xpath('//script[contains(text(), "const villes = ")]/text()').get().split("const villes =")[1]
        )

    def post_process_item(self, item, response, location):
        apply_category(Categories.MEDICAL_LABORATORY, item)
        name = location.pop("nom", "").lower()

        if name.startswith("synlab"):
            item["branch"] = (
                (
                    name.removeprefix("synlab ")
                    .removeprefix("auvergne")
                    .removeprefix("biofrance")
                    .removeprefix("bioliance")
                    .removeprefix("bionyval")
                    .removeprefix("biopaj")
                    .removeprefix("bourgogne")
                    .removeprefix("carron")
                    .removeprefix("charentes")
                    .removeprefix("delaporte")
                    .removeprefix("hauts-de-france")
                    .removeprefix("midi")
                    .removeprefix("nord de france")
                    .removeprefix("normandie maine")
                    .removeprefix("normandie")
                    .removeprefix("nouvelle aquitaine")
                    .removeprefix("occitanie")
                    .removeprefix("oxabio")
                    .removeprefix("paris")
                    .removeprefix("provence")
                    .removeprefix("rhône-alpes")
                    .removeprefix("sud-ouest")
                    .removeprefix("normandie")
                    .removeprefix("normandie")
                )
                .strip(" -")
                .removeprefix("site")
            )
        elif name.startswith("laboratoire bioalliance"):
            item["branch"] = name.removeprefix("laboratoire bioalliance ").removeprefix("de ").removeprefix("d'")

        match = re.search(r"\b\d{5}\b", location.pop("adresse", ""))
        item["postcode"] = match.group() if match else None

        yield item
