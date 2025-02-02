import argparse
from scraper.events_scraper import EventScraper
from config.settings import REGION_MAPPING_LINKS
from logger import logger  # Import the logger


def get_events_info(region_code):
    region = REGION_MAPPING_LINKS.get(region_code)
    if not region:
        logger.error(f"Invalid region code: {region_code}")
        return

    scraper = EventScraper(region)
    scraper.get_all_events_main()


def main():
    parser = argparse.ArgumentParser(description='Event Information Scraper')
    subparsers = parser.add_subparsers(dest='command')

    get_events_parser = subparsers.add_parser('get_events_info', help='Get event information for a specific region')
    get_events_parser.add_argument('region', type=str, help='Region code for scraping events')

    args = parser.parse_args()

    if args.command == 'get_events_info':
        logger.info(f"Fetching events info for region: {args.region}")
        get_events_info(args.region)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
