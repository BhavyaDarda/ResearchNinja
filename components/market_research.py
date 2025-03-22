import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime, timedelta

def render_market_research():
    """Renders the market research visualization panel"""
    
    st.header("Market Research Dashboard")
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask a market research question to see visualizations and insights here.")
        return
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Market Size",
            value=f"${random.randint(10, 500)}B",
            delta=f"{random.uniform(-5, 15):.1f}%"
        )
    
    with col2:
        st.metric(
            label="CAGR",
            value=f"{random.uniform(1, 20):.1f}%",
            delta=f"{random.uniform(-2, 5):.1f}%"
        )
    
    with col3:
        st.metric(
            label="Key Players",
            value=f"{random.randint(3, 12)}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Market Maturity",
            value=random.choice(["Early", "Growth", "Mature", "Declining"]),
            delta=None
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Market Size", "Competitive Landscape", "Regional Analysis"])
    
    with tab1:
        render_market_size_tab()
    
    with tab2:
        render_competitive_landscape_tab()
    
    with tab3:
        render_regional_analysis_tab()
    
    # Summary box at the bottom
    st.subheader("Market Summary")
    
    # Extract the last assistant message for the summary
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        # Take first paragraph as summary
        summary = last_message.split('\n\n')[0] if '\n\n' in last_message else last_message
        st.write(summary)
    else:
        st.write("No market research summary available yet. Ask a question to generate insights.")

def render_market_size_tab():
    """Renders the market size visualization tab"""
    st.subheader("Market Size & Growth")
    
    # Create example market size data
    # In a real application, this would be derived from the research results
    current_year = datetime.now().year
    years = list(range(current_year - 4, current_year + 5))
    
    # Generate random market size data with a growth trend
    base_size = random.uniform(50, 200)
    growth_rate = random.uniform(0.05, 0.15)
    market_sizes = [base_size * ((1 + growth_rate) ** (i - 4)) for i in range(9)]
    
    # Create historical vs forecast split
    historical = market_sizes[:5]
    forecast = market_sizes[4:]
    historical_years = years[:5]
    forecast_years = years[4:]
    
    # Create and display chart
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Bar(
        x=historical_years,
        y=historical,
        name='Historical',
        marker_color='#0A2540'
    ))
    
    # Forecast data
    fig.add_trace(go.Bar(
        x=forecast_years,
        y=forecast,
        name='Forecast',
        marker_color='#00A67E'
    ))
    
    # Add growth rate line
    growth_rates = [(market_sizes[i] / market_sizes[i-1] - 1) * 100 for i in range(1, len(market_sizes))]
    # Add a placeholder for the first year
    growth_rates.insert(0, None)
    
    fig.add_trace(go.Scatter(
        x=years,
        y=growth_rates,
        mode='lines+markers',
        name='Growth Rate (%)',
        yaxis='y2',
        line=dict(color='#FF6B6B', width=2)
    ))
    
    # Update layout for dual-axis chart
    fig.update_layout(
        title='Market Size and Growth Rate',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Market Size (USD Billions)', side='left'),
        yaxis2=dict(title='Growth Rate (%)', side='right', overlaying='y', showgrid=False),
        legend=dict(x=0.01, y=0.99),
        hovermode='x unified',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_competitive_landscape_tab():
    """Renders the competitive landscape visualization tab"""
    st.subheader("Competitive Landscape")
    
    # Create example competitor data
    # In a real application, this would be derived from the research results
    competitors = ['Company A', 'Company B', 'Company C', 'Company D', 'Company E', 'Others']
    market_share = [random.uniform(5, 25) for _ in range(5)]
    market_share.append(100 - sum(market_share))  # Others make up the remaining percentage
    
    # Create and display pie chart
    fig = px.pie(
        values=market_share,
        names=competitors,
        title='Market Share Distribution',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A9A9A9']
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create a competitive positioning map
    st.subheader("Competitor Positioning")
    
    # Create example positioning data
    price_positioning = [random.uniform(1, 10) for _ in range(5)]
    quality_positioning = [random.uniform(1, 10) for _ in range(5)]
    revenue = [random.uniform(1, 15) for _ in range(5)]
    
    # Create a DataFrame for the scatter plot
    df = pd.DataFrame({
        'Competitor': competitors[:5],  # Exclude "Others"
        'Price Point': price_positioning,
        'Quality/Features': quality_positioning,
        'Revenue (USD Billions)': revenue
    })
    
    # Create and display scatter plot
    fig = px.scatter(
        df,
        x='Price Point',
        y='Quality/Features',
        size='Revenue (USD Billions)',
        color='Competitor',
        text='Competitor',
        size_max=50,
        title='Competitive Positioning Map',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    )
    
    fig.update_layout(
        xaxis=dict(title='Price Positioning (Lower → Higher)'),
        yaxis=dict(title='Quality/Features (Lower → Higher)'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_regional_analysis_tab():
    """Renders the regional analysis visualization tab"""
    st.subheader("Regional Market Distribution")
    
    # Create example regional data
    # In a real application, this would be derived from the research results
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    market_share = [random.uniform(5, 40) for _ in range(len(regions))]
    market_share = [share * 100 / sum(market_share) for share in market_share]  # Normalize to 100%
    growth_rate = [random.uniform(-2, 15) for _ in range(len(regions))]
    
    # Create a DataFrame for the visualization
    df = pd.DataFrame({
        'Region': regions,
        'Market Share (%)': market_share,
        'Growth Rate (%)': growth_rate
    })
    
    # Sort by market share
    df = df.sort_values('Market Share (%)', ascending=False)
    
    # Create and display horizontal bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['Region'],
        x=df['Market Share (%)'],
        orientation='h',
        marker_color='#0A2540',
        name='Market Share (%)'
    ))
    
    # Add growth rate markers
    fig.add_trace(go.Scatter(
        y=df['Region'],
        x=df['Growth Rate (%)'],
        mode='markers',
        marker=dict(
            size=12,
            color=df['Growth Rate (%)'],
            colorscale='RdYlGn',
            colorbar=dict(title='Growth Rate (%)'),
            cmin=-5,
            cmax=15,
            line=dict(width=1, color='black')
        ),
        name='Growth Rate (%)'
    ))
    
    fig.update_layout(
        title='Regional Market Distribution and Growth',
        xaxis=dict(title='Market Share (%)'),
        yaxis=dict(title='Region'),
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
