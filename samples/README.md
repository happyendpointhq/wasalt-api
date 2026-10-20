# Sample responses

Example `200` responses for twelve Wasalt API endpoints, copied from the API's public
documentation. Long arrays are cut to their first two items, and personal names of brokers
and agents are removed. Field names and values are otherwise unchanged, including the Arabic
text.

| File | Request |
|---|---|
| `cities.json` | `GET /cities` |
| `neighbourhoods.json` | `GET /neighbourhoods?city_id=273` |
| `search-properties.json` | `GET /search-properties?city_id=273` |
| `property-details.json` | `GET /property-details?property_id=5891941` |
| `property-map-card.json` | `GET /property-map-card?property_id=5891941` |
| `search-rentals.json` | `GET /search-rentals` |
| `rental-details.json` | `GET /rental-details?rental_id=6398` |
| `projects.json` | `GET /projects?city_id=273&zone_id=1` |
| `project-units.json` | `GET /project-units?project_id=100577` |
| `auction-search.json` | `GET /auction-search` |
| `auction-lots.json` | `GET /auction-lots?group_id=1012` |
| `auction-details.json` | `GET /auction-details?auction_id=4734` |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
