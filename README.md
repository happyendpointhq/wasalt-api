# Wasalt API and Scraper

The Wasalt API returns Saudi Arabia real estate data from Wasalt as JSON: sale and
long-term rent listings with their REGA advertising licence, short-term holiday rentals with
nightly rate calendars, off-plan developer projects with their unit mix, and judicial (Infath)
and private property auctions down to the live bid. Wasalt publishes no public developer
API, so this REST API is the way to get its data into your own code without building and
maintaining a Wasalt scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/wasalt-api?utm_source=github&utm_medium=readme&utm_campaign=wasalt-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/wasalt-saudi-data
- Product page: https://happyendpoint.com/library/wasalt-api?utm_source=github&utm_medium=readme&utm_campaign=wasalt-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://wasalt-saudi-data.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 26, all `GET` |
| Coverage | Saudi Arabia: Riyadh, Jeddah, Makkah, Madinah and the national city register |
| Property types | Apartments, villas and townhouses, floors, land, buildings, towers, rest houses, offices, showrooms, warehouses |
| Currency and units | Saudi riyals (SAR), square metres |
| Language | Arabic listing text and place names, with English names and slugs on the reference endpoints |
| Format | JSON, every response wrapped in `{"success": true, "data": ...}` |

---

## What data you get

**Sale and long-term rent listings**
- Search with 17 filters: city, zone, district, several neighbourhoods at once, price, built-up area, bedrooms, bathrooms, parking, property age band and REGA licence status
- Run a search straight from a Wasalt search URL, with the parsed filters echoed back
- Price, built-up area, bedrooms, coordinates with an approximate-location flag, photos, timestamps
- REGA advertising licence on every row; the full licence block (issue and expiry dates, verification link) on the detail record
- Plan number and land number, street facing and width, view count over a stated window, broker capacity and licence

**Short-term holiday rentals** (a separate inventory with its own ids)
- Nightly price with and without the platform fee, guest cap, minimum stay, amenities in English and Arabic
- Forward nightly rate calendar, arrival guide, house rules, cancellation policy, REGA and tourism licence numbers

**Off-plan projects**
- Developer projects with sale price bands, units total and available, area range and construction labels
- Price, plot area and availability per unit inside a project

**Property auctions**
- Judicial (Infath, Ministry of Justice enforcement sales) and private brokerage events, by status, format and city
- Every lot in an event, then one lot's bidding state: starting bid, high bid, increment ladder, deposit, registration window, buyer commission, whether the close was extended
- Public activity feed of bids, alerts and followers; cities ranked by auctions hosted

**Reference data**
- Markets and cities with live listing counts and zones, the full city register, districts with map pins
- The five busiest neighbourhoods of a city with median price per m2
- Property type and auction vocabularies with stable ids

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/wasalt-saudi-data). Your API key is shown in the endpoint playground there. Copy `.env.example` to `.env` and paste it in.

### 2. Make a request

Filters take numeric ids (Riyadh is `273`, Jeddah `274`). Get them from `/cities`, then search:

```bash
curl "https://wasalt-saudi-data.p.rapidapi.com/cities" \
  -H "x-rapidapi-host: wasalt-saudi-data.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://wasalt-saudi-data.p.rapidapi.com/search-properties?city_id=273&property_for=sale&bedrooms=3,4&rega_verified=true" \
  -H "x-rapidapi-host: wasalt-saudi-data.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py
```

```python
from client import get, pages

results = get("/search-properties", city_id=273, property_for="sale", bedrooms="3,4")
for row in results["listings"]:
    print(row["price"], row["builtUpAreaSqm"], row["district"], row["regaLicenceNumber"])

# Every listing in a slice, page by page until hasMore is false:
for row in pages("/search-properties", "listings", city_id=274, property_for="rent"):
    ...
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs
```

---

## Example response

One row from `GET /search-properties?city_id=273`, trimmed. Values are the example in the
API's public documentation. The full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "estimatedCount": 20189,
    "page": 1,
    "pageSize": 16,
    "returned": 12,
    "hasMore": true,
    "listings": [
      {
        "id": 5891941,
        "propertyFor": "sale",
        "category": "apartment",
        "price": 770000,
        "currency": "ر.س",
        "cityId": 273,
        "districtId": 2170,
        "coordinates": { "lat": 24.6205598, "lng": 46.5086854 },
        "isApproximateLocation": true,
        "builtUpAreaSqm": 127.38,
        "bedrooms": 4,
        "isRegaLicensed": true,
        "regaLicenceNumber": "209840",
        "regaFullReference": "495464-SAU-BU-209840",
        "publishedAt": "2026-08-16T22:29:26.795Z"
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://wasalt-saudi-data.p.rapidapi.com`

### Sale and long-term rent

| Endpoint | Returns |
|---|---|
| `GET /search-properties` | Listings with the full filter set, 16 per page |
| `GET /search-properties-by-url` | The results of a pasted Wasalt search URL, with the filters it parsed |
| `GET /property-details` | One listing: description, extra facts, REGA licence block, view count |
| `GET /property-details-by-url` | The listing id and identity behind a Wasalt property URL |
| `GET /property-map-card` | The map pin payload, photo gallery, amenities and rent frequency |

### Short-term rentals

| Endpoint | Returns |
|---|---|
| `GET /search-rentals` | Holiday rentals by city, nightly price, area and bedrooms, 10 per page |
| `GET /rental-details` | One rental: nightly rate calendar, amenities, arrival guide, house rules |
| `GET /nationalities` | The guest nationality list the booking flow uses |

### Off-plan projects

| Endpoint | Returns |
|---|---|
| `GET /projects` | Developer projects with price bands and availability |
| `GET /project-details` | One project: description, attributes, developer, gallery |
| `GET /project-units` | Price, size and availability per unit inside one project |

### Auctions

| Endpoint | Returns |
|---|---|
| `GET /auction-search` | Auction events by seller (Infath or private), status, format and city |
| `GET /auction-lots` | Every lot in one event, with the lot ids |
| `GET /auction-group-details-by-url` | The event id behind a Wasalt auction URL |
| `GET /auction-details` | One lot with its bidding state |
| `GET /auction-activity` | Public feed of bids, alerts and followers for an event or a lot |
| `GET /auction-locations` | Cities hosting auctions, ranked by count |
| `GET /auction-statuses` | Auction lifecycle values for a city |
| `GET /auction-taxonomy` | Auction status and seller vocabularies with ids |

### Reference data

| Endpoint | Returns |
|---|---|
| `GET /markets` | Markets with inventory, split by zone |
| `GET /cities` | Cities with live listing counts and their zones |
| `GET /city-list` | The full Saudi city register, including cities with no listings |
| `GET /districts` | Every district of a city with a map pin |
| `GET /neighbourhoods` | The five busiest neighbourhoods of a city with median price per m2 |
| `GET /taxonomy` | Property type and requirement vocabularies |
| `GET /status` | Service health |

---

## Things to know about the data

These are taken from the API's documentation and its example responses. Most of them produce
wrong numbers or missing rows rather than errors.

- **Leaving out `property_type` does not mean "both".** It returns the residential plane
  only. Offices, showrooms, warehouses and commercial land come back only with
  `property_type=commercial`, so a full sweep is two searches.
- **`bedrooms`, `bathrooms` and `parking` are exact sets, not minimums.** `bedrooms=3` is
  exactly three. For "three or more", send `3,4,5,6`.
- **For rent listings, `price` is the annual rent.** The price filters on `/search-properties`
  are in whole riyals: the asking price for sale, the yearly rent for `property_for=rent`.
  Holiday rentals on `/search-rentals` are priced per night.
- **Do not page against `estimatedCount`.** On `/search-properties` it over-reports on narrow
  slices, and `category` filters each page without narrowing the count, so a page can come
  back short (the documented example has `pageSize: 16`, `returned: 12`) while later pages
  still match. Page until `hasMore` is false; `client.pages()` does this. On `/auction-search`
  the count is exact.
- **Page sizes are fixed per endpoint:** 16 for listings, 10 for rentals and auction events,
  25 for auction lots. There is no page size parameter.
- **The currency field is Arabic.** Listing rows carry `"currency": "ر.س"` (the riyal sign),
  while `/neighbourhoods` says `"SAR"`. Treat both as SAR.
- **Place names on listings are Arabic.** `city` and `district` come back as `الرياض` and
  `ظهرة لبن`. Join on `cityId` and `districtId`, and take English names from `/cities` (which
  has `name` and `nameAr`) or the English slugs on `/districts`.
- **Coordinates can be approximate.** Check `isApproximateLocation` before plotting a pin as
  the exact building.
- **REGA data comes at two levels, with two different numbers.** Search rows have
  `isRegaLicensed` and `regaLicenceNumber`, and some also carry `regaFullReference` (it was
  missing on the live row we checked, so read it with `.get()`). `/property-details` adds a
  `regaLicence` list of sections with Arabic labels and stable English keys: the
  `rega_information` section holds `adLicenseNumber`, `status`, `creationDate`, `endDate`
  and `adLicenseUrl` (REGA's own verification page). The two numbers differ (live: row
  `647107`, detail `adLicenseNumber` `7100328762`), so store both. Most sections list
  `fields`, but `property_borders` nests them under `groups`. One section names the
  employee responsible for the ad; `quickstart.py` skips it.
  `rega_verified=false` is a real filter: it returns the unlicensed remainder.
- **`/property-details` returns no photos or amenities.** Those fields come back empty on that
  route whatever the listing has. Call `/property-map-card` for the gallery, amenities and
  `rentFrequency`.
- **Property age stops at 10 years.** `age_bands` has only `0_1`, `1_5` and `5_10`. Older
  buildings match no band, so leave the filter off to include them.
- **Holiday rentals are a separate inventory.** Rental ids do not work on `/property-details`
  and listing ids do not work on `/rental-details`. `nightlyPrice` is the host's rate and
  `nightlyPriceWithFee` what the guest pays. The headline rate is not the whole story: the
  documented studio lists at 350 SAR a night, while its calendar shows 320 SAR for 13 and
  14 August and 270 SAR for the 15th, so price stays from `nightlyRateCalendar`. Rental photos come back as bare
  `imageFileNames`, not URLs.
- **Neighbourhood medians: Riyadh only, top five only.** `/neighbourhoods` returns a city's
  five busiest areas, not all of them (use `/districts` for the full list). The documentation
  warns that outside Riyadh most `medianPricePerSqm` values are whole-property prices, not per
  m2. Check `medianPricePerSqm` times `medianBuiltUpAreaSqm` before comparing cities.
- **Auctions are two levels: events and lots.** `/auction-search` returns events
  (`groupId`); `/auction-lots` turns an event into lot ids (`auctionId`); `/auction-details`
  takes a lot id, and a group id there is a 404.
- **Infath lots are often published before they are priced.** An upcoming lot can show
  `startingBid`, `highestBid` and `reservePrice` as `0` with a zero increment ladder while
  the deposit and registration window are already real. Poll again nearer the start.
- **Count down from `serverTime`, not your clock.** Each auction event has `millisRemaining`
  measured against the `serverTime` in the same response. `isExtended` shows when late
  bidding pushed the close out.
- **The increment depends on the price.** `bidIncrementLadder` gives the minimum step per
  price band; `pricingUnit` says whether bids are a total price or a rate per square metre.
  The cost of winning is the hammer price plus `buyerCommissionPercent` and VAT.
- **`sellerSlug` is not the value you filter with.** Filter with `seller=all`, `au-infath`
  or `au-wasalt`; private events report `sellerSlug: "au-wasalt-group"`, and sending that back
  is a 400. Split results on `sellerSlug`, never on the display field `seller`.
- **Offline auctions carry no bidding panel.** `format=offline` events are a catalogue of a
  physical sale; only `online` lots have starting bids, ladders and deposits.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | City ids and zones, a licensed apartment search with price per m2, one full record with its REGA block |
| [`examples/python/export_listings.py`](examples/python/export_listings.py) | Pages a search to CSV with REGA licence status, price per m2 and both planes (`--commercial`) |
| [`examples/python/auction_watch.py`](examples/python/auction_watch.py) | Live or upcoming Infath and private auctions: closing time, high bid, next increment, deposit, commission per lot |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | City lookup and a search in Node 18+, no dependencies |
| [`samples/`](samples/) | Documented example responses for twelve endpoints |

---

## API or your own Wasalt scraper

A Wasalt scraper has to handle Arabic page text, a separate auction site, three different
inventories with their own ids, and a site that changes without notice. This API returns all
of it as documented JSON with stable field names, so the code you keep is your analysis,
not a parser. For a one-off export or a recurring file of Saudi listings or auction results
instead of API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=wasalt-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Saudi listings
and auctions without code:

```json
{
  "mcpServers": {
    "wasalt": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: wasalt-saudi-data.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Wasalt API?

Wasalt does not publish a public developer API for its listings or auctions. This API, built
and maintained by Happy Endpoint and independent of Wasalt, provides that access as REST and
JSON.

### Where is the Wasalt API documentation?

Every endpoint, parameter and response is documented on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/wasalt-saudi-data). The endpoint
tables above summarise them, and [`samples/`](samples/) has example responses.

### How do I get a Wasalt API key?

Subscribe to the API on RapidAPI. Your key appears in the playground, and every request sends
it in the `x-rapidapi-key` header. There is a free plan, and every endpoint can be tried on it.

### Can I scrape Wasalt data for all of Saudi Arabia?

Yes. Leave out `city_id` to search every city, or walk city by city with `/cities` and
`/city-list`. For large slices, narrow by `city_id`, then `zone_id`, then
`neighbourhood_ids`, and page each slice until `hasMore` is false. Run residential and
commercial as two searches.

### Can I get Infath auction data?

Yes. `/auction-search?seller=au-infath` returns the Ministry of Justice enforcement auctions,
`/auction-lots` lists their lots, and `/auction-details` gives each lot's starting bid, high
bid, deposit and increment ladder. [`auction_watch.py`](examples/python/auction_watch.py)
walks all three.

### Can I check whether a listing has a REGA licence?

Yes. Every search row carries `isRegaLicensed` and `regaLicenceNumber` (and often `regaFullReference`),
and `rega_verified=true` or `false` filters on it. `/property-details` adds the licence
block with its issue and expiry dates.

### Do you cover other Saudi and Gulf sites?

Yes. Aqar for Saudi property, Ninja, HungerStation and Motory in Saudi Arabia, and Bayut and
PropertyFinder in the UAE. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=wasalt-api).

---

## Related repos

- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Aqar, the other big Saudi property portal: listings, district prices and developer projects
- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [uae-real-estate-data-guide](https://github.com/happyendpointhq/uae-real-estate-data-guide) - accessing Gulf property data next door in the UAE
- [bayut-api](https://github.com/happyendpointhq/bayut-api) - Bayut UAE listings, agents, transactions and off-plan projects

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
