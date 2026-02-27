import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="Indian Economic Growth Dashboard", layout="wide", initial_sidebar_state="expanded")

# ==================== DATA GENERATION ====================
np.random.seed(42)
years = np.arange(1990, 2024)
n = len(years)

# Base trends
gdp_growth = np.where(years < 2000, 5 + np.random.normal(0, 0.5, n), 7 + np.random.normal(0, 0.8, n))
gdp_growth[years == 2008] = 3.9
gdp_growth[(years >= 2009) & (years <= 2010)] += 2.5
gdp_growth[years == 2020] = -5.8
gdp_growth[years >= 2021] = 8.5 + np.random.normal(0, 0.5, 3)

inflation = 6 + np.sin(np.linspace(0, 4*np.pi, n)) * 2 + np.random.normal(0, 1, n)
inflation = np.clip(inflation, 3, 11)

fiscal_deficit = np.where(years < 2000, 5.5, 4.5) + np.random.normal(0, 0.7, n)
fiscal_deficit[years == 2008] = 6.0
fiscal_deficit[years == 2020] = 9.2

public_debt = 70 + np.cumsum(np.random.normal(0, 1, n) * 0.5)
public_debt = np.clip(public_debt, 65, 85)

fdi = np.where(years < 2000, 2, 10 + (years - 2000) * 2) + np.random.normal(0, 2, n)
fdi = np.clip(fdi, 0, 60)

private_gfcf = 20 + (years - 1990) * 1.5 + np.random.normal(0, 3, n)
private_gfcf = np.clip(private_gfcf, 18, 80)

iip = 50 + (years - 1990) * 3 + np.random.normal(0, 5, n)
iip = np.clip(iip, 40, 140)

forex_reserves = np.exp((years - 1990) / 12) * 10 + np.random.normal(0, 15, n)
forex_reserves = np.clip(forex_reserves, 5, 650)

exports = 20 + (years - 1990) * 4 + np.random.normal(0, 8, n)
exports = np.clip(exports, 18, 200)

imports = exports * (1 + np.random.normal(0.2, 0.1, n))
imports = np.clip(imports, 25, 250)

credit_growth = 12 + np.sin(np.linspace(0, 3*np.pi, n)) * 3 + np.random.normal(0, 1.5, n)
credit_growth = np.clip(credit_growth, 5, 20)

gdp = 500 * (1 + gdp_growth / 100).cumprod()

df = pd.DataFrame({
    'Year': years,
    'GDP': gdp,
    'GDP_Growth': gdp_growth,
    'Inflation': inflation,
    'Fiscal_Deficit': fiscal_deficit,
    'Public_Debt': public_debt,
    'FDI': fdi,
    'Private_GFCF': private_gfcf,
    'IIP': iip,
    'Forex_Reserves': forex_reserves,
    'Exports': exports,
    'Imports': imports,
    'Credit_Growth': credit_growth
})

df['Trade_Balance'] = df['Exports'] - df['Imports']
df['Debt_to_GDP'] = df['Public_Debt'] / (df['GDP'] / 1000)  # scaled for readability

# ==================== GENERATE WORLD GDP DATA ====================
countries = pd.DataFrame({
    'country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'France', 'India', 'Brazil', 
                'Italy', 'Canada', 'Russia', 'South Korea', 'Australia', 'Spain', 'Mexico', 'Indonesia',
                'Netherlands', 'Saudi Arabia', 'Turkey', 'Switzerland', 'Nigeria', 'Egypt', 'South Africa',
                'Thailand', 'Vietnam', 'Bangladesh', 'Malaysia', 'Philippines', 'Pakistan', 'Kenya'],
    'iso_alpha': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'IND', 'BRA', 
                  'ITA', 'CAN', 'RUS', 'KOR', 'AUS', 'ESP', 'MEX', 'IDN',
                  'NLD', 'SAU', 'TUR', 'CHE', 'NGA', 'EGY', 'ZAF',
                  'THA', 'VNM', 'BGD', 'MYS', 'PHL', 'PAK', 'KEN']
})

# Assign GDP categories (High, Medium, Low) with some logic
np.random.seed(123)
gdp_category = []
for i, row in countries.iterrows():
    if row['country'] in ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'France']:
        cat = 'High'
    elif row['country'] in ['India', 'Brazil', 'Russia', 'Mexico', 'Indonesia', 'Turkey']:
        cat = 'Medium'
    elif row['country'] in ['Nigeria', 'Egypt', 'Pakistan', 'Kenya']:
        cat = 'Low'
    else:
        # random for others
        cat = np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.5, 0.3])
    gdp_category.append(cat)

countries['GDP_Category'] = gdp_category

# ==================== CONSTANTS ====================
BG_COLOR = '#0a0a0a'
CARD_BG = '#141414'
NEON_BLUE = '#00f5ff'
NEON_GREEN = '#39ff14'
NEON_ORANGE = '#ff8c00'
NEON_YELLOW = '#ffd60a'
NEON_RED = '#ff3131'
NEON_PURPLE = '#bc13fe'

SHAPES = [
    dict(type='rect', x0=1990.5, x1=1991.5, y0=0, y1=1, yref='paper', fillcolor='rgba(255,255,255,0.05)', line_width=0),
    dict(type='rect', x0=2007.5, x1=2008.5, y0=0, y1=1, yref='paper', fillcolor='rgba(255,255,255,0.05)', line_width=0),
    dict(type='rect', x0=2019.5, x1=2020.5, y0=0, y1=1, yref='paper', fillcolor='rgba(255,255,255,0.05)', line_width=0)
]

def dark_layout(title='', yaxis_title='', xaxis_title=''):
    return go.Layout(
        title=title,
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333', linecolor='#333', title=xaxis_title),
        yaxis=dict(gridcolor='#333', linecolor='#333', title=yaxis_title),
        hoverlabel=dict(bgcolor=CARD_BG, font_color='white'),
        shapes=SHAPES,
        margin=dict(l=50, r=20, t=40, b=40)
    )

# ==================== SIDEBAR ====================
st.sidebar.markdown("## Year Range")
start_year, end_year = st.sidebar.slider(
    "Select range",
    min_value=1990, max_value=2023, value=(1990, 2023),
    step=1
)

dff = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

# ==================== KPI CARDS (custom HTML/CSS) ====================
st.markdown(
    f"""
    <style>
    .kpi-card {{
        background-color: {CARD_BG};
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0,245,255,0.25);
        text-align: center;
        color: white;
    }}
    .kpi-card h4 {{
        margin: 0;
        color: {NEON_BLUE};
    }}
    .kpi-card h2 {{
        margin: 5px 0 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("# Indian Economic Growth Dashboard (1990–2023)")

cols = st.columns(5)
with cols[0]:
    st.markdown(f'<div class="kpi-card"><h4>GDP Growth</h4><h2>{dff["GDP_Growth"].iloc[-1]:.1f}%</h2></div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown(f'<div class="kpi-card" style="box-shadow:0 0 15px {NEON_ORANGE}40;"><h4 style="color:{NEON_ORANGE};">Inflation</h4><h2>{dff["Inflation"].iloc[-1]:.1f}%</h2></div>', unsafe_allow_html=True)
with cols[2]:
    st.markdown(f'<div class="kpi-card" style="box-shadow:0 0 15px {NEON_RED}40;"><h4 style="color:{NEON_RED};">Fiscal Deficit</h4><h2>{dff["Fiscal_Deficit"].iloc[-1]:.1f}%</h2></div>', unsafe_allow_html=True)
with cols[3]:
    st.markdown(f'<div class="kpi-card" style="box-shadow:0 0 15px {NEON_GREEN}40;"><h4 style="color:{NEON_GREEN};">FDI (Bn USD)</h4><h2>{dff["FDI"].iloc[-1]:.1f}</h2></div>', unsafe_allow_html=True)
with cols[4]:
    st.markdown(f'<div class="kpi-card" style="box-shadow:0 0 15px {NEON_YELLOW}40;"><h4 style="color:{NEON_YELLOW};">Forex Reserves</h4><h2>{dff["Forex_Reserves"].iloc[-1]:.0f} Bn</h2></div>', unsafe_allow_html=True)

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", "Public Sector", "Private Sector", "External Sector", "3D Analytics", "More Charts", "Global GDP"])

# ----- Overview -----
with tab1:
    st.subheader("GDP Growth vs Inflation")
    fig1 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig1.add_trace(go.Scatter(x=dff['Year'], y=dff['GDP_Growth'], mode='lines+markers', name='GDP Growth', line=dict(color=NEON_BLUE, width=3)))
    fig1.add_trace(go.Scatter(x=dff['Year'], y=dff['Inflation'], mode='lines+markers', name='Inflation', line=dict(color=NEON_ORANGE, width=3)))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("GDP Growth Trend")
    fig2 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig2.add_trace(go.Bar(x=dff['Year'], y=dff['GDP_Growth'], name='GDP Growth', marker_color=NEON_GREEN))
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Credit Growth")
    fig3 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig3.add_trace(go.Scatter(x=dff['Year'], y=dff['Credit_Growth'], mode='lines+markers', line=dict(color=NEON_PURPLE, width=3), name='Credit Growth'))
    st.plotly_chart(fig3, use_container_width=True)

    # Additional chart: GDP vs Public Debt
    st.subheader("GDP vs Public Debt")
    fig1a = go.Figure(layout=dark_layout(yaxis_title='Value'))
    fig1a.add_trace(go.Scatter(x=dff['Year'], y=dff['GDP']/1000, mode='lines+markers', name='GDP (Bn USD)', line=dict(color=NEON_YELLOW, width=3)))
    fig1a.add_trace(go.Scatter(x=dff['Year'], y=dff['Public_Debt'], mode='lines+markers', name='Public Debt (% of GDP)', line=dict(color=NEON_RED, width=3), yaxis='y2'))
    fig1a.update_layout(yaxis2=dict(title='Public Debt (%)', overlaying='y', side='right', gridcolor='#333'))
    st.plotly_chart(fig1a, use_container_width=True)

# ----- Public Sector -----
with tab2:
    st.subheader("Fiscal Deficit")
    fig4 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig4.add_trace(go.Scatter(x=dff['Year'], y=dff['Fiscal_Deficit'], mode='lines+markers', line=dict(color=NEON_RED, width=3), name='Fiscal Deficit'))
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Public Debt")
    fig5 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig5.add_trace(go.Scatter(x=dff['Year'], y=dff['Public_Debt'], mode='lines+markers', line=dict(color=NEON_YELLOW, width=3), name='Public Debt'))
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Fiscal Indicators")
    fig6 = go.Figure(layout=dark_layout(yaxis_title='Percent'))
    fig6.add_trace(go.Bar(x=dff['Year'], y=dff['Fiscal_Deficit'], name='Fiscal Deficit', marker_color=NEON_RED))
    fig6.add_trace(go.Bar(x=dff['Year'], y=dff['Debt_to_GDP'], name='Debt/GDP', marker_color=NEON_ORANGE))
    fig6.update_layout(barmode='group')
    st.plotly_chart(fig6, use_container_width=True)

    # Additional chart: Public Debt vs Inflation
    st.subheader("Public Debt vs Inflation")
    fig2a = go.Figure(layout=dark_layout(xaxis_title='Public Debt (%)', yaxis_title='Inflation (%)'))
    fig2a.add_trace(go.Scatter(x=dff['Public_Debt'], y=dff['Inflation'], mode='markers', marker=dict(color=dff['Year'], colorscale='Viridis', size=8, showscale=True, colorbar=dict(title='Year')), text=dff['Year'], hoverinfo='text+x+y'))
    st.plotly_chart(fig2a, use_container_width=True)

# ----- Private Sector -----
with tab3:
    st.subheader("Private Gross Fixed Capital Formation")
    fig7 = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    fig7.add_trace(go.Scatter(x=dff['Year'], y=dff['Private_GFCF'], mode='lines+markers', line=dict(color=NEON_GREEN, width=3), name='Private GFCF'))
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Index of Industrial Production")
    fig8 = go.Figure(layout=dark_layout(yaxis_title='Index'))
    fig8.add_trace(go.Scatter(x=dff['Year'], y=dff['IIP'], mode='lines+markers', line=dict(color=NEON_BLUE, width=3), name='IIP'))
    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("Foreign Direct Investment")
    fig9 = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    fig9.add_trace(go.Scatter(x=dff['Year'], y=dff['FDI'], mode='lines+markers', line=dict(color=NEON_PURPLE, width=3), name='FDI'))
    st.plotly_chart(fig9, use_container_width=True)

    # Additional chart: IIP vs Credit Growth
    st.subheader("IIP vs Credit Growth")
    fig3a = go.Figure(layout=dark_layout(yaxis_title='Value'))
    fig3a.add_trace(go.Scatter(x=dff['Year'], y=dff['IIP'], mode='lines+markers', name='IIP', line=dict(color=NEON_GREEN, width=3)))
    fig3a.add_trace(go.Scatter(x=dff['Year'], y=dff['Credit_Growth'], mode='lines+markers', name='Credit Growth', line=dict(color=NEON_PURPLE, width=3), yaxis='y2'))
    fig3a.update_layout(yaxis2=dict(title='Credit Growth (%)', overlaying='y', side='right', gridcolor='#333'))
    st.plotly_chart(fig3a, use_container_width=True)

# ----- External Sector -----
with tab4:
    st.subheader("Exports vs Imports")
    fig10 = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    fig10.add_trace(go.Scatter(x=dff['Year'], y=dff['Exports'], mode='lines+markers', name='Exports', line=dict(color=NEON_GREEN, width=3)))
    fig10.add_trace(go.Scatter(x=dff['Year'], y=dff['Imports'], mode='lines+markers', name='Imports', line=dict(color=NEON_RED, width=3)))
    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("Trade Balance")
    fig11 = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    colors = [NEON_GREEN if val >= 0 else NEON_RED for val in dff['Trade_Balance']]
    fig11.add_trace(go.Bar(x=dff['Year'], y=dff['Trade_Balance'], marker_color=colors))
    st.plotly_chart(fig11, use_container_width=True)

    st.subheader("Forex Reserves")
    fig12 = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    fig12.add_trace(go.Scatter(x=dff['Year'], y=dff['Forex_Reserves'], mode='lines+markers', line=dict(color=NEON_YELLOW, width=3), name='Forex Reserves'))
    st.plotly_chart(fig12, use_container_width=True)

    # Additional chart: Forex Reserves vs FDI
    st.subheader("Forex Reserves vs FDI")
    fig4a = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
    fig4a.add_trace(go.Scatter(x=dff['Year'], y=dff['Forex_Reserves'], mode='lines+markers', name='Forex Reserves', line=dict(color=NEON_YELLOW, width=3)))
    fig4a.add_trace(go.Scatter(x=dff['Year'], y=dff['FDI'], mode='lines+markers', name='FDI', line=dict(color=NEON_GREEN, width=3), yaxis='y2'))
    fig4a.update_layout(yaxis2=dict(title='FDI (Bn USD)', overlaying='y', side='right', gridcolor='#333'))
    st.plotly_chart(fig4a, use_container_width=True)

# ----- 3D Analytics -----
with tab5:
    st.subheader("3D Scatter: GDP Growth, Inflation, FDI")
    fig13 = go.Figure(data=[go.Scatter3d(
        x=dff['GDP_Growth'],
        y=dff['Inflation'],
        z=dff['FDI'],
        mode='markers',
        marker=dict(
            size=8,
            color=dff['Year'],
            colorscale='Viridis',
            line=dict(width=2, color='white'),
            colorbar=dict(title='Year')
        ),
        text=dff['Year'],
        hoverinfo='text+x+y+z'
    )])
    fig13.update_layout(
        scene=dict(
            xaxis=dict(title='GDP Growth', gridcolor='#333'),
            yaxis=dict(title='Inflation', gridcolor='#333'),
            zaxis=dict(title='FDI', gridcolor='#333'),
            bgcolor=BG_COLOR
        ),
        paper_bgcolor=BG_COLOR,
        font=dict(color='white'),
        title='GDP Growth vs Inflation vs FDI'
    )
    st.plotly_chart(fig13, use_container_width=True)

    # Additional 3D: Exports, Imports, FDI
    st.subheader("3D Scatter: Exports, Imports, FDI")
    fig5a = go.Figure(data=[go.Scatter3d(
        x=dff['Exports'],
        y=dff['Imports'],
        z=dff['FDI'],
        mode='markers',
        marker=dict(
            size=8,
            color=dff['Year'],
            colorscale='Plasma',
            line=dict(width=2, color='white'),
            colorbar=dict(title='Year')
        ),
        text=dff['Year'],
        hoverinfo='text+x+y+z'
    )])
    fig5a.update_layout(
        scene=dict(
            xaxis=dict(title='Exports', gridcolor='#333'),
            yaxis=dict(title='Imports', gridcolor='#333'),
            zaxis=dict(title='FDI', gridcolor='#333'),
            bgcolor=BG_COLOR
        ),
        paper_bgcolor=BG_COLOR,
        font=dict(color='white'),
        title='Exports vs Imports vs FDI'
    )
    st.plotly_chart(fig5a, use_container_width=True)

# ----- More Charts -----
with tab6:
    st.subheader("Additional Economic Indicators")

    colA, colB = st.columns(2)

    with colA:
        # Inflation vs Credit Growth
        fig6a = go.Figure(layout=dark_layout(yaxis_title='Percent'))
        fig6a.add_trace(go.Scatter(x=dff['Year'], y=dff['Inflation'], mode='lines+markers', name='Inflation', line=dict(color=NEON_ORANGE, width=3)))
        fig6a.add_trace(go.Scatter(x=dff['Year'], y=dff['Credit_Growth'], mode='lines+markers', name='Credit Growth', line=dict(color=NEON_PURPLE, width=3)))
        st.plotly_chart(fig6a, use_container_width=True)

        # Fiscal Deficit vs GDP Growth scatter
        fig6c = go.Figure(layout=dark_layout(xaxis_title='GDP Growth (%)', yaxis_title='Fiscal Deficit (%)'))
        fig6c.add_trace(go.Scatter(x=dff['GDP_Growth'], y=dff['Fiscal_Deficit'], mode='markers', marker=dict(color=dff['Year'], colorscale='Viridis', size=8, showscale=True, colorbar=dict(title='Year')), text=dff['Year'], hoverinfo='text+x+y'))
        st.plotly_chart(fig6c, use_container_width=True)

    with colB:
        # Private GFCF vs IIP
        fig6b = go.Figure(layout=dark_layout(yaxis_title='Value'))
        fig6b.add_trace(go.Scatter(x=dff['Year'], y=dff['Private_GFCF'], mode='lines+markers', name='Private GFCF', line=dict(color=NEON_GREEN, width=3)))
        fig6b.add_trace(go.Scatter(x=dff['Year'], y=dff['IIP'], mode='lines+markers', name='IIP', line=dict(color=NEON_BLUE, width=3), yaxis='y2'))
        fig6b.update_layout(yaxis2=dict(title='IIP', overlaying='y', side='right', gridcolor='#333'))
        st.plotly_chart(fig6b, use_container_width=True)

        # Forex Reserves vs Trade Balance
        fig6d = go.Figure(layout=dark_layout(yaxis_title='Bn USD'))
        fig6d.add_trace(go.Scatter(x=dff['Year'], y=dff['Forex_Reserves'], mode='lines+markers', name='Forex Reserves', line=dict(color=NEON_YELLOW, width=3)))
        fig6d.add_trace(go.Bar(x=dff['Year'], y=dff['Trade_Balance'], name='Trade Balance', marker_color=NEON_RED, yaxis='y2'))
        fig6d.update_layout(yaxis2=dict(title='Trade Balance (Bn USD)', overlaying='y', side='right', gridcolor='#333'))
        st.plotly_chart(fig6d, use_container_width=True)

    # Full-width chart: Debt to GDP over time
    st.subheader("Debt to GDP Ratio Trend")
    fig6e = go.Figure(layout=dark_layout(yaxis_title='Ratio'))
    fig6e.add_trace(go.Scatter(x=dff['Year'], y=dff['Debt_to_GDP'], mode='lines+markers', line=dict(color=NEON_PURPLE, width=3), name='Debt/GDP'))
    st.plotly_chart(fig6e, use_container_width=True)

    # 3D line plot of GDP over time with growth and inflation
    st.subheader("3D Line: GDP, Growth, Inflation over Time")
    fig6f = go.Figure(data=[go.Scatter3d(
        x=dff['Year'],
        y=dff['GDP_Growth'],
        z=dff['Inflation'],
        mode='lines+markers',
        line=dict(color=NEON_BLUE, width=4),
        marker=dict(size=4, color=dff['Year'], colorscale='Viridis'),
        text=dff['Year'],
        hoverinfo='text+x+y+z'
    )])
    fig6f.update_layout(
        scene=dict(
            xaxis=dict(title='Year', gridcolor='#333'),
            yaxis=dict(title='GDP Growth', gridcolor='#333'),
            zaxis=dict(title='Inflation', gridcolor='#333'),
            bgcolor=BG_COLOR
        ),
        paper_bgcolor=BG_COLOR,
        font=dict(color='white'),
        title='GDP Growth and Inflation over Time'
    )
    st.plotly_chart(fig6f, use_container_width=True)

# ----- Global GDP -----
with tab7:
    st.subheader("World GDP Categories (High / Medium / Low)")
    
    # Create choropleth map
    fig_world = px.choropleth(
        countries,
        locations='iso_alpha',
        color='GDP_Category',
        hover_name='country',
        color_discrete_map={'High': NEON_GREEN, 'Medium': NEON_YELLOW, 'Low': NEON_RED},
        title='Global GDP Classification',
        projection='natural earth'
    )
    fig_world.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        geo=dict(bgcolor=BG_COLOR, showframe=False, showcoastlines=True, coastlinecolor='#333')
    )
    st.plotly_chart(fig_world, use_container_width=True)

    st.markdown("---")
    st.subheader("Country-wise GDP Category")
    st.dataframe(countries[['country', 'GDP_Category']].style.applymap(lambda x: f'color: {NEON_GREEN}' if x=='High' else (f'color: {NEON_YELLOW}' if x=='Medium' else f'color: {NEON_RED}'), subset=['GDP_Category']))
