from langchain_core.prompts import PromptTemplate

linkdin_post_prompt = PromptTemplate.from_template("""
You are a social media expert. Create a professional LinkedIn post based on the following summary:
{summary}

The post should be engaging, informative, and include relevant hashtags.
""")

x_post_prompt = PromptTemplate.from_template("""
You are a social media expert. Create a Twitter/X post (tweet) based on the following summary:
{summary}

The tweet should be concise (under 280 characters), catchy, and include relevant hashtags.
""")

insta_post_prompt = PromptTemplate.from_template("""
You are a social media expert. Create an Instagram post caption based on the following summary:
{summary}

The caption should be visual, engaging, include emojis, and relevant hashtags.
""")
