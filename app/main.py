# from excel_loader import load_excel
# from duckdb_engine import DuckDBEngine
# from schema_extractor import extract_schema

# EXCEL_PATH = "D:\\excel_ai_analyst_step1\\data\\sample.xlsx"


# def main():
#     print("📥 Loading Excel...")
#     sheets = load_excel(EXCEL_PATH)

#     print("📊 Registering tables in DuckDB...")
#     db = DuckDBEngine()
#     db.register_tables(sheets)

#     print("🧠 Extracting schema...")
#     schema = extract_schema(sheets)

#     print("\n=== SCHEMA ===")
#     for table, info in schema.items():
#         print(f"\nTable: {table}")
#         for col in info["columns"]:
#             print(f"  - {col['name']} ({col['dtype']}) nulls={col['nulls']}")

# if __name__ == "__main__":
#     main()

from excel_loader import load_excel
from duckdb_engine import DuckDBEngine
from schema_extractor import extract_schema
from llm_agent import generate_sql
from sql_utils import clean_sql

# ✅ Always use relative path
EXCEL_PATH = "data\\sample.xlsx"


def main():
    print("📥 Loading Excel...")
    sheets = load_excel(EXCEL_PATH)

    print("\n✅ Loaded sheets (after normalization):")
    for name, df in sheets.items():
        print(f"  - {name}: rows={df.shape[0]}, cols={df.shape[1]}")

    print("\n📊 Registering tables in DuckDB...")
    db = DuckDBEngine()
    db.register_tables(sheets)

    # 🔍 DEBUG: show actual DuckDB table names
    print("\n📋 DuckDB tables:")
    try:
        tables = db.execute("SHOW TABLES;")
        print(tables)
    except Exception as e:
        print("❌ Could not fetch table list:", e)

    print("\n🧠 Extracting schema...")
    schema = extract_schema(sheets)

    print("\n=== SCHEMA ===")
    for table, info in schema.items():
        print(f"\nTable: {table}")
        for col in info["columns"]:
            print(f"  - {col['name']} ({col['dtype']}) nulls={col['nulls']}")

    # 🔁 Interactive question loop
    while True:
        question = input("\n🧠 Ask a question (or 'exit'): ").strip()

        if question.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            break

        print("\n🤖 Generating SQL...")
        sql = generate_sql(schema, question)

        print("\n🧾 Raw SQL from LLM:\n", sql)

        cleaned_sql = clean_sql(sql)
        print("\n🧼 Cleaned SQL:\n", cleaned_sql)

        try:
            result = db.execute(cleaned_sql)
            print("\n📊 Result:\n", result)
        except Exception as e:
            print("\n❌ SQL Execution Error:")
            print(e)


if __name__ == "__main__":
    main()
