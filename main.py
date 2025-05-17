# main.py

import argparse
import os
from scrapers.instagram import InstagramScraper
from scrapers.generic import GenericScraper

def main():
    parser = argparse.ArgumentParser(description="Universal Web Scraper")
    sub = parser.add_subparsers(dest="command")

    ig = sub.add_parser("instagram", help="Scrape Instagram profile")
    ig.add_argument("username", help="Instagram username")

    gen = sub.add_parser("generic", help="Scrape a general website")
    gen.add_argument("url", help="Website URL")

    args = parser.parse_args()

    if args.command == "instagram":
        username = args.username
        scr = InstagramScraper()

        # Scrape profile and links
        scr.scrape_profile(username)
        scr.scrape_media_links(username)

        # Construct the path to the generated CSV
        csv_path = os.path.join("downloads", "instagram", "instagram", username, "text", "all_links.csv")

        # Download media based on category from generated CSV
        scr.download_media_by_category_from_csv(username, csv_path, {
            "post": 2,
            "reel": 2,
            "tagged": 0
        })

        scr.close()

    elif args.command == "generic":
        gen_scr = GenericScraper()
        gen_scr.scrape(args.url)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
