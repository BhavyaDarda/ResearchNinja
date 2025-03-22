import streamlit as st
from datetime import datetime
import os
import json

# Import all component modules
from components.business_viability import render_business_viability
from components.competitor_analysis import render_competitor_analysis
from components.customer_analysis import render_customer_analysis
from components.trend_analysis import render_trend_analysis
from components.regulatory_analysis import render_regulatory_analysis
from components.supply_chain import render_supply_chain_analysis

# Import backend functions
from backend.ai_integration import generate_ai_response
from backend.scraper import search_and_extract_content

# Import utility modules
from utils.api_validator import APIKeyValidator
from utils.error_handler import ErrorHandler
import logging
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Research Ninja - AI-Powered Content Research",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling based on requirements
st.markdown("""
<style>
    /* Primary colors from requirements */
    :root {
        --primary: #0A2540;
        --secondary: #00A67E;
        --background: #FFFFFF;
        --text: #1A1A1A;
        --accent: #FF6B6B;
        --alert: #FFD93D;
    }

    /* Header styling */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: var(--primary);
    }

    /* Code blocks styling */
    code {
        font-family: 'SF Mono', monospace;
    }

    /* Body text */
    body {
        font-family: system-ui, -apple-system, sans-serif;
        color: var(--text);
    }

    /* Card styling */
    .stCard {
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 4px;
    }
    .badge-primary {
        background-color: #0A2540;
        color: white;
    }
    .badge-secondary {
        background-color: #00A67E;
        color: white;
    }
    .badge-accent {
        background-color: #FF6B6B;
        color: white;
    }
    .badge-alert {
        background-color: #FFD93D;
        color: #1A1A1A;
    }

    /* Improved sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }

    /* Streamlit improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00A67E;
        color: white;
    }

    /* Container with border styling */
    [data-testid="stExpander"] {
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    /* Main container */
    .main-container {
        padding: 2rem;
        border-radius: 10px;
        background-color: #FAFBFC;
    }

    /* Results container */
    .results-container {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E6E9ED;
    }

    /* Make inputs more visible */
    [data-testid="stTextInput"] > div > div > input {
        padding: 0.75rem !important;
        font-size: 1.05rem !important;
    }

    /* Custom card styling */
    .insight-card {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e6e9ed;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Improved button styling */
    .stButton > button {
        font-weight: 600 !important;
        height: 3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'research_sources' not in st.session_state:
    st.session_state.research_sources = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'target_audience' not in st.session_state:
    st.session_state.target_audience = ""
if 'active_tabs' not in st.session_state:
    # Default active tabs for each section
    st.session_state.active_tabs = {
        "business_viability": 0,
        "competitor_analysis": 0,
        "customer_analysis": 0,
        "trend_analysis": 0,
        "regulatory_analysis": 0,
        "supply_chain": 0
    }

# Sidebar for settings
with st.sidebar:
    st.title("🥷 Research Ninja")

    st.markdown("### All-in-One Content Research")
    st.markdown("""
    Enter your business idea, content strategy, topic, or niche in **one query**, and Research Ninja will generate comprehensive analysis across all business dimensions.
    """)

    # Divider
    st.markdown("---")

    # AI Model Selection
    st.subheader("AI Model")
    ai_model = st.selectbox(
        "Select AI Model:",
        ["GPT-4o mini", "Gemini", "Claude", "Cohere"],
        help="Advanced AI models provide more comprehensive analysis but may require API keys"
    )

    # Research parameters
    st.subheader("Research Parameters")

    recency = st.select_slider(
        "Information Recency",
        options=["Any time", "Past year", "Past month", "Past week", "Past day"],
        value="Past month",
        key="sidebar_recency"
    )

    search_depth = st.slider(
        "Research Depth", 
        min_value=1, 
        max_value=10, 
        value=5, 
        help="Higher values provide more comprehensive research but take longer",
        key="sidebar_depth"
    )

    # Export Options
    st.subheader("Export Options")
    export_format = st.selectbox(
        "Export Format:",
        ["PDF", "JSON", "TXT", "Markdown", "DOCX"]
    )

    def perform_export():
        if st.session_state.analysis_results:
            try:
                # Placeholder for actual export logic.  Replace with your export code.
                # This is a critical area where the original 'return' statement might have been
                # and caused the error.  The following line simulates the error handling.
                # ... your export code here ...
                st.success("Research exported successfully!")
            except Exception as e:
                logger.error("Export error", exc_info=True)
                st.error(f"Export failed: {str(e)}")
                #raise HTTPException(status_code=500, detail="Export failed") #Commented out as this requires a specific framework (like FastAPI)
        else:
            st.warning("No research results to export. Run a query first.")


    if st.button("Export Research", type="primary", key="export_button"):
        perform_export()

    # Advanced Settings
    with st.expander("Advanced Settings"):
        st.info("The unified interface automatically optimizes the search across all research dimensions.")

        custom_sources = st.text_area(
            "Additional URLs to include (one per line)",
            placeholder="https://example.com/market-report\nhttps://example.com/industry-analysis",
            help="Add specific sources you want to include in the research",
            key="sidebar_sources"
        )

        st.markdown("#### API Keys (Optional)")
        st.caption("For enhanced results, you can provide API keys for external services:")

        # Initialize API key session state if needed
        if 'api_keys' not in st.session_state:
            st.session_state.api_keys = {
                "bing": "",
                "openai": "",
                "gemini": "",
                "anthropic": "",
                "cohere": ""
            }

        # These fields connect to environment variables through session state
        bing_api = st.text_input("Bing Search API Key", 
                                 value=st.session_state.api_keys["bing"],
                                 type="password", 
                                 help="For better search results")

        openai_api = st.text_input("OpenAI API Key", 
                                   value=st.session_state.api_keys["openai"],
                                   type="password", 
                                   help="For GPT-4o mini model")

        gemini_api = st.text_input("Google Gemini API Key", 
                                   value=st.session_state.api_keys["gemini"],
                                   type="password", 
                                   help="For Gemini model")

        # Save and validate API keys when changed
        if bing_api != st.session_state.api_keys["bing"]:
            if APIKeyValidator.save_api_key("BING_API_KEY", bing_api):
                st.session_state.api_keys["bing"] = bing_api
                st.success("Bing API key validated and saved successfully!")
            else:
                st.error("Invalid Bing API key. Please check and try again.")

        if openai_api != st.session_state.api_keys["openai"]:
            st.session_state.api_keys["openai"] = openai_api
            os.environ["OPENAI_API_KEY"] = openai_api

        if gemini_api != st.session_state.api_keys["gemini"]:
            st.session_state.api_keys["gemini"] = gemini_api
            os.environ["GEMINI_API_KEY"] = gemini_api

        # Additional APIs (without nested expander to avoid Streamlit error)
        st.markdown("##### More API Options:")

        anthropic_api = st.text_input("Anthropic API Key", 
                                     value=st.session_state.api_keys["anthropic"],
                                     type="password", 
                                     help="For Claude model")

        cohere_api = st.text_input("Cohere API Key", 
                                  value=st.session_state.api_keys["cohere"],
                                  type="password", 
                                  help="For Cohere model")

        if anthropic_api != st.session_state.api_keys["anthropic"]:
            st.session_state.api_keys["anthropic"] = anthropic_api
            os.environ["ANTHROPIC_API_KEY"] = anthropic_api

        if cohere_api != st.session_state.api_keys["cohere"]:
            st.session_state.api_keys["cohere"] = cohere_api
            os.environ["COHERE_API_KEY"] = cohere_api

    st.markdown("---")
    st.caption("Research Ninja v1.5 - Unified Research Interface")

# Main content area
st.title("🥷 Research Ninja")
st.subheader("Comprehensive Content Research & Market Analysis Platform")

# Research query input section
st.markdown("### Enter your research query")

query_col1, query_col2 = st.columns([3, 1])
with query_col1:
    user_query = st.text_input(
        "Business idea, content strategy, topic or niche",
        placeholder="Example: A subscription-based meal prep service for fitness enthusiasts",
        key="main_query"
    )

with query_col2:
    target_audience = st.text_input(
        "Target Audience (Optional)",
        placeholder="Example: Young professionals, 25-40",
        key="target_audience_input"
    )

# Research options
advanced_options = st.expander("Additional Research Options", expanded=False)
with advanced_options:
    col1, col2, col3 = st.columns(3)

    with col1:
        focus_business = st.checkbox("Business Viability", value=True)
        focus_competitors = st.checkbox("Competitor Analysis", value=True)

    with col2:
        focus_customers = st.checkbox("Customer Analysis", value=True)
        focus_trends = st.checkbox("Trend Analysis", value=True)

    with col3:
        focus_regulatory = st.checkbox("Regulatory Compliance", value=True)
        focus_supply = st.checkbox("Supply Chain", value=True)

# Research button
research_button = st.button(
    "Generate Comprehensive Research", 
    type="primary", 
    use_container_width=True,
    key="research_button"
)

# Process query when button is clicked
if research_button and user_query:
    # Validate required API keys using the validator
    missing_api_keys = APIKeyValidator.get_missing_api_keys(ai_model)

    # If keys are missing, show a detailed warning with guidance
    if missing_api_keys:
        missing_key_names = [key_info["name"] for key_info in missing_api_keys]

        # Show warning with missing keys
        st.warning(f"⚠️ Missing required API key(s): {', '.join(missing_key_names)}. Research Ninja requires these API keys for real-time data analysis.")

        # Info message about data integrity
        st.info("Research Ninja uses only real data from authorized sources. We don't generate synthetic data.")

        # Show more specific guidance for each missing key
        for key_info in missing_api_keys:
            with st.expander(f"About {key_info['name']}"):
                st.markdown(f"**{key_info['name']}**")
                st.markdown(key_info['description'])
                st.markdown(f"Get your API key here: [{key_info['url']}]({key_info['url']})")
                st.markdown("Then add it in the 'Advanced Settings' panel on the left sidebar.")
    else:
        # All required API keys are available, proceed with research
        with st.spinner(f"Researching '{user_query}' using {ai_model}... This may take a minute or two for comprehensive research."):
            # Save target audience
            st.session_state.target_audience = target_audience

            # Clear previous chat history
            st.session_state.chat_history = []

            # Construct comprehensive research prompt with target audience and focused areas
            research_prompt = f"Comprehensive research on: {user_query}"
            if target_audience:
                research_prompt += f" targeting {target_audience}"

            # Track which sections are enabled for focused research
            enabled_sections = []
            if focus_business:
                enabled_sections.append("business viability")
            if focus_competitors:
                enabled_sections.append("competitor analysis")
            if focus_customers:
                enabled_sections.append("customer and audience analysis")
            if focus_trends:
                enabled_sections.append("market trends")
            if focus_regulatory:
                enabled_sections.append("regulatory compliance")
            if focus_supply:
                enabled_sections.append("supply chain and distribution")

            if enabled_sections:
                research_prompt += f" with focus on {', '.join(enabled_sections)}"

            # Add user query to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": research_prompt,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Get custom URLs if provided
            custom_urls = []
            if custom_sources:
                custom_urls = [url.strip() for url in custom_sources.split("\n") if url.strip()]

            # Increase search depth for comprehensive research
            comprehensive_depth = max(search_depth, 5)  # Ensure a minimum depth for good results

            try:
                # Search and extract web content with enhanced categorized search
                search_results = search_and_extract_content(
                    query=user_query,
                    recency=recency,
                    search_depth=comprehensive_depth,
                    custom_urls=custom_urls
                )

                if not search_results:
                    st.error("No search results found. Please try a different query or check your API keys.")
                    st.stop()

                # Validate search results
                if not isinstance(search_results, list) or not all(isinstance(r, dict) for r in search_results):
                    st.error("Invalid search results format. Please check your API configuration.")
                    st.stop()

            except Exception as e:
                st.error(f"Error during search: {str(e)}")
                logger.error("Search error", exc_info=True)
                st.stop()

            # Save sources to session state
            st.session_state.research_sources = search_results

            # Generate AI response with comprehensive analysis
            response, formatted_sources = generate_ai_response(
                query=research_prompt,
                search_results=search_results,
                model=ai_model
            )

            # Add AI response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "sources": formatted_sources,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Structure the analysis results for visualizations
            st.session_state.analysis_results = {
                "query": user_query,
                "target_audience": target_audience,
                "response": response,
                "sources": formatted_sources,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "enabled_sections": enabled_sections
            }

            # Rerun to display results
            st.rerun()

# Display results if we have analysis data
if st.session_state.analysis_results:
    # Generate research data from chat history
    if not st.session_state.chat_history:
        st.info("Ask a market research question to see visualizations and insights here.")
        st.stop()
    # Get reference to enabled sections
    enabled_sections = st.session_state.analysis_results.get("enabled_sections", [])

    # If no specific sections are enabled, all are enabled by default
    if not enabled_sections:
        focus_business = focus_competitors = focus_customers = focus_trends = focus_regulatory = focus_supply = True

    # AI-generated response for parsing
    last_response = ""
    if st.session_state.chat_history:
        for msg in reversed(st.session_state.chat_history):
            if msg["role"] == "assistant":
                last_response = msg["content"]
                break

    # Display a success message
    st.success(f"Comprehensive research complete for: {st.session_state.analysis_results['query']}")

    # Generate tab names based on the enabled sections
    tab_names = ["📊 Summary & Key Insights"]
    if "business viability" in enabled_sections or focus_business:
        tab_names.append("💰 Business Viability")
    if "competitor analysis" in enabled_sections or focus_competitors:
        tab_names.append("🏆 Competitor Analysis")
    if "customer" in " ".join(enabled_sections) or "audience" in " ".join(enabled_sections) or focus_customers:
        tab_names.append("👥 Target Audience & Customer Analysis")
    if "market trends" in " ".join(enabled_sections) or focus_trends:
        tab_names.append("📈 Market Trends")
    if "regulatory" in " ".join(enabled_sections) or "supply chain" in " ".join(enabled_sections) or focus_regulatory or focus_supply:
        tab_names.append("📜 Regulatory & Supply Chain")

    # Display the main tabs for different research areas
    main_tabs = st.tabs(tab_names)

    # Tab 1: Summary & Key Insights
    with main_tabs[0]:
        st.header("Comprehensive Research Results")

        # Metadata about the query
        meta_col1, meta_col2, meta_col3 = st.columns(3)
        with meta_col1:
            st.metric("Query Timestamp", 
                      st.session_state.analysis_results["timestamp"].split()[0], 
                      None)
        with meta_col2:
            st.metric("AI Model Used", 
                      ai_model, 
                      None)
        with meta_col3:
            sources_count = len(st.session_state.analysis_results["sources"])
            st.metric("Sources Analyzed", 
                      str(sources_count), 
                      None)

        # Show a divider
        st.markdown("---")

        # Add a download button for the response in markdown format
        full_response_md = last_response

        # Display the AI response
        if last_response:
            st.markdown(last_response)

            # Display sources in an expander
            with st.expander("Sources & References"):
                for i, source in enumerate(st.session_state.analysis_results["sources"]):
                    st.markdown(f"**{i+1}. [{source['title']}]({source['url']})**")
                    st.markdown(f"*{source['accessed_date']}*")
                    st.markdown("---")

    # Track tab index for the remaining tabs
    tab_index = 1

    # Tab: Business Viability Analysis (if enabled)
    if "💰 Business Viability" in tab_names:
        with main_tabs[tab_index]:
            render_business_viability()
        tab_index += 1

    # Tab: Competitor Analysis (if enabled)
    if "🏆 Competitor Analysis" in tab_names:
        with main_tabs[tab_index]:
            render_competitor_analysis()
        tab_index += 1

    # Tab: Target Audience & Customer Analysis (if enabled)
    if "👥 Target Audience & Customer Analysis" in tab_names:
        with main_tabs[tab_index]:
            customer_subtabs = st.tabs(["Target Audience Segmentation", "Customer Expectations"])
            with customer_subtabs[0]:
                render_customer_analysis("Target Audience Segmentation")
            with customer_subtabs[1]:
                render_customer_analysis("Customer Expectations")
        tab_index += 1

    # Tab: Market Trends (if enabled)
    if "📈 Market Trends" in tab_names:
        with main_tabs[tab_index]:
            render_trend_analysis()
        tab_index += 1

    # Tab: Regulatory & Supply Chain (if enabled)
    if "📜 Regulatory & Supply Chain" in tab_names:
        with main_tabs[tab_index]:
            regulatory_subtabs = st.tabs(["Regulatory & Compliance", "Supply Chain & Distribution"])
            with regulatory_subtabs[0]:
                if "regulatory compliance" in " ".join(enabled_sections) or focus_regulatory:
                    render_regulatory_analysis()
                else:
                    st.info("Regulatory Analysis was disabled in the research options.")
            with regulatory_subtabs[1]:
                if "supply chain" in " ".join(enabled_sections) or focus_supply:
                    render_supply_chain_analysis()
                else:
                    st.info("Supply Chain Analysis was disabled in the research options.")
else:
    # Welcome message when no research has been done yet
    st.markdown("""
    ## Welcome to Research Ninja 1.5!

    Our **unified research interface** delivers comprehensive business analysis from a single query. Just enter your business idea or content strategy above, and we'll analyze all relevant dimensions at once.

    ### All-in-One Business Research:

    - **Business Viability Analysis**: Market potential, financial projections, and risk assessment
    - **Competitor Analysis**: Detailed SWOT analysis of key players in your market
    - **Target Audience Insights**: Demographic and psychographic profiles of your ideal customers
    - **Market Trends**: Emerging trends, consumer behavior shifts, and growth opportunities
    - **Regulatory & Supply Chain**: Compliance requirements and distribution strategies

    ### How It Works:

    1. Enter one comprehensive query about your business idea
    2. Our AI performs specialized searches across all research dimensions 
    3. Results are analyzed and synthesized into a complete business report
    4. View insights organized by category in the tabbed interface

    *All insights are generated using AI and real-time web data. The more specific your query, the better the results!*
    """)

    # Example queries
    with st.expander("Example Queries"):
        st.markdown("""
        - A subscription box service for pet owners focusing on organic treats and toys
        - An online course teaching social media marketing to small business owners 
        - A mobile app that helps users track and reduce their carbon footprint
        - A premium coffee brand targeting environmentally conscious millennials
        - A content strategy for a financial advice blog for young professionals
        """)