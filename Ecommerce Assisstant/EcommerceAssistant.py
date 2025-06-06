import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

#langsmith tracing and tracking

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true" 

output_parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an Ecommerce Assistant.

ONLY return a valid JSON object with the following fields:
- product_name
- price: {{"currency", "value"}}
- product_details: {{"specs"}}
- tentative_price_in_rupees: {{"currency", "value", "note"}}
- available_on: a list of {{"platform", "url"}}

DO NOT include <think> tags, explanation, markdown, or formatting.

Respond with only valid JSON.""" + output_parser.get_format_instructions()),
("user", "User reuested Product Details: {Query}")
    ]
)

model =  ChatGroq(temperature=0, model_name="deepseek-r1-distill-llama-70b")

chain = prompt | model

result = chain.invoke({"Query": "Motorola Edge Fusion"})

print(result.content)