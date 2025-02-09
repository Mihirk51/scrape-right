import argparse

from config.settings import REGION_MAPPING_LINKS
from database.models.tournaments import insert_events
from logger import logger
from scraper.events_scraper import EventScraper


def get_events_info(region_code):
    region = REGION_MAPPING_LINKS.get(region_code)
    if not region:
        logger.error(f"Invalid region code: {region_code}")
        return

    scraper = EventScraper(region)
    return scraper.get_all_events_main()


def main():
    parser = argparse.ArgumentParser(description="Event Information Scraper")
    subparsers = parser.add_subparsers(dest="command")

    get_events_parser = subparsers.add_parser(
        "get_events_info", help="Get event information for a specific region"
    )
    get_events_parser.add_argument(
        "region", type=str, help="Region code for scraping events"
    )

    args = parser.parse_args()

    if args.command == "get_events_info":
        logger.info(f"Fetching events info for region: {args.region}")
        events = get_events_info(args.region)
        # TODO: Save events to a file store before writing to database
        if events:
            insert_events(events)
            logger.info(f"Inserted {len(events)} events into the database")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
