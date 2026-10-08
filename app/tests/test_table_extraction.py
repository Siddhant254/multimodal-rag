from app.ingestion.table_extractor import extract_tables


PDF_PATH = r"C:\multi_modal_rag\data\uploads\c59a336d-d0e1-490b-9240-43be0af38f93_01. Rational Numbers.pdf"


tables = extract_tables(PDF_PATH)

print(f"Total tables found: {len(tables)}")

for table in tables:
    print("\n--------------------")
    print(f"Page: {table['page_number']}")
    print(f"Table ID: {table['table_id']}")
    print("Rows:")

    for row in table["rows"]:
        print(row)