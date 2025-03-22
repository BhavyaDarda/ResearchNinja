import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render_supply_chain_analysis():
    """Renders the supplier, partner, and distribution analysis visualization panel"""
    
    st.header("Supply Chain & Distribution Analysis Dashboard")
    
    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info("Ask a supply chain or distribution question to see analysis and insights here.")
        return
    
    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(
            label="Supplier Options",
            value=f"{random.randint(5, 30)}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Supply Chain Risk",
            value=f"{random.choice(['Medium', 'Low', 'High'])}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Distribution Channels",
            value=f"{random.randint(3, 8)}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Partnership Opportunities",
            value=f"{random.randint(2, 12)}",
            delta=None
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Supplier Analysis", "Distribution Channels", "Partnership Landscape"])
    
    with tab1:
        render_supplier_analysis_tab()
    
    with tab2:
        render_distribution_channels_tab()
    
    with tab3:
        render_partnership_landscape_tab()
    
    # Supply chain insights
    st.subheader("Key Supply Chain Insights")
    
    # Extract the last assistant message for insights
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        
        # Take a relevant paragraph as insights
        paragraphs = last_message.split('\n\n')
        supply_chain_paragraphs = [p for p in paragraphs if "supplier" in p.lower() or "distribution" in p.lower() or "partner" in p.lower()]
        if supply_chain_paragraphs:
            insights = supply_chain_paragraphs[0]
        else:
            insights = paragraphs[0] if paragraphs else last_message
        
        st.write(insights)
    else:
        st.write("No supply chain analysis insights available yet. Ask a question to generate insights.")

def render_supplier_analysis_tab():
    """Renders the supplier analysis visualization tab"""
    st.subheader("Supplier Landscape Overview")
    
    # Example supplier data
    suppliers = [
        "Supplier A",
        "Supplier B",
        "Supplier C",
        "Supplier D",
        "Supplier E",
        "Supplier F",
        "Supplier G"
    ]
    
    # Generate random scores for key metrics
    quality_scores = [random.uniform(5, 10) for _ in range(len(suppliers))]
    cost_scores = [random.uniform(3, 10) for _ in range(len(suppliers))]  # Higher is better (cost efficiency)
    reliability_scores = [random.uniform(4, 10) for _ in range(len(suppliers))]
    lead_times = [random.randint(3, 30) for _ in range(len(suppliers))]  # Days
    min_order_qtys = [random.randint(50, 1000) for _ in range(len(suppliers))]
    
    # Calculate overall score
    overall_scores = [
        (quality_scores[i] * 0.4) + (cost_scores[i] * 0.3) + (reliability_scores[i] * 0.3)
        for i in range(len(suppliers))
    ]
    
    # Create DataFrame
    supplier_df = pd.DataFrame({
        'Supplier': suppliers,
        'Quality': quality_scores,
        'Cost Efficiency': cost_scores,
        'Reliability': reliability_scores,
        'Lead Time (days)': lead_times,
        'Min Order Quantity': min_order_qtys,
        'Overall Score': overall_scores
    })
    
    # Sort by overall score
    supplier_df = supplier_df.sort_values('Overall Score', ascending=False)
    
    # Create radar chart comparing top 3 suppliers
    top_suppliers = supplier_df.head(3)
    
    # Radar categories
    categories = ['Quality', 'Cost Efficiency', 'Reliability']
    
    fig = go.Figure()
    
    for _, supplier in top_suppliers.iterrows():
        values = [supplier['Quality'], supplier['Cost Efficiency'], supplier['Reliability']]
        values += values[:1]  # Close the loop
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],  # Close the loop
            fill='toself',
            name=supplier['Supplier']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500,
        title='Top Supplier Comparison'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Supplier comparison table
    st.subheader("Supplier Comparison")
    
    # Format table for display
    display_df = supplier_df.copy()
    for col in ['Quality', 'Cost Efficiency', 'Reliability', 'Overall Score']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}/10")
    
    st.dataframe(
        display_df[['Supplier', 'Quality', 'Cost Efficiency', 'Reliability', 'Lead Time (days)', 'Min Order Quantity', 'Overall Score']],
        use_container_width=True
    )
    
    # Supply chain risk analysis
    st.subheader("Supply Chain Risk Assessment")
    
    # Example risk factors
    risk_factors = [
        "Supply Disruption",
        "Quality Issues",
        "Cost Volatility",
        "Lead Time Variability",
        "Supplier Financial Stability",
        "Geopolitical Risks",
        "Environmental Compliance"
    ]
    
    # Generate risk scores and mitigation effectiveness
    risk_scores = [random.uniform(2, 8) for _ in range(len(risk_factors))]
    mitigation_effectiveness = [random.uniform(3, 9) for _ in range(len(risk_factors))]
    
    # Calculate residual risk
    residual_risks = [
        max(1, risk_scores[i] * (1 - mitigation_effectiveness[i] / 10))
        for i in range(len(risk_factors))
    ]
    
    # Create DataFrame
    risk_df = pd.DataFrame({
        'Risk Factor': risk_factors,
        'Initial Risk': risk_scores,
        'Mitigation Effectiveness': mitigation_effectiveness,
        'Residual Risk': residual_risks
    })
    
    # Sort by residual risk
    risk_df = risk_df.sort_values('Residual Risk', ascending=False)
    
    # Create bar chart comparing initial and residual risk
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        y=risk_df['Risk Factor'],
        x=risk_df['Initial Risk'],
        name='Initial Risk',
        orientation='h',
        marker_color='#FF6B6B'
    ))
    
    fig2.add_trace(go.Bar(
        y=risk_df['Risk Factor'],
        x=risk_df['Residual Risk'],
        name='Residual Risk',
        orientation='h',
        marker_color='#00A67E'
    ))
    
    fig2.update_layout(
        title='Supply Chain Risk Assessment',
        xaxis=dict(title='Risk Level (1-10)'),
        yaxis=dict(title=''),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Geographic supplier distribution
    st.subheader("Geographic Supplier Distribution")
    
    # Example regional supplier data
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    supplier_counts = [random.randint(2, 20) for _ in range(len(regions))]
    
    # Create DataFrame
    geo_df = pd.DataFrame({
        'Region': regions,
        'Number of Suppliers': supplier_counts
    })
    
    # Create pie chart
    fig3 = px.pie(
        geo_df,
        values='Number of Suppliers',
        names='Region',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6']
    )
    
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    
    fig3.update_layout(
        title='Supplier Geographic Distribution',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)

def render_distribution_channels_tab():
    """Renders the distribution channels visualization tab"""
    st.subheader("Distribution Channel Analysis")
    
    # Example distribution channels
    channels = [
        "Direct E-commerce",
        "Retail Partners",
        "Wholesale Distribution",
        "Marketplaces",
        "Value-Added Resellers",
        "Affiliate Partners"
    ]
    
    # Generate random metrics for each channel
    revenue_shares = [random.uniform(5, 35) for _ in range(len(channels))]
    # Normalize to 100%
    revenue_shares = [share * 100 / sum(revenue_shares) for share in revenue_shares]
    
    margin_percentages = [random.uniform(15, 60) for _ in range(len(channels))]
    growth_rates = [random.uniform(-5, 20) for _ in range(len(channels))]
    
    # Create DataFrame
    channel_df = pd.DataFrame({
        'Channel': channels,
        'Revenue Share (%)': revenue_shares,
        'Profit Margin (%)': margin_percentages,
        'Growth Rate (%)': growth_rates
    })
    
    # Sort by revenue share
    channel_df = channel_df.sort_values('Revenue Share (%)', ascending=False)
    
    # Create bubble chart
    fig = px.scatter(
        channel_df,
        x='Profit Margin (%)',
        y='Growth Rate (%)',
        size='Revenue Share (%)',
        color='Channel',
        text='Channel',
        size_max=60,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A0A0A0']
    )
    
    # Add quadrant lines
    fig.add_shape(
        type="line",
        x0=30, y0=-10, x1=30, y1=25,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=0, y0=5, x1=70, y1=5,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    # Add quadrant labels
    fig.add_annotation(x=15, y=15, text="High Growth, Low Margin",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=50, y=15, text="Star Performers",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=15, y=-5, text="Problematic",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=50, y=-5, text="Cash Cows",
                      showarrow=False, font=dict(size=12))
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig.update_layout(
        title='Distribution Channel Performance Matrix',
        xaxis=dict(title='Profit Margin (%)', range=[0, 70]),
        yaxis=dict(title='Growth Rate (%)', range=[-10, 25]),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Channel revenue and cost breakdown
    st.subheader("Channel Revenue & Cost Breakdown")
    
    # Generate detailed cost data for top channels
    top_channels = channel_df.head(3)['Channel'].tolist()
    
    # Cost categories
    cost_categories = ['Product Cost', 'Logistics', 'Marketing', 'Platform Fees', 'Customer Support', 'Other']
    
    # Generate cost data for each channel
    channel_costs = []
    
    for channel in top_channels:
        margin = channel_df.loc[channel_df['Channel'] == channel, 'Profit Margin (%)'].values[0]
        
        # Generate cost percentages that add up to (100 - margin)
        total_cost_percent = 100 - margin
        
        # Generate random costs that sum to total_cost_percent
        costs = [random.uniform(5, 20) for _ in range(len(cost_categories) - 1)]
        costs_sum = sum(costs)
        costs = [cost * total_cost_percent / costs_sum for cost in costs]
        
        # Add the remainder to "Other"
        costs.append(total_cost_percent - sum(costs))
        
        for i, category in enumerate(cost_categories):
            channel_costs.append({
                'Channel': channel,
                'Category': category,
                'Percentage': costs[i]
            })
    
    # Create DataFrame
    costs_df = pd.DataFrame(channel_costs)
    
    # Create stacked bar chart
    fig2 = px.bar(
        costs_df,
        x='Channel',
        y='Percentage',
        color='Category',
        title='Cost Structure by Channel',
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A0A0A0']
    )
    
    # Add profit as a separate bar
    for channel in top_channels:
        margin = channel_df.loc[channel_df['Channel'] == channel, 'Profit Margin (%)'].values[0]
        
        fig2.add_trace(go.Bar(
            x=[channel],
            y=[margin],
            name='Profit Margin' if channel == top_channels[0] else None,
            marker_color='#00A67E',
            showlegend=channel == top_channels[0]
        ))
    
    fig2.update_layout(
        barmode='stack',
        xaxis=dict(title=''),
        yaxis=dict(title='Percentage (%)', range=[0, 100]),
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Channel reach and customer characteristics
    st.subheader("Channel Customer Profile Comparison")
    
    # Customer characteristics by channel
    characteristics = [
        "Customer Acquisition Cost",
        "Customer Lifetime Value",
        "Average Order Value",
        "Purchase Frequency",
        "Return Rate"
    ]
    
    # Generate normalized scores (0-10) for each channel and characteristic
    channel_profiles = []
    
    for channel in channels:
        for characteristic in characteristics:
            # Generate score with some patterns
            base_score = 5
            
            if characteristic == "Customer Acquisition Cost":
                # Direct typically has lower CAC than retail
                if "Direct" in channel:
                    adjustment = -2
                elif "Retail" in channel:
                    adjustment = 3
                else:
                    adjustment = random.uniform(-2, 2)
            elif characteristic == "Customer Lifetime Value":
                # Direct typically has higher LTV
                if "Direct" in channel:
                    adjustment = 3
                elif "Affiliate" in channel:
                    adjustment = -2
                else:
                    adjustment = random.uniform(-2, 2)
            else:
                adjustment = random.uniform(-3, 3)
            
            score = base_score + adjustment
            score = max(1, min(10, score))  # Constrain to 1-10
            
            channel_profiles.append({
                'Channel': channel,
                'Characteristic': characteristic,
                'Score': score
            })
    
    # Create DataFrame
    profile_df = pd.DataFrame(channel_profiles)
    
    # Create heatmap
    pivot_df = profile_df.pivot(index='Characteristic', columns='Channel', values='Score')
    
    fig3 = px.imshow(
        pivot_df,
        text_auto='.1f',
        color_continuous_scale='RdYlGn_r',  # Reversed so red is high cost, green is low
        aspect='auto'
    )
    
    fig3.update_layout(
        title='Channel Customer Characteristics (1-10 scale)',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Global distribution reach
    st.subheader("Global Distribution Reach")
    
    # Example regional coverage by channel
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    
    # Generate coverage percentages
    coverage_data = []
    
    for channel in channels:
        for region in regions:
            # Different channels have different regional strengths
            if "Direct" in channel:
                # Direct e-commerce tends to be stronger in developed markets
                if region in ['North America', 'Europe']:
                    base_coverage = random.uniform(70, 95)
                else:
                    base_coverage = random.uniform(30, 70)
            elif "Retail" in channel:
                # Retail partners more evenly distributed but still stronger in developed
                if region in ['North America', 'Europe']:
                    base_coverage = random.uniform(60, 90)
                else:
                    base_coverage = random.uniform(40, 75)
            else:
                base_coverage = random.uniform(30, 80)
            
            coverage_data.append({
                'Channel': channel,
                'Region': region,
                'Coverage (%)': base_coverage
            })
    
    # Create DataFrame
    coverage_df = pd.DataFrame(coverage_data)
    
    # Create heatmap
    pivot_df = coverage_df.pivot(index='Region', columns='Channel', values='Coverage (%)')
    
    fig4 = px.imshow(
        pivot_df,
        text_auto='.0f',
        color_continuous_scale='Blues',
        aspect='auto'
    )
    
    fig4.update_layout(
        title='Distribution Channel Regional Coverage (%)',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        height=400
    )
    
    st.plotly_chart(fig4, use_container_width=True)

def render_partnership_landscape_tab():
    """Renders the partnership landscape visualization tab"""
    st.subheader("Strategic Partnership Opportunities")
    
    # Example partnership categories
    partnership_types = [
        "Technology Integration",
        "Marketing/Co-branding",
        "Distribution Network",
        "R&D Collaboration",
        "Supply Chain Optimization",
        "Industry Consortium"
    ]
    
    # Generate scores for each partnership type
    strategic_value = [random.uniform(5, 10) for _ in range(len(partnership_types))]
    implementation_complexity = [random.uniform(2, 9) for _ in range(len(partnership_types))]
    time_to_value = [random.randint(1, 24) for _ in range(len(partnership_types))]  # Months
    
    # Create DataFrame
    partnership_df = pd.DataFrame({
        'Partnership Type': partnership_types,
        'Strategic Value': strategic_value,
        'Implementation Complexity': implementation_complexity,
        'Time to Value (months)': time_to_value
    })
    
    # Create scatter plot
    fig = px.scatter(
        partnership_df,
        x='Implementation Complexity',
        y='Strategic Value',
        size='Time to Value (months)',
        color='Partnership Type',
        text='Partnership Type',
        size_max=45,
        color_discrete_sequence=['#0A2540', '#00A67E', '#FF6B6B', '#FFD93D', '#6082B6', '#A0A0A0']
    )
    
    # Add quadrant lines
    fig.add_shape(
        type="line",
        x0=5.5, y0=0, x1=5.5, y1=10,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=0, y0=7.5, x1=10, y1=7.5,
        line=dict(color="gray", width=1, dash="dash")
    )
    
    # Add quadrant labels
    fig.add_annotation(x=3, y=8.75, text="Quick Wins",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=7.5, y=8.75, text="Strategic Priorities",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=3, y=5, text="Low Priority",
                      showarrow=False, font=dict(size=12))
    fig.add_annotation(x=7.5, y=5, text="Selective Investment",
                      showarrow=False, font=dict(size=12))
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10)
    )
    
    fig.update_layout(
        title='Partnership Opportunity Matrix',
        xaxis=dict(title='Implementation Complexity', range=[0, 10]),
        yaxis=dict(title='Strategic Value', range=[0, 10]),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Potential partners analysis
    st.subheader("Potential Partners Evaluation")
    
    # Example potential partners
    partners = [
        "Company Alpha",
        "Company Beta",
        "Company Gamma",
        "Company Delta",
        "Company Epsilon"
    ]
    
    # Generate scores for each partner
    strategic_alignment = [random.uniform(5, 10) for _ in range(len(partners))]
    market_position = [random.uniform(5, 10) for _ in range(len(partners))]
    technical_compatibility = [random.uniform(3, 10) for _ in range(len(partners))]
    cultural_fit = [random.uniform(4, 10) for _ in range(len(partners))]
    
    # Calculate overall score
    overall_scores = [
        (strategic_alignment[i] * 0.3) + (market_position[i] * 0.3) + 
        (technical_compatibility[i] * 0.2) + (cultural_fit[i] * 0.2)
        for i in range(len(partners))
    ]
    
    # Create DataFrame
    partner_df = pd.DataFrame({
        'Partner': partners,
        'Strategic Alignment': strategic_alignment,
        'Market Position': market_position,
        'Technical Compatibility': technical_compatibility,
        'Cultural Fit': cultural_fit,
        'Overall Score': overall_scores
    })
    
    # Sort by overall score
    partner_df = partner_df.sort_values('Overall Score', ascending=False)
    
    # Create radar chart comparing top 3 partners
    top_partners = partner_df.head(3)
    
    # Radar categories
    categories = ['Strategic Alignment', 'Market Position', 'Technical Compatibility', 'Cultural Fit']
    
    fig2 = go.Figure()
    
    for _, partner in top_partners.iterrows():
        values = [
            partner['Strategic Alignment'], 
            partner['Market Position'], 
            partner['Technical Compatibility'], 
            partner['Cultural Fit']
        ]
        values += values[:1]  # Close the loop
        
        fig2.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],  # Close the loop
            fill='toself',
            name=partner['Partner']
        ))
    
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500,
        title='Top Partner Comparison'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Partnership success factors
    st.subheader("Partnership Success Factors")
    
    # Success factors
    success_factors = [
        "Clear Value Proposition",
        "Executive Sponsorship",
        "Operational Integration",
        "Cultural Alignment",
        "Mutual Benefits",
        "Transparent Communication",
        "Scalable Framework",
        "Performance Metrics"
    ]
    
    # Generate importance and readiness scores
    importance_scores = [random.uniform(7, 10) for _ in range(len(success_factors))]
    readiness_scores = [random.uniform(3, 9) for _ in range(len(success_factors))]
    
    # Calculate gap
    gap_scores = [importance_scores[i] - readiness_scores[i] for i in range(len(success_factors))]
    
    # Create DataFrame
    success_df = pd.DataFrame({
        'Success Factor': success_factors,
        'Importance': importance_scores,
        'Current Readiness': readiness_scores,
        'Gap': gap_scores
    })
    
    # Sort by gap
    success_df = success_df.sort_values('Gap', ascending=False)
    
    # Create horizontal bar chart
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        y=success_df['Success Factor'],
        x=success_df['Importance'],
        name='Importance',
        orientation='h',
        marker_color='#0A2540'
    ))
    
    fig3.add_trace(go.Bar(
        y=success_df['Success Factor'],
        x=success_df['Current Readiness'],
        name='Current Readiness',
        orientation='h',
        marker_color='#00A67E'
    ))
    
    fig3.update_layout(
        title='Partnership Readiness Assessment',
        xaxis=dict(title='Score (1-10)'),
        yaxis=dict(title=''),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=500,
        barmode='group'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Partnership benefits analysis
    st.subheader("Partnership Benefits Analysis")
    
    # Partnership benefits
    benefits = [
        "Market Access",
        "Technology Access",
        "Cost Reduction",
        "Risk Mitigation",
        "Innovation Acceleration",
        "Competitive Advantage"
    ]
    
    # Example partnership types
    partnership_categories = ["Technology", "Distribution", "Marketing", "R&D"]
    
    # Generate benefit scores for each partnership type
    benefit_data = []
    
    for benefit in benefits:
        for category in partnership_categories:
            # Generate score with some patterns
            if benefit == "Market Access" and category == "Distribution":
                base_score = random.uniform(7, 10)
            elif benefit == "Technology Access" and category == "Technology":
                base_score = random.uniform(7, 10)
            elif benefit == "Innovation Acceleration" and category == "R&D":
                base_score = random.uniform(7, 10)
            elif benefit == "Competitive Advantage" and category == "Marketing":
                base_score = random.uniform(6, 9)
            else:
                base_score = random.uniform(3, 8)
            
            benefit_data.append({
                'Benefit': benefit,
                'Partnership Category': category,
                'Impact Score': base_score
            })
    
    # Create DataFrame
    benefit_df = pd.DataFrame(benefit_data)
    
    # Create heatmap
    pivot_df = benefit_df.pivot(index='Benefit', columns='Partnership Category', values='Impact Score')
    
    fig4 = px.imshow(
        pivot_df,
        text_auto='.1f',
        color_continuous_scale='Blues',
        aspect='auto'
    )
    
    fig4.update_layout(
        title='Partnership Benefits by Category (1-10 scale)',
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        height=400
    )
    
    st.plotly_chart(fig4, use_container_width=True)