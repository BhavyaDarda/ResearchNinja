import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime


def render_business_viability():
    """Renders the business viability analysis visualization panel"""

    st.header("Business Viability Analysis Dashboard")

    # Check if we have any research data
    if not st.session_state.chat_history:
        st.info(
            "Ask a business viability question to see analysis and insights here."
        )
        return

    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)

    # Generate random metrics for demonstration
    # In a real application, these would be derived from the research results
    with col1:
        st.metric(label="Market Potential",
                  value=f"${random.randint(50, 500)}B",
                  delta=f"{random.uniform(2, 15):.1f}%")

    with col2:
        st.metric(label="Viability Score",
                  value=f"{random.randint(65, 95)}/100",
                  delta=None)

    with col3:
        st.metric(label="Competition",
                  value=f"{random.choice(['Low', 'Moderate', 'High'])}",
                  delta=None)

    with col4:
        st.metric(label="Break-even Time",
                  value=f"{random.randint(12, 48)} months",
                  delta=None)

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Financial Projection", "Market Fit", "Risk Assessment",
        "Success Metrics"
    ])

    with tab1:
        render_financial_projection_tab()

    with tab2:
        render_market_fit_tab()

    with tab3:
        render_risk_assessment_tab()

    with tab4:
        render_success_metrics_tab()

    # Summary box at the bottom
    st.subheader("Viability Summary")

    # Extract the last assistant message for the summary
    assistant_messages = [
        msg for msg in st.session_state.chat_history
        if msg["role"] == "assistant"
    ]

    if assistant_messages:
        last_message = assistant_messages[-1]["content"]
        # Take first paragraph as summary
        summary = last_message.split(
            '\n\n')[0] if '\n\n' in last_message else last_message
        st.write(summary)
    else:
        st.write(
            "No business viability summary available yet. Ask a question to generate insights."
        )


def render_financial_projection_tab():
    """Renders the financial projection visualization tab"""
    st.subheader("Financial Projection Analysis")

    # Create example financial projection data
    # In a real application, this would be derived from the research results
    years = list(range(datetime.now().year, datetime.now().year + 6))

    # Generate random financial data
    revenue = [0]
    for i in range(1, 6):
        revenue.append(random.uniform(0.5, 1.5) * (i * i) *
                       100000)  # Quadratic growth pattern

    costs = [100000]  # Initial investment
    for i in range(1, 6):
        costs.append(
            50000 +
            (revenue[i] * random.uniform(0.4, 0.6)))  # Costs grow with revenue

    profit = [revenue[i] - costs[i] for i in range(6)]

    # Create a DataFrame for the visualization
    df = pd.DataFrame({
        'Year': years,
        'Revenue': revenue,
        'Costs': costs,
        'Profit': profit
    })

    # Calculate break-even point
    if all(p <= 0 for p in profit):
        breakeven_year = "Beyond projection"
    else:
        for i, p in enumerate(profit):
            if p > 0:
                if i == 0:
                    breakeven_year = f"Year {years[0]}"
                else:
                    # Interpolate for more precise break-even point
                    prev_year = years[i - 1]
                    curr_year = years[i]
                    prev_profit = profit[i - 1]
                    curr_profit = profit[i]
                    if prev_profit >= 0:
                        breakeven_year = f"Year {prev_year}"
                    else:
                        # Linear interpolation to find month
                        months_after_prev = -prev_profit / (curr_profit -
                                                            prev_profit) * 12
                        breakeven_month = int(months_after_prev)
                        breakeven_year = f"Year {prev_year}, Month {breakeven_month}"
                break
        else:
            breakeven_year = "Beyond projection"

    # Create and display chart
    fig = go.Figure()

    # Revenue trace
    fig.add_trace(
        go.Scatter(x=df['Year'],
                   y=df['Revenue'],
                   mode='lines+markers',
                   name='Revenue',
                   line=dict(color='#00A67E', width=3)))

    # Costs trace
    fig.add_trace(
        go.Scatter(x=df['Year'],
                   y=df['Costs'],
                   mode='lines+markers',
                   name='Costs',
                   line=dict(color='#FF6B6B', width=3)))

    # Profit area
    fig.add_trace(
        go.Scatter(x=df['Year'],
                   y=df['Profit'],
                   mode='lines+markers',
                   name='Profit/Loss',
                   line=dict(color='#0A2540', width=3),
                   fill='tozeroy'))

    # Update layout
    fig.update_layout(
        title=f'Financial Projection (Break-even: {breakeven_year})',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Amount ($)'),
        hovermode='x unified',
        legend=dict(orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1),
        height=400)

    st.plotly_chart(fig, use_container_width=True)

    # Monthly cash flow for first year
    st.subheader("First Year Monthly Cash Flow")

    # Generate monthly data for the first year
    months = [f"Month {i+1}" for i in range(12)]
    monthly_revenue = [0]  # Start with zero
    for i in range(1, 12):
        # Gradually increasing revenue through the year
        monthly_revenue.append(revenue[1] * i /
                               36)  # Gradual ramp up to year 1 total

    monthly_costs = [costs[0] / 4]  # Initial setup cost
    for i in range(1, 12):
        monthly_costs.append(
            costs[1] / 12 +
            random.uniform(-5000, 5000))  # Monthly costs with some variance

    monthly_cash_flow = [
        monthly_revenue[i] - monthly_costs[i] for i in range(12)
    ]
    cumulative_cash_flow = np.cumsum(monthly_cash_flow)

    # Create a DataFrame for the visualization
    monthly_df = pd.DataFrame({
        'Month': months,
        'Revenue': monthly_revenue,
        'Costs': monthly_costs,
        'Cash Flow': monthly_cash_flow,
        'Cumulative': cumulative_cash_flow
    })

    # Create and display chart
    fig2 = go.Figure()

    # Cash flow bars
    fig2.add_trace(
        go.Bar(x=monthly_df['Month'],
               y=monthly_df['Cash Flow'],
               name='Monthly Cash Flow',
               marker_color=[
                   '#FF6B6B' if cf < 0 else '#00A67E'
                   for cf in monthly_cash_flow
               ]))

    # Cumulative line
    fig2.add_trace(
        go.Scatter(x=monthly_df['Month'],
                   y=monthly_df['Cumulative'],
                   mode='lines+markers',
                   name='Cumulative Cash Flow',
                   line=dict(color='#0A2540', width=3)))

    # Update layout
    fig2.update_layout(title='First Year Monthly Cash Flow',
                       xaxis=dict(title='Month'),
                       yaxis=dict(title='Amount ($)'),
                       hovermode='x unified',
                       legend=dict(orientation='h',
                                   yanchor='bottom',
                                   y=1.02,
                                   xanchor='right',
                                   x=1),
                       height=400)

    st.plotly_chart(fig2, use_container_width=True)


def render_market_fit_tab():
    """Renders the market fit visualization tab"""
    st.subheader("Product-Market Fit Analysis")

    # Create market fit metrics
    col1, col2 = st.columns(2)

    with col1:
        # Product-Market Fit Radar Chart
        categories = [
            'Solving Real Problem', 'Target Market Size', 'Willingness to Pay',
            'Market Timing', 'Competitive Advantage', 'Scalability'
        ]

        # Generate random scores for demonstration
        market_fit_scores = [
            random.uniform(5, 10) for _ in range(len(categories))
        ]
        ideal_scores = [10] * len(categories)

        # Calculate overall fit percentage
        fit_percentage = sum(market_fit_scores) / sum(ideal_scores) * 100

        # Create a DataFrame
        df = pd.DataFrame({
            'Category':
            categories + categories,
            'Score':
            market_fit_scores + ideal_scores,
            'Type': ['Current'] * len(categories) + ['Ideal'] * len(categories)
        })

        # Create radar chart
        fig = px.line_polar(df,
                            r='Score',
                            theta='Category',
                            color='Type',
                            line_close=True,
                            color_discrete_sequence=['#00A67E', '#0A2540'],
                            range_r=[0, 10])

        fig.update_layout(
            title=f'Product-Market Fit Assessment: {fit_percentage:.1f}%',
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            height=400)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Target Market Analysis
        st.subheader("Target Market Segments")

        # Example market segments
        segments = [
            'Segment A', 'Segment B', 'Segment C', 'Segment D', 'Others'
        ]
        market_sizes = [random.uniform(10, 40) for _ in range(4)]
        market_sizes.append(100 - sum(market_sizes))  # Others

        growth_rates = [random.uniform(-5, 20) for _ in range(len(segments))]

        # Create a DataFrame
        market_df = pd.DataFrame({
            'Segment': segments,
            'Market Size (%)': market_sizes,
            'Growth Rate (%)': growth_rates
        })

        # Create treemap
        fig2 = px.treemap(
            market_df,
            path=['Segment'],
            values='Market Size (%)',
            color='Growth Rate (%)',
            color_continuous_scale=['#FF6B6B', '#FFFFFF', '#00A67E'],
            color_continuous_midpoint=0)

        fig2.update_layout(title='Target Market Segmentation', height=400)

        st.plotly_chart(fig2, use_container_width=True)

    # Customer Problem-Solution Fit
    st.subheader("Problem-Solution Fit")

    # Example problems and solution fit
    problems = [
        'Problem 1', 'Problem 2', 'Problem 3', 'Problem 4', 'Problem 5'
    ]

    solution_scores = [random.uniform(5, 10) for _ in range(len(problems))]
    importance_scores = [random.uniform(5, 10) for _ in range(len(problems))]

    # Create DataFrame
    problem_df = pd.DataFrame({
        'Problem':
        problems,
        'Solution Effectiveness':
        solution_scores,
        'Problem Importance':
        importance_scores,
        'Score': [
            solution_scores[i] * importance_scores[i] / 10
            for i in range(len(problems))
        ]
    })

    # Sort by score
    problem_df = problem_df.sort_values('Score', ascending=False)

    # Create horizontal bar chart
    fig3 = go.Figure()

    fig3.add_trace(
        go.Bar(y=problem_df['Problem'],
               x=problem_df['Score'],
               orientation='h',
               marker_color='#00A67E',
               name='Overall Score'))

    fig3.update_layout(title='Problem-Solution Fit Analysis',
                       xaxis=dict(title='Score (out of 10)'),
                       yaxis=dict(title='Customer Problem'),
                       height=350)

    st.plotly_chart(fig3, use_container_width=True)


def render_risk_assessment_tab():
    """Renders the risk assessment visualization tab"""
    st.subheader("Business Risk Assessment")

    # Risk matrix
    risk_categories = [
        'Market Risks', 'Financial Risks', 'Operational Risks',
        'Technology Risks', 'Regulatory Risks', 'Competitive Risks'
    ]

    # Generate random scores for demonstration
    impact_scores = [random.uniform(1, 5) for _ in range(len(risk_categories))]
    probability_scores = [
        random.uniform(1, 5) for _ in range(len(risk_categories))
    ]
    risk_scores = [
        impact_scores[i] * probability_scores[i] / 5
        for i in range(len(risk_categories))
    ]

    # Create a DataFrame
    risk_df = pd.DataFrame({
        'Risk Category': risk_categories,
        'Impact': impact_scores,
        'Probability': probability_scores,
        'Risk Score': risk_scores
    })

    # Create risk matrix bubble chart
    fig = px.scatter(risk_df,
                     x='Probability',
                     y='Impact',
                     size='Risk Score',
                     color='Risk Score',
                     hover_name='Risk Category',
                     text='Risk Category',
                     size_max=60,
                     color_continuous_scale='RdYlGn_r',
                     range_color=[0, 5])

    # Add quadrant lines
    fig.add_shape(type="line",
                  x0=2.5,
                  y0=0,
                  x1=2.5,
                  y1=5,
                  line=dict(color="gray", width=1, dash="dash"))

    fig.add_shape(type="line",
                  x0=0,
                  y0=2.5,
                  x1=5,
                  y1=2.5,
                  line=dict(color="gray", width=1, dash="dash"))

    # Add quadrant labels
    fig.add_annotation(x=1.25,
                       y=1.25,
                       text="Low Risk",
                       showarrow=False,
                       font=dict(size=14, color="green"))
    fig.add_annotation(x=3.75,
                       y=1.25,
                       text="Moderate Risk",
                       showarrow=False,
                       font=dict(size=14, color="orange"))
    fig.add_annotation(x=1.25,
                       y=3.75,
                       text="Moderate Risk",
                       showarrow=False,
                       font=dict(size=14, color="orange"))
    fig.add_annotation(x=3.75,
                       y=3.75,
                       text="High Risk",
                       showarrow=False,
                       font=dict(size=14, color="red"))

    fig.update_layout(title='Risk Assessment Matrix',
                      xaxis=dict(title='Probability', range=[0, 5]),
                      yaxis=dict(title='Impact', range=[0, 5]),
                      height=500)

    st.plotly_chart(fig, use_container_width=True)

    # Risk mitigation strategies
    st.subheader("Risk Mitigation Strategies")

    # Sort risks by score
    risk_df = risk_df.sort_values('Risk Score', ascending=False)

    # Display top 3 risks with mitigation strategies
    for i in range(min(3, len(risk_df))):
        risk = risk_df.iloc[i]
        with st.container(border=True):
            cols = st.columns([1, 4])

            with cols[0]:
                st.markdown(f"### {i+1}")
                severity = "High" if risk[
                    'Risk Score'] > 3.5 else "Medium" if risk[
                        'Risk Score'] > 2 else "Low"
                severity_color = "red" if severity == "High" else "orange" if severity == "Medium" else "green"
                st.markdown(
                    f"<p style='color:{severity_color};font-weight:bold'>{severity}</p>",
                    unsafe_allow_html=True)
                st.metric("Score", f"{risk['Risk Score']:.1f}/5")

            with cols[1]:
                st.subheader(risk['Risk Category'])

                # Generate example mitigation strategies
                mitigations = [
                    "Diversify supplier relationships to reduce dependency risks",
                    "Implement robust financial controls and cash flow monitoring",
                    "Develop contingency plans for key operational disruptions",
                    "Establish regulatory compliance monitoring and updates",
                    "Conduct regular market intelligence to track competitive landscape"
                ]

                st.markdown("**Mitigation Strategy:**")
                st.markdown(f"- {mitigations[i % len(mitigations)]}")
                st.markdown(
                    f"- Monitor {risk['Risk Category'].lower()} quarterly")
                st.markdown(
                    f"- Allocate {random.randint(5, 15)}% contingency budget")


def render_success_metrics_tab():
    """Renders the success metrics visualization tab"""
    st.subheader("Key Success Metrics & KPIs")

    # Create columns for different metric categories
    col1, col2 = st.columns(2)

    with col1:
        # Financial KPIs
        st.markdown("### Financial KPIs")

        financial_kpis = {
            "Customer Acquisition Cost (CAC)": f"${random.randint(100, 500)}",
            "Customer Lifetime Value (LTV)": f"${random.randint(1000, 5000)}",
            "LTV:CAC Ratio": f"{random.uniform(2, 8):.1f}",
            "Break-even Point": f"{random.randint(12, 36)} months",
            "Gross Margin": f"{random.uniform(30, 70):.1f}%"
        }

        for kpi, value in financial_kpis.items():
            st.metric(label=kpi, value=value)

    with col2:
        # Growth KPIs
        st.markdown("### Growth KPIs")

        growth_kpis = {
            "Market Share Target": f"{random.uniform(1, 25):.1f}%",
            "User/Customer Growth Rate":
            f"{random.uniform(5, 50):.1f}% monthly",
            "Activation Rate": f"{random.uniform(20, 80):.1f}%",
            "Retention Rate": f"{random.uniform(40, 95):.1f}%",
            "NPS (Net Promoter Score)": f"{random.randint(20, 80)}"
        }

        for kpi, value in growth_kpis.items():
            st.metric(label=kpi, value=value)

    # Critical success factors
    st.subheader("Critical Success Factors")

    # Example success factors
    success_factors = [
        "Market Penetration Rate", "Strategic Partnerships",
        "Technology Adoption", "Team Expertise & Execution",
        "Regulatory Compliance", "Funding/Capital Availability"
    ]

    # Generate scores and thresholds
    factor_scores = [
        random.uniform(0, 100) for _ in range(len(success_factors))
    ]
    factor_thresholds = [
        random.uniform(40, 70) for _ in range(len(success_factors))
    ]

    # Create DataFrame
    csf_df = pd.DataFrame({
        'Factor': success_factors,
        'Current Score': factor_scores,
        'Minimum Threshold': factor_thresholds
    })

    # Create bullet chart
    fig = go.Figure()

    for i, factor in enumerate(success_factors):
        fig.add_trace(
            go.Indicator(mode="gauge+number",
                         value=factor_scores[i],
                         domain={
                             'row': i,
                             'column': 0
                         },
                         title={'text': factor},
                         gauge={
                             'axis': {
                                 'range': [0, 100]
                             },
                             'threshold': {
                                 'line': {
                                     'color': "red",
                                     'width': 2
                                 },
                                 'thickness': 0.75,
                                 'value': factor_thresholds[i]
                             },
                             'steps': [{
                                 'range': [0, 30],
                                 'color': "#FF6B6B"
                             }, {
                                 'range': [30, 70],
                                 'color': "#FFD93D"
                             }, {
                                 'range': [70, 100],
                                 'color': "#00A67E"
                             }],
                             'bar': {
                                 'color': "#0A2540"
                             }
                         }))

    # Update layout
    fig.update_layout(grid={
        'rows': len(success_factors),
        'columns': 1,
        'pattern': "independent"
    },
                      height=100 * len(success_factors) + 50)

    st.plotly_chart(fig, use_container_width=True)
