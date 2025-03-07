from research_paper_fetcher.pubmed_fetcher import fetch_paper_ids, fetch_paper_details
import argparse
import csv
from typing import List

def save_to_csv(filename: str, data: List[dict]) -> None:
    """Save research papers data to a CSV file."""
    try:
        # Include 'Corresponding Author Email' in the fieldnames
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"]

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Ensure each paper contains 'Corresponding Author Email'
            for paper in data:
                if 'Corresponding Author Email' not in paper:
                    paper['Corresponding Author Email'] = 'N/A'  # or some default value

            writer.writerows(data)
        print(f"Results saved to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main() -> None:
    """Command-line interface to fetch research papers from PubMed."""
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Save results to CSV file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    # Fetch paper IDs
    paper_ids = fetch_paper_ids(args.query, max_results=5)
    if not paper_ids:
        print("No papers found.")
        return

    # Fetch paper details
    papers = fetch_paper_details(paper_ids)

    # Print or save results
    if args.file:
        save_to_csv(args.file, papers)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
