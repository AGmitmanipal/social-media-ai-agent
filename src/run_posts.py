from prompts import linkdin_post_prompt, insta_post_prompt, x_post_prompt
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from agent import model
from summary import generate_summary
from search import search_tool

# Example usage
query = "What do you mean by temperature?" 
print(f"Running query: {query}")

# 1. Search
content = search_tool.invoke(query)
print("Search complete.")

# 2. Summarize
summary_text = generate_summary(content)
print("Summary generated.")

# 3. Create Chains
linkdin_post_chain = linkdin_post_prompt | model | StrOutputParser()
x_post_chain = x_post_prompt | model | StrOutputParser()
insta_post_chain = insta_post_prompt | model | StrOutputParser()

parallel_run = RunnableParallel({
    'LinkdIn': linkdin_post_chain,
    'X': x_post_chain,
    'Instagram': insta_post_chain
})

# 4. Invoke
drafts = parallel_run.invoke({
    'summary': summary_text
})

print("Drafts Generated:")
print(drafts)
