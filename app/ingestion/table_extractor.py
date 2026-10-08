import pdfplumber


def is_empty_table(table):
    """
    Returns True if the table contains no meaningful data.
    """

    for row in table:
        for cell in row:
            if cell is not None and str(cell).strip():
                return False

    return True


def clean_cell(cell):
    """
    Cleans a single table cell.
    """

    if cell is None:
        return None

    return " ".join(str(cell).split())


def normalize_table(table):
    """
    Cleans rows and cells without changing the table's meaning.
    """

    normalized_rows = []

    for row in table:

        cleaned_row = [
            clean_cell(cell)
            for cell in row
        ]

        # Skip completely empty rows
        if not any(
            cell is not None and cell.strip()
            for cell in cleaned_row
        ):
            continue

        normalized_rows.append(cleaned_row)

    return normalized_rows


def extract_tables(file_path: str):
    document_tables = []

    with pdfplumber.open(file_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            tables = page.extract_tables()

            for table_index, table in enumerate(tables, start=1):

                # Ignore completely empty tables
                if is_empty_table(table):
                    continue

                normalized_rows = normalize_table(table)

                document_tables.append(
                    {
                        "page_number": page_number,
                        "table_id": f"page_{page_number}_table_{table_index}",
                        "rows": normalized_rows,
                    }
                )

    return document_tables