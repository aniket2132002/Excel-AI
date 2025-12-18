from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from langchain_core.prompts import ChatPromptTemplate

# 🔑 Load API key directly from .env file
config = dotenv_values(".env")
OPENAI_API_KEY = config.get("OPENAI_API_KEY")

print("🔐 Using API key starting with:", OPENAI_API_KEY[:6], "******")

def generate_sql(schema: dict, question: str) -> str:
    schema_text = ""
    for table, info in schema.items():
        schema_text += f"\nTable: {table}\nColumns:\n"
        for col in info["columns"]:
            schema_text += f"- {col['name']} ({col['dtype']})\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You must return ONLY DuckDB SQL. No explanation."),
        ("human",
         f"Schema:\n{schema_text}\n\nQuestion:\n{question}")
    ])

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        openai_api_key=OPENAI_API_KEY  # 🔴 EXPLICIT
    )

    response = llm.invoke(prompt.format_messages())
    return response.content.strip()
