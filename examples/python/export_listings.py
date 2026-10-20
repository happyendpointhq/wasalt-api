"""Export a Wasalt search to CSV, with REGA licence status on every row.

    python export_listings.py --city-id 273 --property-for rent --out riyadh-rent.csv
    python export_listings.py --city-id 274 --commercial --out jeddah-commercial.csv

Residential and commercial are separate planes: leaving out property_type returns residential
only, so run once with --commercial to cover offices, showrooms and warehouses.
For rent listings, price is the annual rent in SAR.
"""

import argparse
import csv

from client import pages

COLUMNS = [
    "id", "propertyFor", "category", "price", "builtUpAreaSqm", "price_per_sqm", "bedrooms",
    "cityId", "districtId", "district", "lat", "lng", "isApproximateLocation",
    "isRegaLicensed", "regaLicenceNumber", "regaFullReference", "broker_capacity",
    "publishedAt",
]


def flatten(row):
    area = row.get("builtUpAreaSqm")
    coords = row.get("coordinates") or {}
    return {
        **{k: row.get(k) for k in COLUMNS if k in row},
        "price_per_sqm": round(row["price"] / area) if area and row.get("price") else None,
        "lat": coords.get("lat"),
        "lng": coords.get("lng"),
        "broker_capacity": (row.get("owner") or {}).get("capacity"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city-id", type=int, help="from /cities, for example 273 (Riyadh)")
    parser.add_argument("--property-for", choices=["sale", "rent"])
    parser.add_argument("--commercial", action="store_true", help="search the commercial plane")
    parser.add_argument("--unlicensed", action="store_true", help="only listings without a REGA licence")
    parser.add_argument("--max-pages", type=int, default=50, help="16 listings per page")
    parser.add_argument("--out", default="wasalt-listings.csv")
    args = parser.parse_args()

    rows = pages(
        "/search-properties",
        "listings",
        max_pages=args.max_pages,
        city_id=args.city_id,
        property_for=args.property_for,
        property_type="commercial" if args.commercial else None,
        rega_verified="false" if args.unlicensed else None,
    )
    written = 0
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(flatten(row))
            written += 1
    print(f"Wrote {written} listings to {args.out}")


if __name__ == "__main__":
    main()
