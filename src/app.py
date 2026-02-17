import streamlit as st
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from agent import model
from prompts import linkdin_post_prompt, x_post_prompt, insta_post_prompt
from summary import generate_summary
from search import search_tool

# Page Configuration
st.set_page_config(
    page_title="PlayPuff AI",
    layout="wide"
)

# Title and Description
st.image("playpuff.png", width=300)
st.title("PlayPuff AI")
st.markdown("""
Generate professional social media posts (LinkedIn, X, Instagram) from a topic or search query.
""")

# Input Section
query = st.text_input("Enter a topic or query:", placeholder="e.g., The impact of AI on healthcare")

if st.button("Generate Content"):
    if not query:
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Searching and generating content..."):
            try:
                # 1. Search
                st.info(f"Searching for '{query}'...")
                search_results = search_tool.invoke(query)
                
                if not search_results:
                     st.error("No search results found. Please try a different query.")
                     st.stop()

                # 2. Summarize
                st.info("Summarizing search results...")
                summary_text = generate_summary(search_results)
                
                with st.expander("View Summary of Search Results"):
                    st.write(summary_text)

                # 3. Generate Posts
                st.info("Generating social media posts...")
                
                # Define Chains
                linkdin_post_chain = linkdin_post_prompt | model | StrOutputParser()
                x_post_chain = x_post_prompt | model | StrOutputParser()
                insta_post_chain = insta_post_prompt | model | StrOutputParser()

                parallel_run = RunnableParallel({
                    'LinkedIn': linkdin_post_chain,
                    'X': x_post_chain,
                    'Instagram': insta_post_chain
                })

                # Run Generations
                drafts = parallel_run.invoke({'summary': summary_text})

                # Display Results
                st.success("Drafts Generated!")
                
                tab1, tab2, tab3 = st.tabs(["LinkedIn", "Twitter / X", "Instagram"])

                with tab1:
                    st.subheader("LinkedIn Post")
                    st.text_area("Copy your LinkedIn post:", value=drafts['LinkedIn'], height=300)
                
                with tab2:
                    st.subheader("X Post")
                    st.text_area("Copy your Tweet:", value=drafts['X'], height=150)
                
                with tab3:
                    st.subheader("Instagram Post")
                    st.text_area("Copy your Instagram Caption:", value=drafts['Instagram'], height=300)

            except Exception as e:
                st.error(f"An error occurred: {e}")
