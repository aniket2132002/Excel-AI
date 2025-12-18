def extract_schema(dataframes: dict) -> dict:
    schema = {}

    for table, df in dataframes.items():
        schema[table] = {
            "columns": [
                {
                    "name": col,
                    "dtype": str(df[col].dtype),
                    "nulls": int(df[col].isna().sum())
                }
                for col in df.columns
            ],
            "rows": len(df)
        }

    return schema
