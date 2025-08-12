import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import settings

llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=0, api_key=settings.OPENAI_API_KEY)

def clean_sql(s: str) -> str:
    s = re.sub(r"```(?:sql)?\s*", "", s, flags=re.IGNORECASE).replace("```", "")
    return s.strip().split(";")[0].strip()

sql_prompt = PromptTemplate.from_template("""
Given the following table schema for the table `reest`:
                                          
{schema}
                                          
Write an SQL statement to answer the following question:
                                          
{question}
                                          
Provide all rows from the table (select *) when relevant.
Provide a LIMIT where applicable.
Respond with only the SQL statement.
""")

sql_chain = sql_prompt | llm | StrOutputParser()

answer_chain = (PromptTemplate.from_template("""
Use the following data to provide a definitive answer to the user's question:

{context}

The question is: {question}
""") | llm | StrOutputParser())
