import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render_regulatory_analysis():
    """Renders the regulatory and compliance analysis visualization panel"""
    
    st.header("Regulatory & Compliance Analysis Dashboard")
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask a regulatory compliance question to see analysis and insights here.")
        return
    
    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Regulatory Risk Score",
            value=f"{random.randint(25, 75)}/100",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Key Regulations",
            value=f"{random.randint(3, 12)}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Compliance Effort",
            value=f"{random.choice(['Medium', 'High', 'Low'])}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Regulatory Changes",
            value=f"{random.choice(['Increasing', 'Stable', 'Evolving'])}",
            delta=None
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Regulatory Landscape", "Compliance Requirements", "Regional Comparison"])
    
    with tab1:
        render_regulatory_landscape_tab()
    
    with tab2:
        render_compliance_requirements_tab()
    
    with tab3:
        render_regional_comparison_tab()
    
    # Regulatory insights
    st.subheader("Key Regulatory Insights")
    
    # Extract the last assistant message for insights
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        
        # Take a relevant paragraph as insights
        paragraphs = last_message.split('\n\n')
        regulatory_paragraphs = [p for p in paragraphs if "regulat" in p.lower() or "compliance" in p.lower() or "legal" in p.lower()]
        if regulatory_paragraphs:
            insights = regulatory_paragraphs[0]
        else:
            insights = paragraphs[0] if paragraphs else last_message
        
        st.write(insights)
    else:
        st.write("No regulatory analysis insights available yet. Ask a question to generate insights.")

def render_regulatory_landscape_tab():
    """Renders the regulatory landscape visualization tab"""
    st.subheader("Key Regulatory Framework Overview")
    
    # Example regulatory data
    regulations = [
        "Regulation A",
        "Regulation B",
        "Regulation C",
        "Regulation D",
        "Regulation E",
        "Regulation F"
    ]
    
    # Generate random impact and complexity scores
    impact_scores = [random.uniform(1, 10) for _ in range(len(regulations))]
    complexity_scores = [random.uniform(1, 10) for _ in range(len(regulations))]
    
    # Determine status based on how recent (newer ones more likely to be pending)
    status_options = ["Active", "Pending", "Proposed", "Under Review"]
    status_weights = [0.6, 0.2, 0.1, 0.1]
    statuses = [np.random.choice(status_options, p=status_weights) for _ in range(len(regulations))]
    
    # Create DataFrame
    reg_df = pd.DataFrame({
        'Regulation': regulations,
        'Business Impact': impact_scores,
        'Compliance Complexity': complexity_scores,
        'Status': statuses
    })
    
    # Create scatter plot for regulatory matrix
    fig = px.scatter(
        reg_df,
        x='Compliance Complexity',
        y='Business Impact',
        color='Status',
        size=[8] * len(reg_df),  # Constant size
        text='Regulation',
        color_discrete_map={
            'Active': '#00A67E',
            'Pending': '#FFD93D',
            'Proposed': '#6082B6',
            'Under Review': '#FF6B6B'
        }
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
    fig.add_annotation(x=2.5, y=7.5, text="High Impact, Low Complexity",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=7.5, y=7.5, text="Critical Attention",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=2.5, y=2.5, text="Lower Priority",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=7.5, y=2.5, text="Complex, Lower Impact",
                      showarrow=False, font=dict(size=12))
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig.update_layout(
        title='Regulatory Impact vs. Compliance Complexity',
        xaxis=dict(title='Compliance Complexity', range=[0, 10]),
        yaxis=dict(title='Business Impact', range=[0, 10]),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regulatory timeline
    st.subheader("Regulatory Timeline")
    
    # Example timeline data
    timeline_events = [
        {"Regulation": "Regulation A", "Event": "Implementation Deadline", "Date": datetime.now() + timedelta(days=random.randint(30, 180))},
        {"Regulation": "Regulation B", "Event": "Public Comment Period", "Date": datetime.now() + timedelta(days=random.randint(-60, -30))},
        {"Regulation": "Regulation C", "Event": "Final Rule Publication", "Date": datetime.now() + timedelta(days=random.randint(-120, -90))},
        {"Regulation": "Regulation D", "Event": "Enforcement Begins", "Date": datetime.now() + timedelta(days=random.randint(60, 90))},
        {"Regulation": "Regulation E", "Event": "Regulatory Review", "Date": datetime.now() + timedelta(days=random.randint(120, 240))},
        {"Regulation": "Regulation F", "Event": "Initial Announcement", "Date": datetime.now() + timedelta(days=random.randint(-180, -150))}
    ]
    
    # Create DataFrame
    timeline_df = pd.DataFrame(timeline_events)
    
    # Sort by date
    timeline_df = timeline_df.sort_values('Date')
    
    # Assign colors based on date (future/past)
    timeline_df['Color'] = timeline_df['Date'].apply(
        lambda x: '#00A67E' if x > datetime.now() else '#6082B6'
    )
    
    # Create timeline visualization
    fig2 = go.Figure()
    
    for i, row in timeline_df.iterrows():
        fig2.add_trace(go.Scatter(
            x=[row['Date']],
            y=[row['Regulation']],
            mode='markers+text',
            marker=dict(size=15, color=row['Color']),
            text=row['Event'],
            textposition='middle right',
            textfont=dict(size=12),
            name=row['Event']
        ))
    
    # Add a line for the current date
    fig2.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="#FF6B6B",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    fig2.update_layout(
        title='Key Regulatory Dates & Deadlines',
        xaxis=dict(title=''),
        yaxis=dict(title='', categoryorder='array', categoryarray=timeline_df['Regulation'].unique()),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Regulatory trend analysis
    st.subheader("Regulatory Trend Analysis")
    
    # Example trend data over time
    years = list(range(datetime.now().year - 3, datetime.now().year + 4))
    regulatory_categories = ["Data Privacy", "Consumer Protection", "Financial Reporting", "Environmental"]
    
    # Generate trend data
    trend_data = []
    
    for category in regulatory_categories:
        # Define trend direction and starting point
        start_value = random.randint(5, 20)
        trend_direction = random.choice([0.5, 1, 1.5])  # Mostly increasing
        
        values = []
        current = start_value
        
        for year in years:
            # Add some randomness to the trend
            if year >= datetime.now().year:
                # Future predictions more variable
                change = trend_direction * random.uniform(0.8, 2.0)
            else:
                # Historical data more consistent
                change = trend_direction * random.uniform(0.5, 1.5)
            
            current += change
            values.append(current)
        
        for i, year in enumerate(years):
            trend_data.append({
                'Year': year,
                'Category': category,
                'Regulatory Activity': values[i]
            })
    
    # Create DataFrame
    trend_df = pd.DataFrame(trend_data)
    
    # Create line chart
    fig3 = px.line(
        trend_df,
        x='Year',
        y='Regulatory Activity',
        color='Category',
        markers=True,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D']
    )
    
    # Add a line separating historical from forecast
    fig3.add_vline(
        x=datetime.now().year - 0.5,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text="Forecast →",
        annotation_position="top right"
    )
    
    fig3.update_layout(
        title='Regulatory Activity Trends by Category',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Regulatory Activity Index'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)

def render_compliance_requirements_tab():
    """Renders the compliance requirements visualization tab"""
    st.subheader("Compliance Requirements Analysis")
    
    # Example compliance categories and requirements
    compliance_categories = [
        "Data Protection & Privacy",
        "Financial Reporting",
        "Consumer Rights",
        "Environmental Compliance",
        "Health & Safety",
        "Employment Law"
    ]
    
    # Generate random complexity and implementation status
    complexity_scores = [random.uniform(1, 10) for _ in range(len(compliance_categories))]
    implementation_scores = [random.uniform(0, 100) for _ in range(len(compliance_categories))]
    
    # Create DataFrame
    compliance_df = pd.DataFrame({
        'Category': compliance_categories,
        'Complexity': complexity_scores,
        'Implementation (%)': implementation_scores
    })
    
    # Sort by implementation percentage
    compliance_df = compliance_df.sort_values('Implementation (%)')
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Implementation bars
    fig.add_trace(go.Bar(
        y=compliance_df['Category'],
        x=compliance_df['Implementation (%)'],
        orientation='h',
        marker_color='#00A67E',
        name='Implemented'
    ))
    
    # Remaining work
    fig.add_trace(go.Bar(
        y=compliance_df['Category'],
        x=100 - compliance_df['Implementation (%)'],
        orientation='h',
        marker_color='#FF6B6B',
        name='Remaining'
    ))
    
    fig.update_layout(
        title='Compliance Implementation Status',
        xaxis=dict(title='Implementation Percentage'),
        yaxis=dict(title=''),
        barmode='stack',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed compliance requirements
    st.subheader("Key Compliance Requirements")
    
    # Display top 3 categories with detailed requirements
    top_categories = compliance_df.sort_values('Complexity', ascending=False).head(3)
    
    for i, row in top_categories.iterrows():
        category = row['Category']
        
        with st.container(border=True):
            cols = st.columns([1, 4])
            
            with cols[0]:
                # Display complexity score
                complexity_color = "red" if row['Complexity'] > 7 else "orange" if row['Complexity'] > 5 else "green"
                st.metric(
                    label="Complexity",
                    value=f"{row['Complexity']:.1f}/10"
                )
                st.markdown(f"**Implementation:**")
                st.progress(row['Implementation (%)']/100)
                st.markdown(f"{row['Implementation (%)']:.1f}%")
            
            with cols[1]:
                st.subheader(category)
                
                # Generate example requirements based on the category
                if "Data" in category:
                    requirements = [
                        "Data collection consent requirements",
                        "Data subject access rights implementation",
                        "Cross-border data transfer restrictions",
                        "Data breach notification processes"
                    ]
                elif "Financial" in category:
                    requirements = [
                        "Quarterly financial reporting standards",
                        "Revenue recognition guidelines",
                        "Tax compliance documentation",
                        "Financial controls implementation"
                    ]
                elif "Consumer" in category:
                    requirements = [
                        "Service terms and conditions transparency",
                        "Cooling-off period implementation",
                        "Fair marketing practice guidelines",
                        "Complaint handling procedures"
                    ]
                elif "Environmental" in category:
                    requirements = [
                        "Emissions reporting and reduction",
                        "Waste management procedures",
                        "Environmental impact assessment",
                        "Sustainability reporting standards"
                    ]
                elif "Health" in category:
                    requirements = [
                        "Workplace safety assessment",
                        "Safety training documentation",
                        "Incident reporting procedures",
                        "Health monitoring requirements"
                    ]
                elif "Employment" in category:
                    requirements = [
                        "Worker classification compliance",
                        "Working hours and overtime tracking",
                        "Anti-discrimination policies",
                        "Employee data protection"
                    ]
                else:
                    requirements = [
                        "Requirement 1",
                        "Requirement 2",
                        "Requirement 3",
                        "Requirement 4"
                    ]
                
                for req in requirements:
                    st.markdown(f"- {req}")
    
    # Compliance cost and resource analysis
    st.subheader("Compliance Resource Requirements")
    
    # Example compliance cost data
    cost_categories = ['Technology', 'Personnel', 'Training', 'External Expertise', 'Documentation', 'Ongoing Monitoring']
    cost_values = [random.uniform(10000, 100000) for _ in range(len(cost_categories))]
    
    # Create DataFrame
    cost_df = pd.DataFrame({
        'Category': cost_categories,
        'Cost (USD)': cost_values
    })
    
    # Sort by cost
    cost_df = cost_df.sort_values('Cost (USD)', ascending=False)
    
    # Create pie chart
    fig2 = px.pie(
        cost_df,
        values='Cost (USD)',
        names='Category',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A0A0A0']
    )
    
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    
    fig2.update_layout(
        title='Compliance Cost Distribution',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Compliance timeline and milestones
    st.subheader("Compliance Timeline & Milestones")
    
    # Example timeline data
    today = datetime.now()
    milestones = [
        {"Phase": "Assessment", "Start": today - timedelta(days=90), "End": today - timedelta(days=30)},
        {"Phase": "Planning", "Start": today - timedelta(days=30), "End": today},
        {"Phase": "Implementation", "Start": today, "End": today + timedelta(days=90)},
        {"Phase": "Testing", "Start": today + timedelta(days=90), "End": today + timedelta(days=120)},
        {"Phase": "Audit", "Start": today + timedelta(days=120), "End": today + timedelta(days=150)},
        {"Phase": "Ongoing Compliance", "Start": today + timedelta(days=150), "End": today + timedelta(days=365)}
    ]
    
    # Create DataFrame
    milestones_df = pd.DataFrame(milestones)
    
    # Calculate task duration
    milestones_df['Duration'] = (milestones_df['End'] - milestones_df['Start']).dt.days
    
    # Assign colors based on phase
    color_map = {
        "Assessment": "#6082B6",
        "Planning": "#FFD93D",
        "Implementation": "#FF6B6B",
        "Testing": "#00A67E",
        "Audit": "#A0A0A0",
        "Ongoing Compliance": "#0A2540"
    }
    
    milestones_df['Color'] = milestones_df['Phase'].map(color_map)
    
    # Create Gantt chart
    fig3 = px.timeline(
        milestones_df,
        x_start='Start',
        x_end='End',
        y='Phase',
        color='Phase',
        color_discrete_map=color_map
    )
    
    # Add a line for the current date
    fig3.add_vline(
        x=today,
        line_width=2,
        line_dash="dash",
        line_color="#FF6B6B",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    fig3.update_layout(
        title='Compliance Implementation Timeline',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        height=350
    )
    
    st.plotly_chart(fig3, use_container_width=True)

def render_regional_comparison_tab():
    """Renders the regional comparison visualization tab"""
    st.subheader("Regional Regulatory Comparison")
    
    # Example regions and regulatory areas
    regions = ['North America', 'European Union', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    regulatory_areas = ['Data Privacy', 'Financial Compliance', 'Labor Laws', 'Environmental Regulations', 'Consumer Protection']
    
    # Generate random stringency scores
    regulatory_data = []
    
    for region in regions:
        for area in regulatory_areas:
            # Different regions have different baseline stringency
            base_stringency = {
                'European Union': random.uniform(6, 10),
                'North America': random.uniform(5, 9),
                'Asia Pacific': random.uniform(4, 8),
                'Latin America': random.uniform(3, 7),
                'Middle East & Africa': random.uniform(2, 6)
            }
            
            # Add some variance by regulatory area
            area_adjustment = {
                'Data Privacy': random.uniform(-1, 2),
                'Financial Compliance': random.uniform(-1, 1),
                'Labor Laws': random.uniform(-2, 2),
                'Environmental Regulations': random.uniform(-1, 3),
                'Consumer Protection': random.uniform(-2, 1)
            }
            
            stringency = min(10, max(1, base_stringency[region] + area_adjustment[area]))
            
            regulatory_data.append({
                'Region': region,
                'Regulatory Area': area,
                'Stringency': stringency
            })
    
    # Create DataFrame
    reg_df = pd.DataFrame(regulatory_data)
    
    # Create heatmap
    pivot_df = reg_df.pivot(index='Regulatory Area', columns='Region', values='Stringency')
    
    fig = px.imshow(
        pivot_df,
        text_auto='.1f',
        color_continuous_scale='RdYlGn_r',  # Reversed so red is high stringency
        aspect='auto'
    )
    
    fig.update_layout(
        title='Regulatory Stringency by Region (1-10 scale)',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market entry complexity
    st.subheader("Market Entry Regulatory Complexity")
    
    # Generate overall entry complexity
    entry_complexity = []
    
    for region in regions:
        # Calculate average stringency for the region
        avg_stringency = reg_df[reg_df['Region'] == region]['Stringency'].mean()
        
        # Generate additional factors
        compliance_cost = random.uniform(1, 10)
        documentation = random.uniform(1, 10)
        approval_time = random.uniform(1, 10)
        
        # Calculate overall complexity
        overall = (avg_stringency * 0.4) + (compliance_cost * 0.2) + (documentation * 0.2) + (approval_time * 0.2)
        
        entry_complexity.append({
            'Region': region,
            'Regulatory Stringency': avg_stringency,
            'Compliance Cost': compliance_cost,
            'Documentation Requirements': documentation,
            'Approval Timeframe': approval_time,
            'Overall Complexity': overall
        })
    
    # Create DataFrame
    entry_df = pd.DataFrame(entry_complexity)
    
    # Sort by overall complexity
    entry_df = entry_df.sort_values('Overall Complexity', ascending=False)
    
    # Create radar chart
    categories = ['Regulatory Stringency', 'Compliance Cost', 'Documentation Requirements', 'Approval Timeframe']
    
    fig2 = go.Figure()
    
    for i, region in enumerate(entry_df['Region']):
        values = entry_df.loc[entry_df['Region'] == region, categories].values.flatten().tolist()
        values += values[:1]  # Close the loop
        
        fig2.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],  # Close the loop
            fill='toself',
            name=region
        ))
    
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key regulatory differences
    st.subheader("Key Regional Regulatory Differences")
    
    # Display the most divergent regulatory areas
    regulatory_areas = pivot_df.index.tolist()
    
    for area in regulatory_areas:
        region_scores = pivot_df.loc[area]
        min_region = region_scores.idxmin()
        max_region = region_scores.idxmax()
        difference = region_scores[max_region] - region_scores[min_region]
        
        if difference > 3:  # Only show significant differences
            with st.container(border=True):
                st.subheader(f"📊 {area}")
                
                cols = st.columns(2)
                
                with cols[0]:
                    st.markdown(f"**Most Stringent: {max_region}**")
                    st.markdown(f"Stringency: {region_scores[max_region]:.1f}/10")
                    
                    # Generate example requirements for stringent regions
                    st.markdown("**Key Requirements:**")
                    if area == "Data Privacy":
                        st.markdown("- Explicit consent for data collection")
                        st.markdown("- Mandatory data protection officer")
                        st.markdown("- Right to be forgotten implementation")
                    elif area == "Financial Compliance":
                        st.markdown("- Quarterly detailed reporting")
                        st.markdown("- Strict anti-money laundering controls")
                        st.markdown("- Comprehensive audit requirements")
                    elif area == "Labor Laws":
                        st.markdown("- Strong employee protections")
                        st.markdown("- Strict working hour limitations")
                        st.markdown("- Comprehensive benefits requirements")
                    else:
                        st.markdown("- Stringent approval processes")
                        st.markdown("- Extensive documentation requirements")
                        st.markdown("- Regular compliance reporting")
                
                with cols[1]:
                    st.markdown(f"**Least Stringent: {min_region}**")
                    st.markdown(f"Stringency: {region_scores[min_region]:.1f}/10")
                    
                    # Generate example requirements for less stringent regions
                    st.markdown("**Key Requirements:**")
                    if area == "Data Privacy":
                        st.markdown("- Basic consent guidelines")
                        st.markdown("- Limited data breach notification requirements")
                        st.markdown("- Fewer restrictions on data usage")
                    elif area == "Financial Compliance":
                        st.markdown("- Annual reporting may be sufficient")
                        st.markdown("- Less stringent documentation requirements")
                        st.markdown("- Fewer audit requirements")
                    elif area == "Labor Laws":
                        st.markdown("- More flexibility in employment terms")
                        st.markdown("- Fewer restrictions on working hours")
                        st.markdown("- Simplified benefits requirements")
                    else:
                        st.markdown("- Simplified approval processes")
                        st.markdown("- Basic documentation requirements")
                        st.markdown("- Less frequent compliance reporting")