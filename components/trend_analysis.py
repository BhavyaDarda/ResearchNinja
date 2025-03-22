import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render_trend_analysis():
    """Renders the industry and trend analysis visualization panel"""
    
    st.header("Industry & Trend Analysis Dashboard")
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask an industry trend analysis question to see insights and visualizations here.")
        return
    
    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Market Growth Rate",
            value=f"{random.uniform(3, 15):.1f}%",
            delta=f"{random.uniform(-2, 5):.1f}%"
        )
    
    with col2:
        st.metric(
            label="Top Trend Impact",
            value=f"{random.choice(['High', 'Medium', 'Very High'])}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Disruption Potential",
            value=f"{random.randint(6, 9)}/10",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Adoption Timeframe",
            value=f"{random.choice(['6-12 mo', '1-2 yrs', '2-3 yrs'])}",
            delta=None
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Market Trends", "Technology Landscape", "Consumer Behavior", "Competitive Shifts"])
    
    with tab1:
        render_market_trends_tab()
    
    with tab2:
        render_technology_landscape_tab()
    
    with tab3:
        render_consumer_behavior_tab()
        
    with tab4:
        render_competitive_shifts_tab()
    
    # Trend insights
    st.subheader("Key Industry Insights")
    
    # Extract the last assistant message for insights
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        
        # Take a relevant paragraph as insights
        paragraphs = last_message.split('\n\n')
        trend_paragraphs = [p for p in paragraphs if "trend" in p.lower() or "industry" in p.lower() or "market" in p.lower()]
        if trend_paragraphs:
            insights = trend_paragraphs[0]
        else:
            insights = paragraphs[0] if paragraphs else last_message
        
        st.write(insights)
    else:
        st.write("No trend analysis insights available yet. Ask a question to generate insights.")

def render_market_trends_tab():
    """Renders the market trends visualization tab"""
    st.subheader("Market Growth Trends")
    
    # Create a time series of market size/growth
    # In a real application, this would be derived from the research results
    years = list(range(datetime.now().year - 3, datetime.now().year + 6))
    
    # Generate market size data with growth
    base_market_size = random.uniform(50, 500)  # Starting market size in billions
    growth_rates = [random.uniform(0.03, 0.15) for _ in range(len(years) - 1)]
    
    market_sizes = [base_market_size]
    for rate in growth_rates:
        market_sizes.append(market_sizes[-1] * (1 + rate))
    
    # Create a DataFrame for visualization
    market_df = pd.DataFrame({
        'Year': years,
        'Market Size (USD Billions)': market_sizes,
        'Market Type': ['Historical'] * 3 + ['Forecast'] * 6
    })
    
    # Calculate year-over-year growth rates
    market_df['YoY Growth (%)'] = [0] + [100 * (market_sizes[i] / market_sizes[i-1] - 1) for i in range(1, len(market_sizes))]
    
    # Create combined chart (line for market size, bar for growth rate)
    fig = go.Figure()
    
    # Market size line
    fig.add_trace(go.Scatter(
        x=market_df['Year'],
        y=market_df['Market Size (USD Billions)'],
        mode='lines+markers',
        name='Market Size',
        line=dict(color='#0A2540', width=3)
    ))
    
    # Growth rate bars
    fig.add_trace(go.Bar(
        x=market_df['Year'][1:],  # Skip first year as we don't have growth rate
        y=market_df['YoY Growth (%)'][1:],
        name='YoY Growth (%)',
        marker_color='#00A67E',
        yaxis='y2'
    ))
    
    # Add a line separating historical from forecast
    fig.add_vline(
        x=datetime.now().year - 0.5,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text="Forecast →",
        annotation_position="top right"
    )
    
    # Update layout with dual y-axis
    fig.update_layout(
        title='Market Size and Growth Projection',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Market Size (USD Billions)', side='left'),
        yaxis2=dict(
            title='YoY Growth (%)',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market segmentation and trends
    st.subheader("Market Segmentation Trends")
    
    # Example segments and their historical/projected market share
    segments = ['Segment A', 'Segment B', 'Segment C', 'Segment D', 'Segment E']
    periods = ['Previous Year', 'Current Year', 'Next Year', 'In 3 Years']
    
    # Generate random data for segment share evolution
    segment_data = []
    
    # Generate initial shares that sum to 100%
    initial_shares = [random.uniform(10, 40) for _ in range(len(segments) - 1)]
    initial_shares.append(100 - sum(initial_shares))
    
    for i, segment in enumerate(segments):
        # Ensure segment shares evolve somewhat realistically
        share_change_direction = random.choice([-1, 1, 1])  # Bias toward growth
        share_changes = [
            0,  # Previous year (base)
            random.uniform(-3, 5),  # Current year
            share_change_direction * random.uniform(1, 7),  # Next year
            share_change_direction * random.uniform(3, 15)  # In 3 years
        ]
        
        shares = [
            initial_shares[i],  # Previous year
            initial_shares[i] + share_changes[1],  # Current year
            initial_shares[i] + share_changes[1] + share_changes[2],  # Next year
            initial_shares[i] + share_changes[1] + share_changes[2] + share_changes[3]  # In 3 years
        ]
        
        for j, period in enumerate(periods):
            segment_data.append({
                'Segment': segment,
                'Period': period,
                'Market Share (%)': shares[j],
                'Period Num': j  # For sorting
            })
    
    # Create DataFrame
    segment_df = pd.DataFrame(segment_data)
    
    # Create area chart for segment evolution
    pivot_df = segment_df.pivot(index='Period Num', columns='Segment', values='Market Share (%)')
    pivot_df.index = periods
    
    # Normalize to ensure shares sum to 100% in each period
    for period in periods:
        period_shares = segment_df[segment_df['Period'] == period]['Market Share (%)'].values
        total = sum(period_shares)
        segment_df.loc[segment_df['Period'] == period, 'Market Share (%)'] *= 100 / total
    
    # Re-pivot with normalized values
    pivot_df = segment_df.pivot(index='Period', columns='Segment', values='Market Share (%)')
    
    # Create stacked area chart
    fig2 = px.area(
        pivot_df,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    )
    
    fig2.update_layout(
        title='Evolution of Market Segments',
        xaxis=dict(title=''),
        yaxis=dict(title='Market Share (%)', range=[0, 100]),
        legend=dict(title='Segment'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key market drivers
    st.subheader("Key Market Growth Drivers")
    
    # Example growth drivers
    growth_drivers = [
        "Technology Adoption",
        "Changing Consumer Preferences", 
        "Regulatory Changes",
        "Economic Factors",
        "Market Expansion",
        "Product Innovation"
    ]
    
    # Generate impact scores
    impact_scores = [random.uniform(5, 10) for _ in range(len(growth_drivers))]
    
    # Create DataFrame
    driver_df = pd.DataFrame({
        'Driver': growth_drivers,
        'Impact Score': impact_scores
    })
    
    # Sort by impact
    driver_df = driver_df.sort_values('Impact Score', ascending=False)
    
    # Create horizontal bar chart
    fig3 = px.bar(
        driver_df,
        y='Driver',
        x='Impact Score',
        orientation='h',
        color='Impact Score',
        color_continuous_scale='Blues',
        text=driver_df['Impact Score'].apply(lambda x: f"{x:.1f}")
    )
    
    fig3.update_layout(
        title='Impact of Market Growth Drivers',
        xaxis=dict(title='Impact Score (1-10)'),
        yaxis=dict(title=''),
        coloraxis_showscale=False,
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)

def render_technology_landscape_tab():
    """Renders the technology landscape visualization tab"""
    st.subheader("Technology Trend Assessment")
    
    # Example technology trends data
    technologies = [
        "Artificial Intelligence", 
        "Blockchain", 
        "IoT", 
        "5G Connectivity",
        "Quantum Computing",
        "AR/VR",
        "Cloud Computing",
        "Robotic Process Automation"
    ]
    
    # Generate data for S-curve position, impact, and timeline
    s_curve_positions = [random.uniform(0, 100) for _ in range(len(technologies))]
    impact_scores = [random.uniform(1, 10) for _ in range(len(technologies))]
    adoption_timelines = [random.randint(1, 7) for _ in range(len(technologies))]  # Years until mainstream
    
    # Create DataFrame
    tech_df = pd.DataFrame({
        'Technology': technologies,
        'S-Curve Position (%)': s_curve_positions,
        'Industry Impact': impact_scores,
        'Years to Mainstream': adoption_timelines
    })
    
    # Create S-curve scatter plot
    fig = px.scatter(
        tech_df,
        x='S-Curve Position (%)',
        y='Industry Impact',
        size='Industry Impact',
        color='Years to Mainstream',
        hover_name='Technology',
        text='Technology',
        color_continuous_scale='viridis_r',  # Reversed so shorter time is green
        size_max=45
    )
    
    # Add S-curve shape
    x = np.linspace(0, 100, 100)
    y = 10 / (1 + np.exp(-0.1 * (x - 50)))  # S-curve formula
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=dict(color='rgba(200, 200, 200, 0.3)', width=2, dash='dash'),
        name='Adoption Curve',
        hoverinfo='skip'
    ))
    
    # Add phase labels
    fig.add_annotation(x=15, y=9, text="Emerging", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=50, y=9, text="Growth", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=85, y=9, text="Mature", showarrow=False, font=dict(size=12))
    
    fig.update_layout(
        title='Technology Adoption S-Curve',
        xaxis=dict(title='Adoption Maturity', range=[0, 100]),
        yaxis=dict(title='Industry Impact (1-10)', range=[0, 10]),
        height=500
    )
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Technology impact assessment
    st.subheader("Technology Impact Matrix")
    
    # Create columns for top rated technologies
    top_techs = tech_df.sort_values('Industry Impact', ascending=False).head(3)
    cols = st.columns(3)
    
    for i, (_, tech) in enumerate(top_techs.iterrows()):
        with cols[i]:
            with st.container(border=True):
                st.subheader(tech['Technology'])
                
                impact_color = "green" if tech['Industry Impact'] > 7 else "orange" if tech['Industry Impact'] > 5 else "red"
                timeline_text = "Short-term" if tech['Years to Mainstream'] <= 2 else "Medium-term" if tech['Years to Mainstream'] <= 4 else "Long-term"
                
                st.markdown(f"**Impact Score:** <span style='color:{impact_color};'>{tech['Industry Impact']:.1f}/10</span>", unsafe_allow_html=True)
                st.markdown(f"**Adoption Timeline:** {timeline_text} ({tech['Years to Mainstream']} years)")
                st.markdown(f"**Maturity:** {tech['S-Curve Position (%)']:.0f}%")
                
                # Example impact areas
                st.markdown("**Primary Impact Areas:**")
                
                # Generate random impact areas based on the technology
                impact_areas = []
                if "AI" in tech['Technology'] or "Intelligence" in tech['Technology']:
                    impact_areas = ["Decision Automation", "Predictive Analytics", "Customer Experience"]
                elif "Blockchain" in tech['Technology']:
                    impact_areas = ["Supply Chain Transparency", "Smart Contracts", "Digital Identity"]
                elif "IoT" in tech['Technology']:
                    impact_areas = ["Operational Efficiency", "Predictive Maintenance", "Asset Tracking"]
                elif "5G" in tech['Technology']:
                    impact_areas = ["Real-time Communication", "Edge Computing", "High-bandwidth Applications"]
                elif "Quantum" in tech['Technology']:
                    impact_areas = ["Cryptography", "Complex Simulations", "Optimization Problems"]
                elif "AR/VR" in tech['Technology'] or "Augmented" in tech['Technology']:
                    impact_areas = ["Training & Simulation", "Remote Collaboration", "Customer Engagement"]
                elif "Cloud" in tech['Technology']:
                    impact_areas = ["Scalability", "Cost Optimization", "Global Accessibility"]
                elif "Automation" in tech['Technology'] or "RPA" in tech['Technology']:
                    impact_areas = ["Process Efficiency", "Error Reduction", "Resource Optimization"]
                else:
                    impact_areas = ["Operational Efficiency", "Customer Experience", "Business Model Innovation"]
                
                for area in impact_areas:
                    st.markdown(f"- {area}")
    
    # Technology convergence map
    st.subheader("Technology Convergence Analysis")
    
    # Example convergence relationships
    convergence_data = [
        {'from': 'Artificial Intelligence', 'to': 'IoT', 'strength': 0.8},
        {'from': 'Artificial Intelligence', 'to': 'Cloud Computing', 'strength': 0.7},
        {'from': 'Artificial Intelligence', 'to': 'Robotic Process Automation', 'strength': 0.9},
        {'from': '5G Connectivity', 'to': 'IoT', 'strength': 0.9},
        {'from': '5G Connectivity', 'to': 'AR/VR', 'strength': 0.7},
        {'from': 'Blockchain', 'to': 'IoT', 'strength': 0.5},
        {'from': 'Cloud Computing', 'to': 'IoT', 'strength': 0.6},
        {'from': 'Cloud Computing', 'to': '5G Connectivity', 'strength': 0.4},
        {'from': 'Quantum Computing', 'to': 'Artificial Intelligence', 'strength': 0.6}
    ]
    
    # Create network graph
    nodes = list(set([item['from'] for item in convergence_data] + [item['to'] for item in convergence_data]))
    
    # Create node positions
    import math
    node_positions = {}
    radius = 1
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / len(nodes)
        node_positions[node] = (radius * math.cos(angle), radius * math.sin(angle))
    
    # Create edge traces
    edge_traces = []
    for item in convergence_data:
        x0, y0 = node_positions[item['from']]
        x1, y1 = node_positions[item['to']]
        
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            line=dict(width=item['strength'] * 5, color='rgba(150, 150, 150, 0.8)'),
            hoverinfo='text',
            text=f"{item['from']} → {item['to']}: {item['strength'] * 10:.1f}/10 convergence",
            mode='lines'
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_trace = go.Scatter(
        x=[node_positions[node][0] for node in nodes],
        y=[node_positions[node][1] for node in nodes],
        mode='markers+text',
        text=nodes,
        textposition='middle center',
        marker=dict(
            size=20,
            color=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A0A0A0', '#E57373', '#81C784'],
            line=dict(width=2, color='white')
        ),
        hoverinfo='text'
    )
    
    # Create figure
    fig2 = go.Figure(data=edge_traces + [node_trace])
    
    fig2.update_layout(
        title='Technology Convergence Network',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)

def render_consumer_behavior_tab():
    """Renders the consumer behavior visualization tab"""
    st.subheader("Consumer Behavior Shifts")
    
    # Example consumer behavior trend data
    behavior_trends = [
        "Mobile-First Experience",
        "Sustainability Focus",
        "Personalization Demand",
        "Privacy Concerns",
        "Experience Over Ownership",
        "Social Commerce",
        "Voice & Visual Search",
        "Omnichannel Expectations"
    ]
    
    # Generate growth and impact data
    growth_rates = [random.uniform(10, 50) for _ in range(len(behavior_trends))]
    impact_scores = [random.uniform(3, 10) for _ in range(len(behavior_trends))]
    timeframes = [random.choice(["Short-term", "Medium-term", "Long-term"]) for _ in range(len(behavior_trends))]
    
    # Create DataFrame
    behavior_df = pd.DataFrame({
        'Trend': behavior_trends,
        'Growth Rate (% YoY)': growth_rates,
        'Business Impact': impact_scores,
        'Timeframe': timeframes
    })
    
    # Sort by business impact
    behavior_df = behavior_df.sort_values('Business Impact', ascending=False)
    
    # Color mapping for timeframes
    timeframe_colors = {
        "Short-term": "#00A67E",  # Green
        "Medium-term": "#FFD93D",  # Yellow
        "Long-term": "#FF6B6B"    # Red
    }
    
    # Create bubble chart
    fig = px.scatter(
        behavior_df,
        x='Growth Rate (% YoY)',
        y='Business Impact',
        size='Business Impact',
        color='Timeframe',
        text='Trend',
        color_discrete_map=timeframe_colors,
        size_max=45
    )
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig.update_layout(
        title='Consumer Behavior Trend Matrix',
        xaxis=dict(title='Growth Rate (% YoY)'),
        yaxis=dict(title='Business Impact (1-10)', range=[0, 10]),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Consumer preference shifts over time
    st.subheader("Consumer Preference Evolution")
    
    # Example preference data over time
    years = list(range(datetime.now().year - 3, datetime.now().year + 4))
    preferences = ["Preference A", "Preference B", "Preference C", "Preference D", "Preference E"]
    
    # Generate preference data over time
    preference_data = []
    
    for preference in preferences:
        # Define a starting point and trend direction for each preference
        start_value = random.uniform(10, 30)
        trend_direction = random.choice([-1, 1])
        trend_strength = random.uniform(0.1, 0.5)
        
        values = []
        current = start_value
        
        for year in years:
            # Add some randomness to the trend
            change = trend_direction * trend_strength * random.uniform(0.5, 1.5)
            current += change
            
            # Constrain to reasonable bounds
            current = max(5, min(40, current))
            
            values.append(current)
        
        preference_data.append({
            'Preference': preference,
            'Values': values
        })
    
    # Create DataFrame for visualization
    preference_df = pd.DataFrame()
    
    for i, year in enumerate(years):
        year_data = {'Year': year}
        
        for pref in preference_data:
            year_data[pref['Preference']] = pref['Values'][i]
        
        preference_df = pd.concat([preference_df, pd.DataFrame([year_data])])
    
    # Create line chart
    fig2 = go.Figure()
    
    color_palette = ['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    
    for i, preference in enumerate(preferences):
        fig2.add_trace(go.Scatter(
            x=preference_df['Year'],
            y=preference_df[preference],
            mode='lines+markers',
            name=preference,
            line=dict(color=color_palette[i % len(color_palette)], width=3)
        ))
    
    # Add a line separating historical from forecast
    fig2.add_vline(
        x=datetime.now().year - 0.5,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text="Forecast →",
        annotation_position="top right"
    )
    
    fig2.update_layout(
        title='Evolution of Consumer Preferences',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Preference Strength'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key demographic segment analysis
    st.subheader("Demographic Behavior Analysis")
    
    # Create columns for demographic segments
    col1, col2 = st.columns(2)
    
    with col1:
        # Age-based behavior differences
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
        behaviors = ['Online Shopping', 'Social Media Usage', 'Mobile Payments', 'Sustainability Focus']
        
        # Generate random scores for each age group and behavior
        age_behavior_data = []
        
        for behavior in behaviors:
            for age in age_groups:
                age_behavior_data.append({
                    'Age Group': age,
                    'Behavior': behavior,
                    'Adoption Rate (%)': random.uniform(20, 90)
                })
        
        # Create DataFrame
        age_df = pd.DataFrame(age_behavior_data)
        
        # Create heatmap
        pivot_df = age_df.pivot(index='Behavior', columns='Age Group', values='Adoption Rate (%)')
        
        fig3 = px.imshow(
            pivot_df,
            text_auto='.0f',
            color_continuous_scale='Blues',
            aspect='auto'
        )
        
        fig3.update_layout(
            title='Behavior Adoption by Age Group',
            xaxis=dict(title=''),
            yaxis=dict(title=''),
            height=300
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Urban vs. Suburban vs. Rural behavior differences
        locations = ['Urban', 'Suburban', 'Rural']
        behaviors = ['Online Shopping', 'Social Media Usage', 'Mobile Payments', 'Sustainability Focus']
        
        # Generate random scores for each location and behavior
        location_behavior_data = []
        
        for behavior in behaviors:
            for location in locations:
                location_behavior_data.append({
                    'Location': location,
                    'Behavior': behavior,
                    'Adoption Rate (%)': random.uniform(20, 90)
                })
        
        # Create DataFrame
        location_df = pd.DataFrame(location_behavior_data)
        
        # Create heatmap
        pivot_df = location_df.pivot(index='Behavior', columns='Location', values='Adoption Rate (%)')
        
        fig4 = px.imshow(
            pivot_df,
            text_auto='.0f',
            color_continuous_scale='Greens',
            aspect='auto'
        )
        
        fig4.update_layout(
            title='Behavior Adoption by Location Type',
            xaxis=dict(title=''),
            yaxis=dict(title=''),
            height=300
        )
        
        st.plotly_chart(fig4, use_container_width=True)

def render_competitive_shifts_tab():
    """Renders the competitive shifts visualization tab"""
    st.subheader("Competitive Landscape Evolution")
    
    # Example market share evolution data
    competitors = ['Company A', 'Company B', 'Company C', 'Company D', 'Others']
    years = list(range(datetime.now().year - 2, datetime.now().year + 4))
    
    # Generate market share data
    market_share_data = []
    
    # Generate initial market shares
    initial_shares = [random.uniform(10, 30) for _ in range(len(competitors) - 1)]
    initial_shares.append(100 - sum(initial_shares))  # Others
    
    for i, competitor in enumerate(competitors):
        # Define trend for each competitor
        trend_direction = random.choice([-1, 1, 1])  # Bias toward growth
        trend_strength = random.uniform(0.5, 2.0)
        
        shares = [initial_shares[i]]
        
        for year_idx in range(1, len(years)):
            # Previous year's share with trend and some randomness
            prev_share = shares[-1]
            change = trend_direction * trend_strength * random.uniform(0.5, 1.5)
            
            # Add constraints to keep shares reasonable
            # Stronger competitors shouldn't drop below 5%, weaker ones can go lower
            min_share = 5 if prev_share > 15 else 1
            
            new_share = max(min_share, prev_share + change)
            shares.append(new_share)
        
        for j, year in enumerate(years):
            market_share_data.append({
                'Competitor': competitor,
                'Year': year,
                'Market Share (%)': shares[j]
            })
    
    # Create DataFrame
    market_share_df = pd.DataFrame(market_share_data)
    
    # Normalize to ensure shares sum to 100% in each year
    for year in years:
        year_shares = market_share_df[market_share_df['Year'] == year]['Market Share (%)'].values
        total = sum(year_shares)
        market_share_df.loc[market_share_df['Year'] == year, 'Market Share (%)'] *= 100 / total
    
    # Create stacked area chart
    fig = px.area(
        market_share_df,
        x='Year',
        y='Market Share (%)',
        color='Competitor',
        groupnorm='percent',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    )
    
    # Add a line separating historical from forecast
    fig.add_vline(
        x=datetime.now().year - 0.5,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text="Forecast →",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Market Share Evolution',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Market Share (%)'),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Business model innovation trends
    st.subheader("Business Model Innovation Trends")
    
    # Example business model innovations
    business_models = [
        "Subscription/Recurring Revenue",
        "Platform/Marketplace",
        "Freemium",
        "Product-as-a-Service",
        "Data Monetization",
        "Outcome-based Pricing"
    ]
    
    # Generate random adoption and growth data
    current_adoption = [random.uniform(10, 60) for _ in range(len(business_models))]
    projected_growth = [random.uniform(5, 30) for _ in range(len(business_models))]
    
    # Create DataFrame
    model_df = pd.DataFrame({
        'Business Model': business_models,
        'Current Adoption (%)': current_adoption,
        'Projected Growth (% points)': projected_growth,
        'Future Adoption (%)': [min(100, curr + growth) for curr, growth in zip(current_adoption, projected_growth)]
    })
    
    # Sort by future adoption
    model_df = model_df.sort_values('Future Adoption (%)', ascending=False)
    
    # Create a bar chart showing current and future adoption
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        y=model_df['Business Model'],
        x=model_df['Current Adoption (%)'],
        name='Current Adoption',
        orientation='h',
        marker_color='#0A2540'
    ))
    
    fig2.add_trace(go.Bar(
        y=model_df['Business Model'],
        x=model_df['Projected Growth (% points)'],
        name='Projected Growth',
        orientation='h',
        marker_color='#00A67E',
        base=model_df['Current Adoption (%)']
    ))
    
    fig2.update_layout(
        title='Business Model Adoption Trends',
        xaxis=dict(title='Adoption Rate (%)'),
        yaxis=dict(title=''),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Innovation hotspots
    st.subheader("Competitive Innovation Hotspots")
    
    # Example innovation areas
    innovation_areas = [
        "AI/ML Integration",
        "User Experience",
        "Pricing Strategy",
        "Channel Innovation",
        "Supply Chain Optimization",
        "Sustainability",
        "Customer Insights"
    ]
    
    # Generate innovation activity levels
    activity_levels = [random.uniform(1, 10) for _ in range(len(innovation_areas))]
    success_rates = [random.uniform(30, 80) for _ in range(len(innovation_areas))]
    
    # Create DataFrame
    innovation_df = pd.DataFrame({
        'Area': innovation_areas,
        'Activity Level': activity_levels,
        'Success Rate (%)': success_rates
    })
    
    # Create bubble chart
    fig3 = px.scatter(
        innovation_df,
        x='Activity Level',
        y='Success Rate (%)',
        size='Activity Level',
        text='Area',
        color='Success Rate (%)',
        color_continuous_scale='RdYlGn',
        size_max=45
    )
    
    fig3.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig3.add_shape(
        type="rect",
        x0=5, y0=50, x1=10, y1=100,
        line=dict(color="rgba(0,166,126,0.3)"),
        fillcolor="rgba(0,166,126,0.1)"
    )
    
    fig3.add_annotation(
        x=7.5, y=75,
        text="High-Value Innovation Areas",
        showarrow=False,
        font=dict(size=12, color="#00A67E")
    )
    
    fig3.update_layout(
        title='Innovation Activity vs. Success Rate',
        xaxis=dict(title='Innovation Activity Level', range=[0, 10]),
        yaxis=dict(title='Success Rate (%)'),
        height=500
    )
    
    st.plotly_chart(fig3, use_container_width=True)