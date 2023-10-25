import csv

def generate_bibtex_key(authors, year):
    """Generate a BibTeX key from the first author's last name and the year"""
    last_names = authors.split(",")[0].split()
    last_name = last_names[-1] if len(last_names) > 0 else ""
    return f"{last_name.lower()}{year}"

def convert_csv_to_bibtex(csv_file, bibtex_file):
    """Convert a CSV file to BibTeX format"""
    with open(csv_file, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        with open(bibtex_file, "w", encoding="utf-8") as bibtexfile:
            for row in reader:
                authors = row["Authors"]
                year = row["Year"]
                title = row["Title"]
                doi = row["DOI"]
                # bibtex_key = generate_bibtex_key(authors, year)
                bibtex_entry = f"@article{{\n" \
                               f"  author = {{{authors}}},\n" \
                               f"  title = {{{title}}},\n" \
                               f"  year = {{{year}}},\n" \
                               f"  number = 1,\n" \
                               f"  doi = {{{doi}}}\n" \
                               f"}}\n\n"
                bibtexfile.write(bibtex_entry)

# Example usage
convert_csv_to_bibtex("your_file_name.csv", "scopus.bib")