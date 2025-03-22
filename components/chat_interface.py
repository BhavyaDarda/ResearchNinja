import streamlit as st
from backend.ai_integration import generate_ai_response
from backend.scraper import search_and_extract_content
from datetime import datetime


def initialize_session():
    """Initializes session state variables if not set"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "research_sources" not in st.session_state:
        st.session_state.research_sources = []


def render_chat_interface(ai_model):
    """
    Renders the chat interface for research queries

    Args:
        ai_model (str): The selected AI model to use for responses
    """
    initialize_session()
    st.header("Research Assistant")

    # Chat message container
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("Sources"):
                        for idx, source in enumerate(message["sources"]):
                            st.markdown(
                                f"{idx+1}. [{source['title']}]({source['url']})"
                            )

    # Query input
    st.write("### Ask a research question")

    col1, col2 = st.columns([5, 1])

    with col1:
        user_query = st.text_input(
            "Enter your research query",
            placeholder=
            "Example: Analyze the market trends for electric vehicles in Europe",
            label_visibility="collapsed",
            key="chat_query_input")

    with col2:
        search_button = st.button("Research",
                                  type="primary",
                                  key="chat_search_button")

    advanced_options = st.expander("Advanced Options")

    with advanced_options:
        col1, col2 = st.columns(2)
        with col1:
            recency = st.select_slider("Information Recency",
                                       options=[
                                           "Any time", "Past year",
                                           "Past month", "Past week",
                                           "Past day"
                                       ],
                                       value="Past month",
                                       key="chat_recency_slider")
        with col2:
            search_depth = st.slider(
                "Search Depth",
                1,
                10,
                3,
                help=
                "Higher values provide more comprehensive research but take longer",
                key="chat_depth_slider")

        custom_sources = st.text_area(
            "Additional URLs to include (one per line)",
            placeholder=
            "https://example.com/market-report\nhttps://example.com/industry-analysis",
            help="Add specific sources you want to include in the research",
            key="chat_custom_sources")

    # Process the research query when button is clicked
    if search_button and user_query:
        with st.spinner(f"Researching '{user_query}' using {ai_model}..."):
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role":
                "user",
                "content":
                user_query,
                "timestamp":
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Get custom URLs if provided
            custom_urls = [
                url.strip() for url in custom_sources.split("\n")
                if url.strip()
            ] if custom_sources else []

            try:
                # Search and extract web content
                search_results = search_and_extract_content(
                    query=user_query,
                    recency=recency,
                    search_depth=search_depth,
                    custom_urls=custom_urls)

                # Save sources to session state
                st.session_state.research_sources = search_results

                # Generate AI response based on the extracted content
                response, formatted_sources = generate_ai_response(
                    query=user_query,
                    search_results=search_results,
                    model=ai_model)

                # Add AI response to chat history
                st.session_state.chat_history.append({
                    "role":
                    "assistant",
                    "content":
                    response,
                    "sources":
                    formatted_sources,
                    "timestamp":
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Refresh to display new messages
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Disclaimer about AI models
    st.caption(
        "Note: Free tier AI models are used which may have knowledge cutoffs and limitations."
    )
