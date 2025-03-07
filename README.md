# Research Paper Fetcher

## 📌 Overview
Research Paper Fetcher is a command-line tool that retrieves research papers from PubMed based on a search query. It fetches paper details, extracts author affiliations, and filters out non-academic (company-affiliated) authors.

---

## 🚀 Features
- Fetches research papers from **PubMed API**.
- Extracts **title, publication date, authors, and affiliations**.
- Identifies **non-academic (company-affiliated) authors**.
- Provides **CLI support** for easy access.
- Saves results in a **CSV file** (optional).

---

## ⚙️ Installation

### **1️⃣ Prerequisites**
- Python **3.8+**
- Poetry package manager

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/research-paper-fetcher.git
cd research-paper-fetcher
```
### **3️⃣ Install Dependencies**
```bash
poetry install
```

## 🛠️ Usage

### **1️⃣ Fetch Research Papers (Basic)**
```bash
poetry run get-papers-list "cancer treatment"
```

```bash
{
  "PubmedID": "40052396",
  "Title": "A Green Microwave-Assisted Extraction of Cannabis sativa L.",
  "Publication Date": "2025 Mar 07",
  "Non-academic Authors": ["Dr. Smith"],
  "Company Affiliations": ["Moderna Inc."]
}

```

### **2️⃣ Save Results to CSV**
```bash
poetry run get-papers-list "cancer treatment" --file results.csv
```
### **3️⃣ Enable Debug Mode**
```bash
poetry run get-papers-list "cancer treatment" --debug
```

## 🏗️ Project Structure

```bash
research-paper-fetcher/
│── src/
│   ├── research_paper_fetcher/
│   │   ├── pubmed_fetcher.py  # Core API module
│   │   ├── main.py            # CLI script
│── tests/                     # Test cases
│── pyproject.toml             # Poetry dependency file
│── README.md                  # Project documentation
│── .gitignore                 # Ignore unnecessary files
```

## 🔍 System Design & Workflow

### **1️⃣ Fetching Paper IDs from PubMed**
- Uses **PubMed `esearch.fcgi` API** to retrieve **relevant paper IDs** based on the search term.

### **2️⃣ Fetching Paper Details**
- Calls **`efetch.fcgi` API** to get **paper metadata**.
- Extracts **title, publication date, authors, and affiliations**.

### **3️⃣ Filtering Company-Affiliated Authors**
- Identifies **company affiliations** using keywords (`Inc., Ltd., Pharma`).
- Excludes **university and research-based affiliations**.

### **4️⃣ Output & Storage**
- Displays **filtered results in JSON format**.
- Saves results to **CSV (if requested by the user)**.


## ✅ Functional Requirements

- ✔ Fetch research papers based on a search query.
- ✔ Extract title, publication date, authors, and affiliations.
- ✔ Identify non-academic (company-affiliated) authors.
- ✔ Handle invalid queries, API failures, missing data.
- ✔ Provide CLI support with CSV output option.

## ⚠️ Non-Functional Requirements
- ✔ Efficient API calls with batch processing.
- ✔ Error handling for network issues & API failures.
- ✔ Modular design (pubmed_fetcher.py for API, main.py for CLI).
- ✔ Python type hints for readability and maintainability.
- ✔ Follows best practices for structured logging & debugging.

## ⚠️ Known Limitations
- PubMed API does not always return company affiliations → Some results may be "N/A".
- Industry-funded research may not be clearly labeled in PubMed data.
- Alternative data sources (e.g., ClinicalTrials.gov) might be needed for better industry research.

## 📜 License
This project is licensed under the MIT License.

## 👩‍💻 Author
**Harshita Yadav** 
- Backend Developer | Passionate about APIs & System Design
- [GitHub](https://github.com/harshita795) | [LinkedIn](https://www.linkedin.com/in/harshita-yadav-backend-developer/)
