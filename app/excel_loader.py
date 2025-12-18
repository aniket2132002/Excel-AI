import pandas as pd
import re

def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w_]", "", name)

    # 🚨 CRITICAL FIX: table names must not start with a number
    if name[0].isdigit():
        name = f"t_{name}"

    return name


def load_excel(file_path: str) -> dict:
    xls = pd.ExcelFile(file_path)
    sheets = {}

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)

        if df is None or df.shape[1] == 0 or df.shape[0] == 0:
            print(f"⚠️ Skipping sheet (no columns): {sheet_name}")
            continue

        clean_table_name = normalize_name(sheet_name)
        df.columns = [str(c).strip() for c in df.columns]

        sheets[clean_table_name] = df

    return sheets
