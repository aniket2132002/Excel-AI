print("\n📋 DuckDB tables:")
tables = db.execute("SHOW TABLES;")
print(tables)
