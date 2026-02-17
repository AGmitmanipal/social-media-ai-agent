from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agent import model

summarization_prompt = PromptTemplate.from_template("""
You are a research assistant.
Summarize the following content into 4-5 bullet points and a conclusion at the end:

{content}
""")

summarization_chain = summarization_prompt | model | StrOutputParser()

def generate_summary(content):
    """
    Generates a summary of the provided content.
    """
    return summarization_chain.invoke({'content': content})