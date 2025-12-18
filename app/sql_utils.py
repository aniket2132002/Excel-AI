def clean_sql(sql: str) -> str:
    """
    Cleans LLM-generated SQL by removing markdown,
    code fences, and unsafe characters.
    """

    if not sql:
        return ""

    sql = sql.strip()

    # Remove triple backticks and language tags
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

    # Remove leading/trailing semicolons
    sql = sql.strip().rstrip(";")

    return sql.strip()
