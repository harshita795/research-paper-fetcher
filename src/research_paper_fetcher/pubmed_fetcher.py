import requests
import xml.etree.ElementTree as ET
import re  # Import regular expressions module
from typing import List, Dict, Optional

# API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to identify company-affiliated authors
COMPANY_KEYWORDS = ["Inc.", "Ltd.", "Pharma", "Biotech", "Corporation", "GmbH"]
UNIVERSITY_KEYWORDS = ["University", "Institute", "College", "Research Center", "Hospital"]

def is_company_affiliation(affiliation: Optional[str]) -> bool:
    """Check if an affiliation belongs to a company (not an academic institution)."""
    if not affiliation:
        return False

    # Exclude affiliations that mention academic institutions
    for keyword in UNIVERSITY_KEYWORDS:
        if keyword.lower() in affiliation.lower():
            return False  # If it's a university, return False immediately

    # Check for company-related keywords
    for keyword in COMPANY_KEYWORDS:
        if keyword.lower() in affiliation.lower():
            return True  # If it contains company-related words, return True

    return False  # Default to False (academic) if unclear


def fetch_paper_ids(query: str, max_results: int = 5) -> List[str]:
    """
    Fetch paper IDs from PubMed based on a search query.
    Adds filters to increase the chance of getting company-affiliated papers.
    """
    if not query.strip():
        print("Error: Query cannot be empty.")
        return []

    params = {
        "db": "pubmed",
        "term": f"{query} AND industry[Affiliation]",  # Prioritize industry-funded papers
        "retmax": max_results,
        "format": "json"
    }

    try:
        response = requests.get(PUBMED_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: Failed to fetch paper IDs - {e}")
        return []


def fetch_paper_details(paper_ids: List[str]) -> List[Dict[str, Optional[str]]]:
    """
    Fetch details (title, authors, affiliations, publication date, and corresponding author email) for given paper IDs from PubMed.
    """
    if not paper_ids:
        print("Error: No valid paper IDs provided.")
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"  # Fetch data in XML format to extract detailed author affiliations
    }

    try:
        response = requests.get(PUBMED_DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)  # Parse XML response

        papers = []
        for article in root.findall(".//PubmedArticle"):
            paper_id = article.find(".//PMID").text
            title_element = article.find(".//ArticleTitle")
            title = title_element.text if title_element is not None else "Unknown"

            # Extract publication date
            pub_date_element = article.find(".//PubDate")
            pub_year = pub_date_element.find("Year").text if pub_date_element is not None and pub_date_element.find("Year") is not None else "Unknown"
            pub_month = pub_date_element.find("Month").text if pub_date_element is not None and pub_date_element.find("Month") is not None else ""
            pub_day = pub_date_element.find("Day").text if pub_date_element is not None and pub_date_element.find("Day") is not None else ""

            publication_date = f"{pub_year} {pub_month} {pub_day}".strip()

            # Extract author affiliations and corresponding email
            authors = article.findall(".//Author")
            company_authors = []
            company_names = []
            corresponding_email = "N/A"

            for author in authors:
                last_name = author.find("LastName")
                first_name = author.find("ForeName")
                affiliation = author.find(".//AffiliationInfo/Affiliation")

                author_name = f"{first_name.text} {last_name.text}" if first_name is not None and last_name is not None else "Unknown"

                if affiliation is not None:
                    affiliation_text = affiliation.text

                    # Extract corresponding author email (if available)
                    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation_text)
                    if email_match:
                        corresponding_email = email_match.group(0)  # Store first detected email

                    if is_company_affiliation(affiliation_text):
                        company_authors.append(author_name)
                        company_names.append(affiliation_text)

            papers.append({
                "PubmedID": paper_id,
                "Title": title,
                "Publication Date": publication_date,
                "Non-academic Authors": company_authors if company_authors else ["N/A"],
                "Company Affiliations": company_names if company_names else ["N/A"],
                "Corresponding Author Email": corresponding_email  # Include email field
            })

        return papers

    except requests.exceptions.RequestException as e:
        print(f"API Error: Failed to fetch paper details - {e}")
        return []
