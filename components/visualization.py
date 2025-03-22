import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random
import datetime
from typing import List, Dict, Any

def render_visualization_panel(mode):
    """
    Renders the visualization panel for different modes

    Args:
        mode (str): The current research mode
    """
    st.header("Data Visualization")

    if not st.session_state.research_sources and not st.session_state.chat_history:
        render_empty_state(mode)
        return

    # Create tabs for different visualization options
    tab1, tab2, tab3 = st.tabs(["Overview", "Insights", "Sources"])

    with tab1:
        render_overview_tab(mode)

    with tab2:
        if st.session_state.chat_history:
            render_insights_tab()
        else:
            st.info("No insights available. Start researching to see key findings.")

    with tab3:
        render_sources_tab()


def render_empty_state(mode):
    """Renders an empty state when no data is available"""
    st.info(f"Ask a research question to see {mode.lower()} visualizations here.")

    # Show a placeholder for the visualization
    st.markdown("### Visualization Preview")

    # Example of what the visualization will look like (placeholder)
    if mode == "Market Research":
        fig = go.Figure()
        fig.add_annotation(
            text="Market research visualization will appear here",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    elif mode == "Competitor Analysis":
        fig = go.Figure()
        fig.add_annotation(
            text="Competitor analysis visualization will appear here",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = go.Figure()
        fig.add_annotation(
            text=f"{mode} visualization will appear here",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def render_overview_tab(mode):
    """Renders the overview tab with main visualization"""
    if mode == "Market Research":
        st.subheader("Market Overview")

        # If we have research data, generate visualizations
        if st.session_state.chat_history:
            # Create example market trend data based on most recent query
            # In a real application, this would be derived from actual research results
            dates = pd.date_range(end=datetime.date.today(), periods=12, freq='M')

            # Create a DataFrame for example visualization
            df = pd.DataFrame({
                'Date': dates,
                'Market Size (USD Billions)': [random.uniform(10, 100) for _ in range(len(dates))],
                'Growth Rate (%)': [random.uniform(-5, 15) for _ in range(len(dates))]
            })

            # Create and display market trend chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Date'], 
                y=df['Market Size (USD Billions)'],
                mode='lines+markers',
                name='Market Size',
                line=dict(color='#0A2540', width=2)
            ))

            # Add growth rate on secondary y-axis
            fig.add_trace(go.Scatter(
                x=df['Date'], 
                y=df['Growth Rate (%)'],
                mode='lines+markers',
                name='Growth Rate',
                line=dict(color='#00A67E', width=2),
                yaxis='y2'
            ))

            # Update layout for dual-axis chart
            fig.update_layout(
                title='Market Trends Analysis',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Market Size (USD Billions)', side='left', showgrid=False),
                yaxis2=dict(title='Growth Rate (%)', side='right', overlaying='y', showgrid=False),
                hovermode='x unified',
                legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    elif mode == "Competitor Analysis":
        st.subheader("Competitor Landscape")

        # If we have research data, generate visualizations
        if st.session_state.chat_history:
            # Create example competitor data based on the research query
            # In a real application, this would be derived from actual research results
            competitors = ['Company A', 'Company B', 'Company C', 'Company D', 'Company E']
            market_share = [random.uniform(5, 30) for _ in range(len(competitors))]
            revenue = [random.uniform(1, 10) for _ in range(len(competitors))]
            growth = [random.uniform(-5, 20) for _ in range(len(competitors))]

            # Create a DataFrame for example visualization
            df = pd.DataFrame({
                'Competitor': competitors,
                'Market Share (%)': market_share,
                'Revenue (USD Billions)': revenue,
                'Growth Rate (%)': growth
            })

            # Create and display bubble chart for competitor analysis
            fig = px.scatter(
                df, 
                x='Market Share (%)', 
                y='Growth Rate (%)',
                size='Revenue (USD Billions)',
                color='Competitor',
                hover_name='Competitor',
                text='Competitor',
                size_max=40,
                color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#8884d8']
            )

            fig.update_layout(
                title='Competitor Positioning Map',
                xaxis=dict(title='Market Share (%)'),
                yaxis=dict(title='Growth Rate (%)'),
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    elif mode == "Trend Analysis":
        st.subheader("Trend Analysis")

        # If we have research data, generate visualizations
        if st.session_state.chat_history:
            # Create example trend data
            categories = ['Trend A', 'Trend B', 'Trend C', 'Trend D', 'Trend E']
            current_year = [random.uniform(20, 100) for _ in range(len(categories))]
            previous_year = [random.uniform(10, 90) for _ in range(len(categories))]

            # Create a DataFrame for example visualization
            df = pd.DataFrame({
                'Category': categories,
                'Current Year': current_year,
                'Previous Year': previous_year
            })

            # Create and display radar chart for trend analysis
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=df['Current Year'],
                theta=df['Category'],
                fill='toself',
                name='Current Year',
                line_color='#0A2540'
            ))

            fig.add_trace(go.Scatterpolar(
                r=df['Previous Year'],
                theta=df['Category'],
                fill='toself',
                name='Previous Year',
                line_color='#00A67E'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(max(current_year), max(previous_year)) * 1.1]
                    )
                ),
                title='Trend Comparison',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    elif mode == "Customer Segmentation":
        st.subheader("Customer Segments")

        # If we have research data, generate visualizations
        if st.session_state.chat_history:
            # Create example customer segment data
            segments = ['Segment A', 'Segment B', 'Segment C', 'Segment D']
            segment_size = [random.uniform(10, 40) for _ in range(len(segments))]
            segment_growth = [random.uniform(-5, 15) for _ in range(len(segments))]
            segment_revenue = [random.uniform(1, 10) for _ in range(len(segments))]

            # Create a DataFrame for example visualization
            df = pd.DataFrame({
                'Segment': segments,
                'Size (%)': segment_size,
                'Growth (%)': segment_growth,
                'Revenue (USD Billions)': segment_revenue
            })

            # Create and display treemap for customer segmentation
            fig = px.treemap(
                df,
                path=['Segment'],
                values='Size (%)',
                color='Growth (%)',
                hover_data=['Revenue (USD Billions)'],
                color_continuous_scale=['#FF6B6B', '#FFFFFF', '#00A67E'],
                color_continuous_midpoint=0
            )

            fig.update_layout(
                title='Customer Segment Analysis',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

def render_insights_tab():
    """Renders the insights tab with key findings"""
    st.subheader("Key Insights")

    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]

    if assistant_messages:
        last_message = assistant_messages[-1]["content"]

        # Split the content into paragraphs and extract key insights
        paragraphs = last_message.split('\n\n')
        insights = [p for p in paragraphs if len(p) > 50][:3]  # Select the first 3 substantial paragraphs

        for i, insight in enumerate(insights):
            with st.container():
                st.markdown(f"**Insight {i+1}:** {insight}")
                st.markdown("---")
    else:
        st.info("No insights available. Start researching to see key findings.")

def render_sources_tab():
    """Renders the sources tab with reference information"""
    st.subheader("Research Sources")

    if not st.session_state.research_sources:
        st.info("No sources available. Start researching to see references.")
        return

    # Display the sources used in the research
    for i, source in enumerate(st.session_state.research_sources):
        with st.expander(f"Source {i+1}: {source['title']}", expanded=False):
            st.markdown(f"**URL:** [{source['url']}]({source['url']})")
            st.markdown(f"**Accessed:** {source['accessed_date']}")
            content_snippet = source.get('content', 'No content available')
            if len(content_snippet) > 300:
                content_snippet = content_snippet[:300] + "..."
            st.markdown(f"**Snippet:** {content_snippet}")