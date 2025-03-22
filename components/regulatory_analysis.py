import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import logging

# Configure logger specific to this module
logger = logging.getLogger(__name__)

def render_regulatory_analysis():
    """
    Renders the regulatory & compliance analysis dashboard with multiple interactive visualizations.
    Any exceptions are caught and displayed.
    """
    try:
        st.header("Regulatory & Compliance Analysis Dashboard")
        
        # Ensure that research data exists; if not, show an informational message.
        if not st.session_state.chat_history:
            st.info("Ask a regulatory compliance question to see analysis and insights here.")
            return
        
        # Create a row of key regulatory metrics (using random demo values)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Regulatory Risk Score", value=f"{random.randint(25, 75)}/100")
        with col2:
            st.metric(label="Key Regulations", value=f"{random.randint(3, 12)}")
        with col3:
            st.metric(label="Compliance Effort", value=random.choice(['Low', 'Medium', 'High']))
        with col4:
            st.metric(label="Regulatory Changes", value=random.choice(['Increasing', 'Stable', 'Evolving']))
        
        # Create tabs for different aspects of regulatory analysis
        tab1, tab2, tab3 = st.tabs(["Regulatory Landscape", "Compliance Requirements", "Regional Comparison"])
        with tab1:
            render_regulatory_landscape_tab()
        with tab2:
            render_compliance_requirements_tab()
        with tab3:
            render_regional_comparison_tab()
        
        # Display key regulatory insights extracted from the latest assistant message
        st.subheader("Key Regulatory Insights")
        assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
        if assistant_messages:
            last_message = assistant_messages[-1]["content"]
            paragraphs = last_message.split('\n\n')
            # Prefer paragraphs containing keywords such as "regulat", "compliance", or "legal"
            regulatory_paragraphs = [p for p in paragraphs if any(kw in p.lower() for kw in ["regulat", "compliance", "legal"])]
            insights = regulatory_paragraphs[0] if regulatory_paragraphs else (paragraphs[0] if paragraphs else last_message)
            st.write(insights)
        else:
            st.write("No regulatory analysis insights available yet. Ask a question to generate insights.")
    except Exception as e:
        logger.error(f"Error in render_regulatory_analysis: {str(e)}", exc_info=True)
        st.error("An error occurred while rendering the regulatory analysis dashboard.")

def render_regulatory_landscape_tab():
    """
    Renders the regulatory landscape tab displaying a scatter plot and timeline visualization.
    """
    try:
        st.subheader("Key Regulatory Framework Overview")
        
        # Example regulatory data (demo purposes)
        regulations = ["Regulation A", "Regulation B", "Regulation C", "Regulation D", "Regulation E", "Regulation F"]
        impact_scores = [random.uniform(1, 10) for _ in range(len(regulations))]
        complexity_scores = [random.uniform(1, 10) for _ in range(len(regulations))]
        status_options = ["Active", "Pending", "Proposed", "Under Review"]
        status_weights = [0.6, 0.2, 0.1, 0.1]
        statuses = [np.random.choice(status_options, p=status_weights) for _ in range(len(regulations))]
        
        reg_df = pd.DataFrame({
            'Regulation': regulations,
            'Business Impact': impact_scores,
            'Compliance Complexity': complexity_scores,
            'Status': statuses
        })
        
        # Create a scatter plot (regulatory matrix)
        fig = px.scatter(reg_df,
                         x='Compliance Complexity',
                         y='Business Impact',
                         color='Status',
                         text='Regulation',
                         size=[8] * len(reg_df),
                         color_discrete_map={'Active': '#00A67E',
                                               'Pending': '#FFD93D',
                                               'Proposed': '#6082B6',
                                               'Under Review': '#FF6B6B'})
        # Add quadrant lines
        fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="gray", width=1, dash="dash"))
        fig.add_shape(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="gray", width=1, dash="dash"))
        # Add quadrant annotations
        fig.add_annotation(x=2.5, y=7.5, text="High Impact, Low Complexity", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=7.5, y=7.5, text="Critical Attention", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=2.5, y=2.5, text="Lower Priority", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=7.5, y=2.5, text="Complex, Lower Impact", showarrow=False, font=dict(size=12))
        fig.update_traces(textposition='top center', textfont=dict(size=10))
        fig.update_layout(title='Regulatory Impact vs. Compliance Complexity', xaxis=dict(title='Compliance Complexity', range=[0, 10]), yaxis=dict(title='Business Impact', range=[0, 10]), height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Regulatory timeline visualization
        st.subheader("Regulatory Timeline")
        timeline_events = [
            {"Regulation": "Regulation A", "Event": "Implementation Deadline", "Date": datetime.now() + timedelta(days=random.randint(30, 180))},
            {"Regulation": "Regulation B", "Event": "Public Comment Period", "Date": datetime.now() + timedelta(days=random.randint(-60, -30))},
            {"Regulation": "Regulation C", "Event": "Final Rule Publication", "Date": datetime.now() + timedelta(days=random.randint(-120, -90))},
            {"Regulation": "Regulation D", "Event": "Enforcement Begins", "Date": datetime.now() + timedelta(days=random.randint(60, 90))},
            {"Regulation": "Regulation E", "Event": "Regulatory Review", "Date": datetime.now() + timedelta(days=random.randint(120, 240))},
            {"Regulation": "Regulation F", "Event": "Initial Announcement", "Date": datetime.now() + timedelta(days=random.randint(-180, -150))}
        ]
        timeline_df = pd.DataFrame(timeline_events).sort_values('Date')
        timeline_df['Color'] = timeline_df['Date'].apply(lambda x: '#00A67E' if x > datetime.now() else '#6082B6')
        fig2 = go.Figure()
        for i, row in timeline_df.iterrows():
            fig2.add_trace(go.Scatter(x=[row['Date']], y=[row['Regulation']], mode='markers+text',
                                        marker=dict(size=15, color=row['Color']),
                                        text=row['Event'], textposition='middle right', name=row['Event']))
        fig2.add_vline(x=datetime.now().timestamp(), line_width=2, line_dash="dash", line_color="#FF6B6B",
                       annotation_text="Today", annotation_position="top right")
        fig2.update_layout(title='Key Regulatory Dates & Deadlines', xaxis=dict(title=''), yaxis=dict(title=''), showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        logger.error(f"Error in render_regulatory_landscape_tab: {str(e)}", exc_info=True)
        st.error("An error occurred while rendering the regulatory landscape visualization.")

def render_compliance_requirements_tab():
    """
    Renders the compliance requirements tab with a bar chart and detailed textual analysis.
    """
    try:
        st.subheader("Compliance Requirements Analysis")
        
        compliance_categories = [
            "Data Protection & Privacy",
            "Financial Reporting",
            "Consumer Rights",
            "Environmental Compliance",
            "Health & Safety",
            "Employment Law"
        ]
        complexity_scores = [random.uniform(1, 10) for _ in range(len(compliance_categories))]
        implementation_scores = [random.uniform(0, 100) for _ in range(len(compliance_categories))]
        
        compliance_df = pd.DataFrame({
            'Category': compliance_categories,
            'Complexity': complexity_scores,
            'Implementation (%)': implementation_scores
        }).sort_values('Implementation (%)')
        
        # Create a stacked horizontal bar chart (Implemented vs. Remaining)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=compliance_df['Category'],
            x=compliance_df['Implementation (%)'],
            orientation='h',
            marker_color='#00A67E',
            name='Implemented'
        ))
        fig.add_trace(go.Bar(
            y=compliance_df['Category'],
            x=[100 - val for val in compliance_df['Implementation (%)']],
            orientation='h',
            marker_color='#FF6B6B',
            name='Remaining'
        ))
        fig.update_layout(title='Compliance Implementation Status', xaxis=dict(title='Implementation Percentage'), yaxis=dict(title=''), barmode='stack', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Key Compliance Requirements")
        top_categories = compliance_df.sort_values('Complexity', ascending=False).head(3)
        for i, row in top_categories.iterrows():
            with st.container():
                cols = st.columns([1, 4])
                with cols[0]:
                    st.metric(label="Complexity", value=f"{row['Complexity']:.1f}/10")
                    st.markdown("**Implementation:**")
                    st.progress(row['Implementation (%)'] / 100)
                    st.markdown(f"{row['Implementation (%)']:.1f}%")
                with cols[1]:
                    st.subheader(row['Category'])
                    example_requirements = []
                    if "Data" in row['Category']:
                        example_requirements = ["Consent requirements", "Data protection officer", "Breach notification processes"]
                    elif "Financial" in row['Category']:
                        example_requirements = ["Quarterly reporting", "Revenue recognition", "Internal audits"]
                    elif "Consumer" in row['Category']:
                        example_requirements = ["Transparency guidelines", "Cooling-off periods", "Complaint resolution"]
                    elif "Environmental" in row['Category']:
                        example_requirements = ["Emission limits", "Sustainability audits", "Waste management"]
                    elif "Health" in row['Category']:
                        example_requirements = ["Workplace safety protocols", "Training programs", "Incident reporting"]
                    elif "Employment" in row['Category']:
                        example_requirements = ["Contract clarity", "Anti-discrimination policies", "Leave management"]
                    else:
                        example_requirements = ["Requirement 1", "Requirement 2", "Requirement 3"]
                    for req in example_requirements:
                        st.markdown(f"- {req}")
        
        st.subheader("Compliance Resource Requirements")
        cost_categories = ['Technology', 'Personnel', 'Training', 'External Expertise', 'Documentation', 'Ongoing Monitoring']
        cost_values = [random.uniform(10000, 100000) for _ in range(len(cost_categories))]
        cost_df = pd.DataFrame({'Category': cost_categories, 'Cost (USD)': cost_values}).sort_values('Cost (USD)', ascending=False)
        fig2 = px.pie(cost_df, values='Cost (USD)', names='Category', color_discrete_sequence=['#0A2540','#00A67E','#FF6B6B','#FFD93D','#6082B6','#A0A0A0'])
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(title='Compliance Cost Distribution', height=400)
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        logger.error(f"Error in render_compliance_requirements_tab: {str(e)}", exc_info=True)
        st.error("An error occurred while rendering the compliance requirements visualization.")

def render_regional_comparison_tab():
    """
    Renders the regional comparison tab with a heatmap and radar charts highlighting regulatory stringency.
    """
    try:
        st.subheader("Regional Regulatory Comparison")
        regions = ['North America', 'European Union', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
        regulatory_areas = ['Data Privacy', 'Financial Compliance', 'Labor Laws', 'Environmental Regulations', 'Consumer Protection']
        
        regulatory_data = []
        for region in regions:
            for area in regulatory_areas:
                base_stringency = {
                    'European Union': random.uniform(6, 10),
                    'North America': random.uniform(5, 9),
                    'Asia Pacific': random.uniform(4, 8),
                    'Latin America': random.uniform(3, 7),
                    'Middle East & Africa': random.uniform(2, 6)
                }
                area_adjustment = {
                    'Data Privacy': random.uniform(-1, 2),
                    'Financial Compliance': random.uniform(-1, 1),
                    'Labor Laws': random.uniform(-2, 2),
                    'Environmental Regulations': random.uniform(-1, 3),
                    'Consumer Protection': random.uniform(-2, 1)
                }
                stringency = min(10, max(1, base_stringency[region] + area_adjustment[area]))
                regulatory_data.append({'Region': region, 'Regulatory Area': area, 'Stringency': stringency})
        
        reg_df = pd.DataFrame(regulatory_data)
        pivot_df = reg_df.pivot(index='Regulatory Area', columns='Region', values='Stringency')
        fig = px.imshow(pivot_df, text_auto='.1f', color_continuous_scale='RdYlGn_r', aspect='auto')
        fig.update_layout(title='Regulatory Stringency by Region (1-10 Scale)', xaxis=dict(title=''), yaxis=dict(title=''), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Market Entry Regulatory Complexity")
        entry_complexity = []
        for region in regions:
            avg_stringency = reg_df[reg_df['Region'] == region]['Stringency'].mean()
            compliance_cost = random.uniform(1, 10)
            documentation = random.uniform(1, 10)
            approval_time = random.uniform(1, 10)
            overall = (avg_stringency * 0.4) + (compliance_cost * 0.2) + (documentation * 0.2) + (approval_time * 0.2)
            entry_complexity.append({
                'Region': region,
                'Regulatory Stringency': avg_stringency,
                'Compliance Cost': compliance_cost,
                'Documentation Requirements': documentation,
                'Approval Timeframe': approval_time,
                'Overall Complexity': overall
            })
        entry_df = pd.DataFrame(entry_complexity).sort_values('Overall Complexity', ascending=False)
        
        # Radar chart for each region (top 3 by overall complexity)
        top_regions = entry_df.head(3)
        categories = ['Regulatory Stringency', 'Compliance Cost', 'Documentation Requirements', 'Approval Timeframe']
        fig2 = go.Figure()
        for _, row in top_regions.iterrows():
            values = [row[cat] for cat in categories]
            values += values[:1]
            fig2.add_trace(go.Scatterpolar(r=values, theta=categories + [categories[0]], fill='toself', name=row['Region']))
        fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True, height=500)
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        logger.error(f"Error in render_regional_comparison_tab: {str(e)}", exc_info=True)
        st.error("An error occurred while rendering the regional comparison visualization.")
        
# Note: Additional improvements could include caching results, adding interactive filters, and using real data
# instead of randomized demo values.
