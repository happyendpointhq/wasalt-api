"""Pick a city, search REGA-licensed apartments for sale, then open the first listing.

    python quickstart.py
"""

from client import get

# 1. City and zone ids. Search filters take ids, not names.
cities = get("/cities")
riyadh = next(c for c in cities if c["name"] == "Riyadh")
print(f"{riyadh['name']} ({riyadh['nameAr']}), id {riyadh['id']}, {riyadh['propertyCount']:,} listings")
for zone in riyadh["zones"]:
    print(f"  zone {zone['id']}: {zone['name']} ({zone['propertyCount']:,})")

# 2. Three- or four-bedroom apartments for sale, licensed listings only.
#    bedrooms is an exact set: "3,4" means 3 or 4, not "3 or more".
results = get(
    "/search-properties",
    city_id=riyadh["id"],
    property_for="sale",
    category="apartment",
    bedrooms="3,4",
    rega_verified="true",
)
print(f"\nAbout {results['estimatedCount']:,} matches (an estimate), first page:")
for row in results["listings"]:
    per_sqm = row["price"] / row["builtUpAreaSqm"] if row.get("builtUpAreaSqm") else None
    rate = f"{per_sqm:,.0f} SAR/m2" if per_sqm else "no area"
    print(f"{row['price']:>12,} SAR  {row.get('bedrooms')} bd  {rate:>14}  {row['district']}  (id {row['id']})")

# 3. The full record: description, extra facts (plan and land number) and the REGA licence block.
if results["listings"]:
    listing = get("/property-details", property_id=results["listings"][0]["id"])
    print(f"\n{listing['title']}")
    print(f"Viewed {listing['viewCount']} times in {listing['viewWindowDays']} days")
    for fact in listing.get("additionalAttributes") or []:
        print(f"  {fact['key']}: {fact['value']}")
    # The REGA block is a list of sections. Print the licence and the property specs; skip the
    # section naming the person responsible for the ad. Some sections (property_borders) nest
    # their fields under "groups" instead of "fields".
    for block in listing.get("regaLicence") or []:
        if block["key"] not in ("rega_information", "property_specs"):
            continue
        for field in block.get("fields") or []:
            print(f"  REGA {field['key']}: {field['value']}")
