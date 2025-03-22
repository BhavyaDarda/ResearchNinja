import streamlit as st
import random
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_competitor_analysis():
    """Renders the competitor analysis visualization panel"""
    st.header("Competitor Analysis Dashboard")

    competitors = [
        'All Competitors', 'Company A', 'Company B', 'Company C', 'Company D',
        'Company E'
    ]
    selected_competitor = st.selectbox("Select Competitor for Analysis",
                                       competitors)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Market Share",
                  f"{random.uniform(5, 30):.1f}%",
                  delta=f"{random.uniform(-5, 5):.1f}%")
    with col2:
        st.metric("Revenue Growth",
                  f"{random.uniform(-5, 25):.1f}%",
                  delta=f"{random.uniform(-10, 10):.1f}%")
    with col3:
        st.metric("Product Count",
                  f"{random.randint(5, 50)}",
                  delta=f"{random.randint(-5, 10)}")
    with col4:
        st.metric("Pricing Index",
                  f"{random.uniform(80, 120):.1f}",
                  delta=f"{random.uniform(-10, 10):.1f}")

    tabs = st.tabs(["Market Position", "SWOT Analysis", "Growth-Share Matrix"])

    with tabs[0]:
        if selected_competitor != 'All Competitors':
            render_competitor_details(selected_competitor)
        else:
            render_market_overview()
    with tabs[1]:
        render_swot_analysis(selected_competitor)
    with tabs[2]:
        render_growth_share_matrix()


def render_competitor_details(competitor):
    """Renders detailed analysis for a specific competitor"""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {competitor} Strengths")
        st.markdown("- Strong market presence")
        st.markdown("- Innovative product portfolio")
        st.markdown("- Efficient distribution network")
    with col2:
        metrics = {
            "Market Share": f"{random.uniform(5, 30):.1f}%",
            "Annual Revenue": f"${random.uniform(10, 100):.1f}M",
            "Growth Rate": f"{random.uniform(-5, 25):.1f}%",
            "Customer Satisfaction": f"{random.uniform(3.5, 4.8):.1f}/5.0"
        }
        for key, value in metrics.items():
            st.metric(label=key, value=value)


def render_market_overview():
    """Renders overall market analysis"""
    companies = [
        'Company A', 'Company B', 'Company C', 'Company D', 'Company E'
    ]
    df = pd.DataFrame({
        'Company':
        companies,
        'Market Share (%)': [random.uniform(5, 30) for _ in companies],
        'Growth Rate (%)': [random.uniform(-5, 25) for _ in companies]
    })
    fig = px.scatter(df,
                     x='Market Share (%)',
                     y='Growth Rate (%)',
                     text='Company',
                     size=[30] * len(companies),
                     color='Company')
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)


def render_swot_analysis(competitor):
    """Renders SWOT analysis visualization"""
    if competitor == 'All Competitors':
        st.info("Please select a specific competitor to see SWOT analysis.")
        return
    st.subheader(f"SWOT Analysis: {competitor}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Strengths")
        st.markdown("- Strong brand recognition")
        st.markdown("- Innovative product portfolio")
        st.markdown("- Efficient supply chain")
        st.markdown("### Weaknesses")
        st.markdown("- High operational costs")
        st.markdown("- Limited market reach")
        st.markdown("- Product gaps")
    with col2:
        st.markdown("### Opportunities")
        st.markdown("- Emerging markets")
        st.markdown("- Digital transformation")
        st.markdown("- Strategic partnerships")
        st.markdown("### Threats")
        st.markdown("- Intense competition")
        st.markdown("- Regulatory changes")
        st.markdown("- Market volatility")


def render_growth_share_matrix():
    """Renders BCG growth-share matrix"""
    st.subheader("Growth-Share Matrix Analysis")
    products = [
        'Product A', 'Product B', 'Product C', 'Product D', 'Product E'
    ]
    df = pd.DataFrame({
        'Product':
        products,
        'Market Share (%)': [random.uniform(0, 50) for _ in products],
        'Growth Rate (%)': [random.uniform(-10, 30) for _ in products],
        'Revenue (M)': [random.uniform(10, 100) for _ in products]
    })
    fig = px.scatter(df,
                     x='Market Share (%)',
                     y='Growth Rate (%)',
                     size='Revenue (M)',
                     text='Product',
                     color='Product',
                     title='BCG Growth-Share Matrix')
    fig.add_hline(y=np.mean(df['Growth Rate (%)']),
                  line_dash="dash",
                  line_color="gray")
    fig.add_vline(x=np.mean(df['Market Share (%)']),
                  line_dash="dash",
                  line_color="gray")
    st.plotly_chart(fig, use_container_width=True)


# Run the application
if __name__ == "__main__":
    render_competitor_analysis()
