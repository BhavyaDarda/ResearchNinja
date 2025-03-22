import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render_customer_analysis(mode):
    """Renders the customer analysis visualization panel
    
    Args:
        mode (str): The analysis mode - either "Target Audience Segmentation" or "Customer Expectations"
    """
    
    if mode == "Target Audience Segmentation":
        st.header("Target Audience Segmentation Dashboard")
        render_audience_segmentation()
    else:
        st.header("Customer Expectations Analysis Dashboard")
        render_customer_expectations()
    
def render_audience_segmentation():
    """Renders the audience segmentation analysis"""
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask a target audience segmentation question to see analysis and insights here.")
        return
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Total Market Size",
            value=f"{random.randint(10, 100)}M",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Avg. Customer Value",
            value=f"${random.randint(50, 500)}",
            delta=f"{random.uniform(-5, 15):.1f}%"
        )
    
    with col3:
        st.metric(
            label="Segments Identified",
            value=f"{random.randint(3, 8)}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Primary Segment",
            value=f"Segment {random.choice(['A', 'B', 'C'])}",
            delta=None
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Segment Profiles", "Demographic Analysis", "Psychographic Analysis"])
    
    with tab1:
        render_segment_profiles_tab()
    
    with tab2:
        render_demographic_analysis_tab()
    
    with tab3:
        render_psychographic_analysis_tab()
    
    # Segmentation insights
    st.subheader("Key Audience Insights")
    
    # Extract the last assistant message for insights
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        
        # Take a relevant paragraph as insights
        paragraphs = last_message.split('\n\n')
        audience_paragraphs = [p for p in paragraphs if "audience" in p.lower() or "segment" in p.lower() or "customer" in p.lower()]
        if audience_paragraphs:
            insights = audience_paragraphs[0]
        else:
            insights = paragraphs[0] if paragraphs else last_message
        
        st.write(insights)
    else:
        st.write("No audience segmentation insights available yet. Ask a question to generate insights.")

def render_segment_profiles_tab():
    """Renders the customer segment profiles visualization tab"""
    st.subheader("Customer Segment Profiles")
    
    # Create example segment data
    segments = ['Segment A', 'Segment B', 'Segment C', 'Segment D']
    
    # Set up the grid of segments
    cols = st.columns(len(segments))
    
    # Example segment characteristics
    characteristics = {
        'Age Range': ['25-34', '35-44', '45-54', '18-24'],
        'Income Level': ['High', 'Medium', 'Medium-High', 'Low-Medium'],
        'Gender Split': ['60% F, 40% M', '45% F, 55% M', '50% F, 50% M', '65% F, 35% M'],
        'Primary Location': ['Urban', 'Suburban', 'Rural', 'Urban'],
        'Tech Adoption': ['Early Adopter', 'Mainstream', 'Late Majority', 'Early Adopter'],
        'Education': ['College+', 'High School+', 'Graduate+', 'College'],
        'Purchase Behavior': ['Frequent', 'Occasional', 'Planned', 'Impulsive'],
        'Price Sensitivity': ['Low', 'Medium', 'High', 'Medium-High']
    }
    
    # Generate random segment sizes
    segment_sizes = [random.uniform(15, 40) for _ in range(len(segments))]
    total = sum(segment_sizes)
    segment_percentages = [size * 100 / total for size in segment_sizes]
    
    # Display each segment in its column
    for i, (col, segment) in enumerate(zip(cols, segments)):
        with col:
            with st.container(border=True):
                st.subheader(segment)
                st.metric(
                    label="Market Share",
                    value=f"{segment_percentages[i]:.1f}%"
                )
                
                # Segment avatar/image placeholder
                st.markdown(f"""
                <div style="background-color:#f0f2f6; border-radius:50%; width:100px; height:100px; 
                display:flex; align-items:center; justify-content:center; margin:0 auto; font-size:24px; 
                color:#0A2540; font-weight:bold;">
                {segment[0]}
                </div>
                """, unsafe_allow_html=True)
                
                # Segment characteristics
                for key, values in characteristics.items():
                    st.markdown(f"**{key}:** {values[i]}")
                
                # Randomly determine if this is a primary segment
                is_primary = i == 0
                if is_primary:
                    st.markdown("**Primary Target:** ✅")
                else:
                    st.markdown("**Primary Target:** ❌")
    
    # Comparative segment analysis
    st.subheader("Comparative Segment Analysis")
    
    # Create example data for radar chart comparing segments
    categories = ['Purchasing Power', 'Brand Loyalty', 'Social Media Activity', 'Product Knowledge', 'Influence']
    
    # Generate random ratings for each segment and category
    segment_ratings = {}
    for segment in segments:
        segment_ratings[segment] = [random.uniform(1, 10) for _ in range(len(categories))]
    
    # Create a DataFrame for the radar chart
    df_radar = pd.DataFrame()
    for segment in segments:
        segment_df = pd.DataFrame({
            'Segment': [segment] * len(categories),
            'Category': categories,
            'Rating': segment_ratings[segment]
        })
        df_radar = pd.concat([df_radar, segment_df])
    
    # Create and display radar chart
    fig = px.line_polar(
        df_radar, r='Rating', theta='Category', color='Segment', line_close=True,
        range_r=[0, 10],
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D']
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_demographic_analysis_tab():
    """Renders the demographic analysis visualization tab"""
    st.subheader("Demographic Analysis")
    
    # Create columns for different demographic visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        st.subheader("Age Distribution")
        
        # Example age data
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        age_distribution = [random.uniform(5, 25) for _ in range(len(age_groups))]
        
        # Normalize to 100%
        total = sum(age_distribution)
        age_distribution = [val * 100 / total for val in age_distribution]
        
        # Create DataFrame
        age_df = pd.DataFrame({
            'Age Group': age_groups,
            'Percentage': age_distribution
        })
        
        # Create bar chart
        fig1 = px.bar(
            age_df,
            x='Age Group',
            y='Percentage',
            text_auto='.1f',
            labels={'Percentage': 'Percentage (%)'},
            color='Percentage',
            color_continuous_scale='Blues'
        )
        
        fig1.update_layout(
            xaxis=dict(title='Age Group'),
            yaxis=dict(title='Percentage (%)'),
            coloraxis_showscale=False,
            height=350
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Income distribution
        st.subheader("Income Distribution")
        
        # Example income data
        income_groups = ['Under $25k', '$25k-$50k', '$50k-$75k', '$75k-$100k', '$100k+']
        income_distribution = [random.uniform(5, 30) for _ in range(len(income_groups))]
        
        # Normalize to 100%
        total = sum(income_distribution)
        income_distribution = [val * 100 / total for val in income_distribution]
        
        # Create DataFrame
        income_df = pd.DataFrame({
            'Income Group': income_groups,
            'Percentage': income_distribution
        })
        
        # Create bar chart
        fig2 = px.bar(
            income_df,
            x='Income Group',
            y='Percentage',
            text_auto='.1f',
            labels={'Percentage': 'Percentage (%)'},
            color='Percentage',
            color_continuous_scale='Greens'
        )
        
        fig2.update_layout(
            xaxis=dict(title='Income Group'),
            yaxis=dict(title='Percentage (%)'),
            coloraxis_showscale=False,
            height=350
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Geographic distribution
    st.subheader("Geographic Distribution")
    
    # Example geographic data
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    geo_distribution = [random.uniform(10, 40) for _ in range(len(regions))]
    
    # Normalize to 100%
    total = sum(geo_distribution)
    geo_distribution = [val * 100 / total for val in geo_distribution]
    
    # Create DataFrame
    geo_df = pd.DataFrame({
        'Region': regions,
        'Percentage': geo_distribution
    })
    
    # Create pie chart
    fig3 = px.pie(
        geo_df,
        values='Percentage',
        names='Region',
        hole=0.4,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    )
    
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    
    fig3.update_layout(
        title='Geographic Distribution',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Urban vs. Suburban vs. Rural
    st.subheader("Urban vs. Suburban vs. Rural")
    
    # Example data
    location_types = ['Urban', 'Suburban', 'Rural']
    location_distribution = [random.uniform(20, 50) for _ in range(len(location_types))]
    
    # Normalize to 100%
    total = sum(location_distribution)
    location_distribution = [val * 100 / total for val in location_distribution]
    
    # Create DataFrame
    location_df = pd.DataFrame({
        'Location Type': location_types,
        'Percentage': location_distribution
    })
    
    # Create donut chart
    fig4 = px.pie(
        location_df,
        values='Percentage',
        names='Location Type',
        hole=0.6,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B']
    )
    
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    
    fig4.update_layout(
        height=300
    )
    
    st.plotly_chart(fig4, use_container_width=True)

def render_psychographic_analysis_tab():
    """Renders the psychographic analysis visualization tab"""
    st.subheader("Psychographic Analysis")
    
    # Create columns for different psychographic visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Values and Interests
        st.subheader("Values & Interests")
        
        # Example values data
        values = ['Innovation', 'Tradition', 'Community', 'Achievement', 'Self-expression', 'Security']
        value_scores = [random.uniform(1, 10) for _ in range(len(values))]
        
        # Create DataFrame
        values_df = pd.DataFrame({
            'Value': values,
            'Score': value_scores
        })
        
        # Sort by score
        values_df = values_df.sort_values('Score', ascending=False)
        
        # Create horizontal bar chart
        fig1 = px.bar(
            values_df,
            y='Value',
            x='Score',
            orientation='h',
            color='Score',
            color_continuous_scale='Blues',
            text_auto='.1f'
        )
        
        fig1.update_layout(
            xaxis=dict(title='Importance Score (1-10)'),
            yaxis=dict(title=''),
            coloraxis_showscale=False,
            height=400
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Lifestyle Factors
        st.subheader("Lifestyle Factors")
        
        # Example lifestyle data
        lifestyles = ['Tech-savvy', 'Fitness-oriented', 'Environmentally conscious', 
                       'Family-focused', 'Career-driven', 'Travel enthusiast']
        lifestyle_scores = [random.uniform(1, 10) for _ in range(len(lifestyles))]
        
        # Create DataFrame
        lifestyle_df = pd.DataFrame({
            'Lifestyle': lifestyles,
            'Score': lifestyle_scores
        })
        
        # Sort by score
        lifestyle_df = lifestyle_df.sort_values('Score', ascending=False)
        
        # Create horizontal bar chart
        fig2 = px.bar(
            lifestyle_df,
            y='Lifestyle',
            x='Score',
            orientation='h',
            color='Score',
            color_continuous_scale='Greens',
            text_auto='.1f'
        )
        
        fig2.update_layout(
            xaxis=dict(title='Prevalence Score (1-10)'),
            yaxis=dict(title=''),
            coloraxis_showscale=False,
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Buying Behavior Analysis
    st.subheader("Buying Behavior Analysis")
    
    # Create columns for different aspects of buying behavior
    col3, col4 = st.columns(2)
    
    with col3:
        # Purchase Drivers
        st.subheader("Purchase Drivers")
        
        # Example purchase drivers
        drivers = ['Price', 'Quality', 'Brand Reputation', 'Convenience', 'Features/Technology', 'Customer Service']
        driver_scores = [random.uniform(1, 10) for _ in range(len(drivers))]
        
        # Create DataFrame
        drivers_df = pd.DataFrame({
            'Driver': drivers,
            'Importance': driver_scores
        })
        
        # Create radar chart
        fig3 = px.line_polar(
            drivers_df, r='Importance', theta='Driver', line_close=True,
            range_r=[0, 10],
            color_discrete_sequence=['#0A2540']
        )
        
        fig3.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Channel Preferences
        st.subheader("Channel Preferences")
        
        # Example channel data
        channels = ['Online / E-commerce', 'Retail Stores', 'Mobile Apps', 'Social Commerce', 'Marketplace', 'Direct Sales']
        channel_percentages = [random.uniform(5, 30) for _ in range(len(channels))]
        
        # Normalize to 100%
        total = sum(channel_percentages)
        channel_percentages = [val * 100 / total for val in channel_percentages]
        
        # Create DataFrame
        channels_df = pd.DataFrame({
            'Channel': channels,
            'Percentage': channel_percentages
        })
        
        # Create pie chart
        fig4 = px.pie(
            channels_df,
            values='Percentage',
            names='Channel',
            color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A9A9A9']
        )
        
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        
        fig4.update_layout(
            height=400
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # Social Media Platform Usage
    st.subheader("Social Media Platform Usage")
    
    # Example social media data
    platforms = ['Facebook', 'Instagram', 'TikTok', 'Twitter', 'LinkedIn', 'YouTube', 'Pinterest', 'Reddit']
    platform_usage = [random.uniform(10, 80) for _ in range(len(platforms))]
    
    # Create DataFrame
    social_df = pd.DataFrame({
        'Platform': platforms,
        'Usage (%)': platform_usage
    })
    
    # Sort by usage
    social_df = social_df.sort_values('Usage (%)', ascending=False)
    
    # Create bar chart
    fig5 = px.bar(
        social_df,
        x='Platform',
        y='Usage (%)',
        color='Usage (%)',
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    
    fig5.update_layout(
        xaxis=dict(title='Platform'),
        yaxis=dict(title='Usage (%)'),
        coloraxis_showscale=False,
        height=400
    )
    
    st.plotly_chart(fig5, use_container_width=True)

def render_customer_expectations():
    """Renders the customer expectations analysis"""
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask a customer expectations question to see analysis and insights here.")
        return
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Satisfaction Score",
            value=f"{random.uniform(7, 9.5):.1f}/10",
            delta=f"{random.uniform(-1, 1):.1f}"
        )
    
    with col2:
        st.metric(
            label="Unmet Needs",
            value=f"{random.randint(3, 8)}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Feature Requests",
            value=f"{random.randint(10, 50)}",
            delta=f"{random.randint(1, 10)}"
        )
    
    with col4:
        st.metric(
            label="NPS",
            value=f"{random.randint(20, 70)}",
            delta=f"{random.uniform(-10, 10):.1f}"
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Feature Demand", "Expectations Gap", "Satisfaction Analysis"])
    
    with tab1:
        render_feature_demand_tab()
    
    with tab2:
        render_expectations_gap_tab()
    
    with tab3:
        render_satisfaction_analysis_tab()
    
    # Expectations insights
    st.subheader("Customer Expectations Insights")
    
    # Extract the last assistant message for insights
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        
        # Take a relevant paragraph as insights
        paragraphs = last_message.split('\n\n')
        expectation_paragraphs = [p for p in paragraphs if "expect" in p.lower() or "need" in p.lower() or "want" in p.lower()]
        if expectation_paragraphs:
            insights = expectation_paragraphs[0]
        else:
            insights = paragraphs[0] if paragraphs else last_message
        
        st.write(insights)
    else:
        st.write("No customer expectations insights available yet. Ask a question to generate insights.")

def render_feature_demand_tab():
    """Renders the feature demand visualization tab"""
    st.subheader("Feature Demand Analysis")
    
    # Example feature demand data
    features = [
        "Advanced Analytics", "Mobile Integration", "Social Sharing", 
        "Customization Options", "API Access", "Automation Tools",
        "Interactive Dashboard", "Real-time Updates", "Team Collaboration",
        "Integration with Other Tools"
    ]
    
    demand_scores = [random.uniform(1, 10) for _ in range(len(features))]
    development_complexity = [random.uniform(1, 10) for _ in range(len(features))]
    
    # Calculate priority score (demand / complexity)
    priority_scores = [demand_scores[i] / development_complexity[i] * 3 for i in range(len(features))]
    
    # Create DataFrame
    feature_df = pd.DataFrame({
        'Feature': features,
        'Demand Score': demand_scores,
        'Development Complexity': development_complexity,
        'Priority Score': priority_scores
    })
    
    # Sort by priority score
    feature_df = feature_df.sort_values('Priority Score', ascending=False)
    
    # Create scatter plot
    fig = px.scatter(
        feature_df,
        x='Development Complexity',
        y='Demand Score',
        size='Priority Score',
        color='Priority Score',
        text='Feature',
        size_max=50,
        color_continuous_scale='Viridis'
    )
    
    # Add quadrant lines
    fig.add_shape(
        type="line",
        x0=5, y0=0, x1=5, y1=10,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=0, y0=5, x1=10, y1=5,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    # Add quadrant labels
    fig.add_annotation(x=2.5, y=7.5, text="Quick Wins",
                      showarrow=False, font=dict(size=14, color="green"))
    fig.add_annotation(x=7.5, y=7.5, text="Major Projects",
                      showarrow=False, font=dict(size=14, color="blue"))
    fig.add_annotation(x=2.5, y=2.5, text="Low Priority",
                      showarrow=False, font=dict(size=14, color="gray"))
    fig.add_annotation(x=7.5, y=2.5, text="Thankless Tasks",
                      showarrow=False, font=dict(size=14, color="red"))
    
    fig.update_layout(
        title='Feature Prioritization Matrix',
        xaxis=dict(title='Development Complexity', range=[0, 10]),
        yaxis=dict(title='Customer Demand', range=[0, 10]),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top requested features table
    st.subheader("Top Requested Features")
    
    # Display top 5 features by demand
    top_features = feature_df.sort_values('Demand Score', ascending=False).head(5)
    
    # Format table
    formatted_top_features = top_features.copy()
    formatted_top_features['Demand Score'] = formatted_top_features['Demand Score'].apply(lambda x: f"{x:.1f}/10")
    formatted_top_features['Development Complexity'] = formatted_top_features['Development Complexity'].apply(lambda x: f"{x:.1f}/10")
    formatted_top_features['Priority Score'] = formatted_top_features['Priority Score'].apply(lambda x: f"{x:.2f}")
    
    # Display table
    st.dataframe(
        formatted_top_features[['Feature', 'Demand Score', 'Development Complexity', 'Priority Score']],
        use_container_width=True
    )

def render_expectations_gap_tab():
    """Renders the expectations gap visualization tab"""
    st.subheader("Expectations vs. Reality Gap Analysis")
    
    # Example dimensions to measure
    dimensions = [
        "Ease of Use", "Customer Support", "Feature Set", "Performance/Speed",
        "Reliability", "Value for Money", "Design/UI", "Integration Capabilities"
    ]
    
    # Generate random scores for customer expectations and current reality
    expectation_scores = [random.uniform(7, 10) for _ in range(len(dimensions))]
    reality_scores = [random.uniform(3, 9.5) for _ in range(len(dimensions))]
    
    # Calculate gaps
    gaps = [expectation_scores[i] - reality_scores[i] for i in range(len(dimensions))]
    
    # Create DataFrame
    gap_df = pd.DataFrame({
        'Dimension': dimensions,
        'Expected': expectation_scores,
        'Reality': reality_scores,
        'Gap': gaps
    })
    
    # Sort by gap size
    gap_df = gap_df.sort_values('Gap', ascending=False)
    
    # Create a bar chart showing expectations vs. reality
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=gap_df['Dimension'],
        x=gap_df['Expected'],
        name='Expected',
        orientation='h',
        marker_color='#0A2540'
    ))
    
    fig.add_trace(go.Bar(
        y=gap_df['Dimension'],
        x=gap_df['Reality'],
        name='Reality',
        orientation='h',
        marker_color='#00A67E'
    ))
    
    # Update layout
    fig.update_layout(
        title='Customer Expectations vs. Reality',
        xaxis=dict(title='Score (0-10)'),
        yaxis=dict(title=''),
        barmode='overlay',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display gap analysis table
    st.subheader("Expectations Gap Analysis")
    
    # Format table
    formatted_gap_df = gap_df.copy()
    formatted_gap_df['Expected'] = formatted_gap_df['Expected'].apply(lambda x: f"{x:.1f}")
    formatted_gap_df['Reality'] = formatted_gap_df['Reality'].apply(lambda x: f"{x:.1f}")
    formatted_gap_df['Gap'] = formatted_gap_df['Gap'].apply(lambda x: f"{x:.1f}")
    
    # Add gap classification
    def classify_gap(gap):
        if gap > 3:
            return "Critical"
        elif gap > 1.5:
            return "Significant"
        elif gap > 0.5:
            return "Moderate"
        else:
            return "Minimal"
    
    formatted_gap_df['Classification'] = gap_df['Gap'].apply(classify_gap)
    
    # Display table
    st.dataframe(
        formatted_gap_df[['Dimension', 'Expected', 'Reality', 'Gap', 'Classification']],
        use_container_width=True
    )
    
    # Display action recommendations for top gaps
    st.subheader("Recommended Actions")
    
    # Take top 3 gaps
    top_gaps = gap_df.head(3)
    
    for i, row in top_gaps.iterrows():
        dimension = row['Dimension']
        gap = row['Gap']
        
        with st.container(border=True):
            cols = st.columns([1, 5])
            
            with cols[0]:
                # Display a visual indicator of the gap severity
                if gap > 3:
                    st.markdown("🔴")
                    severity = "Critical"
                elif gap > 1.5:
                    st.markdown("🟠")
                    severity = "Significant"
                else:
                    st.markdown("🟡")
                    severity = "Moderate"
                
                st.markdown(f"**{severity}**")
                st.markdown(f"Gap: **{gap:.1f}**")
            
            with cols[1]:
                st.subheader(dimension)
                st.markdown("**Recommended Action:**")
                
                # Generate example recommendations based on the dimension
                if dimension == "Ease of Use":
                    st.markdown("- Conduct usability testing to identify friction points")
                    st.markdown("- Simplify user interface and streamline workflows")
                    st.markdown("- Develop better onboarding and in-app guidance")
                elif dimension == "Customer Support":
                    st.markdown("- Expand support team availability and channels")
                    st.markdown("- Improve response times and resolution rates")
                    st.markdown("- Develop self-service knowledge base and community forums")
                elif dimension == "Feature Set":
                    st.markdown("- Prioritize development of most requested features")
                    st.markdown("- Conduct competitive analysis to identify feature gaps")
                    st.markdown("- Create a public product roadmap to set expectations")
                else:
                    st.markdown("- Conduct detailed research to understand specific pain points")
                    st.markdown("- Benchmark against industry leaders to identify improvement areas")
                    st.markdown("- Develop specific metrics to track improvements")

def render_satisfaction_analysis_tab():
    """Renders the satisfaction analysis visualization tab"""
    st.subheader("Customer Satisfaction Analysis")
    
    # Example time-series data for satisfaction trends
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    csat_scores = [random.uniform(7, 9) for _ in range(len(months))]
    nps_scores = [random.uniform(30, 70) for _ in range(len(months))]
    
    # Create DataFrame
    satisfaction_df = pd.DataFrame({
        'Date': months,
        'CSAT Score': csat_scores,
        'NPS': nps_scores
    })
    
    # Create line chart with dual y-axis
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=satisfaction_df['Date'],
        y=satisfaction_df['CSAT Score'],
        name='CSAT Score',
        line=dict(color='#0A2540', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=satisfaction_df['Date'],
        y=satisfaction_df['NPS'],
        name='NPS',
        line=dict(color='#00A67E', width=3),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title='Satisfaction Trends',
        xaxis=dict(title=''),
        yaxis=dict(title='CSAT Score (0-10)', range=[0, 10]),
        yaxis2=dict(title='NPS (-100 to 100)', range=[0, 100], overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Customer feedback sentiment analysis
    st.subheader("Feedback Sentiment Analysis")
    
    # Example sentiment data
    sentiments = ['Positive', 'Neutral', 'Negative']
    sentiment_counts = [random.randint(50, 200), random.randint(20, 100), random.randint(10, 50)]
    
    # Calculate percentages
    total_sentiments = sum(sentiment_counts)
    sentiment_percentages = [count * 100 / total_sentiments for count in sentiment_counts]
    
    # Create DataFrame
    sentiment_df = pd.DataFrame({
        'Sentiment': sentiments,
        'Count': sentiment_counts,
        'Percentage': sentiment_percentages
    })
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create donut chart
        fig2 = px.pie(
            sentiment_df,
            values='Count',
            names='Sentiment',
            hole=0.6,
            color='Sentiment',
            color_discrete_map={
                'Positive': '#00A67E',
                'Neutral': '#FFD93D',
                'Negative': '#FF6B6B'
            }
        )
        
        fig2.update_traces(textposition='inside', textinfo='percent')
        
        fig2.update_layout(
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Topic-based sentiment analysis
        topics = ['Pricing', 'Features', 'Usability', 'Performance', 'Support']
        
        # Generate random sentiment counts for each topic
        topic_sentiment_data = []
        
        for topic in topics:
            pos = random.randint(10, 100)
            neu = random.randint(5, 50)
            neg = random.randint(1, 30)
            total = pos + neu + neg
            
            topic_sentiment_data.append({
                'Topic': topic,
                'Positive': pos,
                'Neutral': neu,
                'Negative': neg,
                'Positive %': pos * 100 / total,
                'Neutral %': neu * 100 / total,
                'Negative %': neg * 100 / total
            })
        
        # Create DataFrame
        topic_df = pd.DataFrame(topic_sentiment_data)
        
        # Create stacked bar chart
        fig3 = go.Figure()
        
        fig3.add_trace(go.Bar(
            y=topic_df['Topic'],
            x=topic_df['Positive %'],
            name='Positive',
            orientation='h',
            marker_color='#00A67E'
        ))
        
        fig3.add_trace(go.Bar(
            y=topic_df['Topic'],
            x=topic_df['Neutral %'],
            name='Neutral',
            orientation='h',
            marker_color='#FFD93D'
        ))
        
        fig3.add_trace(go.Bar(
            y=topic_df['Topic'],
            x=topic_df['Negative %'],
            name='Negative',
            orientation='h',
            marker_color='#FF6B6B'
        ))
        
        # Update layout
        fig3.update_layout(
            title='Sentiment by Topic',
            xaxis=dict(title='Percentage (%)'),
            yaxis=dict(title=''),
            barmode='stack',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            height=300
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    # Common feedback themes
    st.subheader("Common Feedback Themes")
    
    # Example feedback themes
    positive_themes = ["Easy to use interface", "Great customer support", "Time-saving features", "Reliable performance"]
    negative_themes = ["Missing advanced features", "Price is too high", "Learning curve is steep", "Limited integrations"]
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### Positive Themes")
        for i, theme in enumerate(positive_themes):
            st.markdown(f"**{i+1}.** {theme}")
    
    with col4:
        st.markdown("### Areas for Improvement")
        for i, theme in enumerate(negative_themes):
            st.markdown(f"**{i+1}.** {theme}")
