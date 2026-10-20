"""Print the bidding state of every lot in live (or upcoming) Saudi property auctions.

    python auction_watch.py                      # live auctions, both seller planes
    python auction_watch.py --status auction-upcoming --seller au-infath

For each auction event: when it closes (counted from the API's serverTime, not your clock),
then per lot the starting bid, current high bid, the minimum increment at that price,
the deposit and the buyer commission.
"""

import argparse
from datetime import datetime, timedelta

from client import get, pages


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def increment_at(ladder, price):
    """The minimum bid step for the price band containing `price`."""
    for band in ladder or []:
        if band["from"] <= price <= band["to"]:
            return band["increment"]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", default="auction-live",
                        choices=["auction-live", "auction-upcoming", "auction-past"])
    parser.add_argument("--seller", default="all", choices=["all", "au-infath", "au-wasalt"])
    parser.add_argument("--city-id", type=int)
    parser.add_argument("--max-groups", type=int, default=3)
    parser.add_argument("--max-lots", type=int, default=5, help="lots read per event")
    args = parser.parse_args()

    groups = pages("/auction-search", "auctionGroups", status=args.status, seller=args.seller,
                   format="online", city_id=args.city_id)
    for count, group in enumerate(groups, start=1):
        server_now = parse_time(group["serverTime"])
        next_change = server_now + timedelta(milliseconds=group["millisRemaining"])
        kind = "Infath (judicial)" if group["sellerSlug"] == "au-infath" else "private brokerage"
        print(f"\n{group['name']}  [{kind}, {group['status']}]")
        print(f"  {group['lotCount']} lots, deposit {group['depositAmount']:,} SAR, "
              f"next state change {next_change:%Y-%m-%d %H:%M} UTC")

        lots = get("/auction-lots", group_id=group["groupId"])["lots"]
        for lot in lots[: args.max_lots]:
            detail = get("/auction-details", auction_id=lot["auctionId"])
            bidding = detail.get("bidding")
            if not bidding:
                print(f"  lot {lot['sequence']}: bidding panel unavailable {detail.get('partialErrors')}")
                continue
            if not bidding["startingBid"]:
                # Infath lots are often published before pricing is set: zeros, real deposit.
                print(f"  lot {lot['sequence']}: not priced yet, deposit {bidding['depositAmount']:,} SAR")
                continue
            current = max(bidding["highestBid"], bidding["startingBid"])
            step = increment_at(bidding["bidIncrementLadder"], current)
            unit = "SAR" if bidding["pricingUnit"] == "total-price" else f"SAR ({bidding['pricingUnit']})"
            step_text = f"{step:,}" if step else "n/a"
            extended = ", extended" if bidding.get("isExtended") else ""
            print(f"  lot {lot['sequence']}: start {bidding['startingBid']:,}, high {bidding['highestBid']:,} {unit}, "
                  f"step {step_text}, buyer commission {bidding['buyerCommissionPercent']}%, "
                  f"closes {bidding['endDate']}{extended}")
        if count >= args.max_groups:
            break


if __name__ == "__main__":
    main()
