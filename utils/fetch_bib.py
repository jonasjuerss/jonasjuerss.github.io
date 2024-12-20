import argparse
import os

import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, default=os.environ.get("ZOTERO_USER", None),
                        help="The (numerical) Zotero API user ID.")
    parser.add_argument("--key", type=str, default=os.environ.get("ZOTERO_KEY", None),
                        help="The Zotero API key.")
    parser.add_argument("--page_size", type=int, default=100, help="The number of entries per page.")
    args = parser.parse_args()

    base_url = f"https://api.zotero.org/users/{args.user}/items?format=bibtex&limit={args.page_size}"
    headers = {"Zotero-API-Key": args.key, "Zotero-API-Version": "3"}

    total_results = 1
    page = 0
    with open(os.path.join("library.bib"), 'w+', encoding="utf-8") as file:
        while page * args.page_size <= total_results:
            res = requests.get(f"{base_url}&start={page}", headers=headers)
            res.raise_for_status()
            total_results = int(res.headers["Total-Results"])
            file.writelines(res.text + "\n")
            page += 1
            print(f"Loaded page {page}/{((total_results - 1) // args.page_size) + 1}")