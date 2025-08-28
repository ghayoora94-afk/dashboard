import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Pakistan Electrification Dashboard", layout="wide")

# ---------------- Data ----------------
demand_by_income = pd.DataFrame([
    {"group": "Lower", "households": 16.875, "additionalDemand": 123.5, "percentage": 45},
    {"group": "Lower Middle", "households": 11.25, "additionalDemand": 96.4, "percentage": 30},
    {"group": "Middle", "households": 5.625, "additionalDemand": 74.7, "percentage": 15},
    {"group": "Upper Middle", "households": 3.0, "additionalDemand": 61.0, "percentage": 8},
    {"group": "Upper", "households": 0.75, "additionalDemand": 25.4, "percentage": 2},
])

grid_metrics = pd.DataFrame([
    {"metric": "Annual Generation (TWh)", "current": 110, "post": 491, "increase": 346},
    {"metric": "Peak Demand (GW)", "current": 32.5, "post": 133, "increase": 309},
    {"metric": "Residential Share (TWh)", "current": 55, "post": 436, "increase": 693},
])

fuel_shift = pd.DataFrame([
    {"name": "LPG Shift", "value": 60},
    {"name": "Natural Gas Shift", "value": 30},
    {"name": "Biomass Shift", "value": 10},
])

projected_peak = pd.DataFrame([
    {"year": 2025, "baseline": 35, "partial": 35, "full": 35},
    {"year": 2026, "baseline": 35, "partial": 45, "full": 70},
    {"year": 2027, "baseline": 35, "partial": 55, "full": 95},
    {"year": 2028, "baseline": 35, "partial": 65, "full": 115},
    {"year": 2029, "baseline": 35, "partial": 74, "full": 130},
    {"year": 2030, "baseline": 35, "partial": 84, "full": 133},
])

infrastructure_costs = pd.DataFrame([
    {"component": "Generation", "cost": 12.5},
    {"component": "Transmission", "cost": 2.5},
    {"component": "Distribution", "cost": 4.0},
    {"component": "Storage", "cost": 1.5},
])

household_consumption = pd.DataFrame([
    {"group": "Lower", "monthlyKWh": 610, "households": 16.875, "totalGWh": 10.29},
    {"group": "Lower Middle", "monthlyKWh": 714, "households": 11.25, "totalGWh": 8.03},
    {"group": "Middle", "monthlyKWh": 1107, "households": 5.625, "totalGWh": 6.23},
    {"group": "Upper Middle", "monthlyKWh": 1694, "households": 3.0, "totalGWh": 5.08},
    {"group": "Upper", "monthlyKWh": 2824, "households": 0.75, "totalGWh": 2.12},
])

# ---------------- Layout ----------------
st.title("⚡ Pakistan Residential Electrification Impact Analysis")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Households", "37.5M")
col2.metric("Additional Demand", "381 TWh/yr")
col3.metric("Current Capacity", "46 GW")
col4.metric("Required Capacity", "133 GW")

# Tabs
selected_tab = st.tabs(["Demand Analysis", "Grid Impact", "Infrastructure", "Timeline"])

# ---------------- Demand Analysis ----------------
with selected_tab[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Additional Demand by Income Group")
        fig = px.bar(demand_by_income, x="group", y="additionalDemand", color="group", text="additionalDemand",
                     labels={"additionalDemand": "TWh/year"})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Fuel Shift Composition")
        fig = px.pie(fuel_shift, values="value", names="name", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Consumption by Income Group")
    fig = go.Figure()
    fig.add_bar(x=household_consumption["group"], y=household_consumption["monthlyKWh"], name="Monthly kWh per HH")
    fig.add_trace(go.Scatter(x=household_consumption["group"], y=household_consumption["totalGWh"],
                             name="Total GWh", mode="lines+markers", yaxis="y2"))
    fig.update_layout(yaxis=dict(title="Monthly kWh"),
                      yaxis2=dict(title="Total GWh", overlaying="y", side="right"))
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Grid Impact ----------------
with selected_tab[1]:
    st.subheader("Grid Metrics")
    fig = go.Figure()
    fig.add_trace(go.Bar(y=grid_metrics["metric"], x=grid_metrics["current"], name="Current", orientation='h'))
    fig.add_trace(go.Bar(y=grid_metrics["metric"], x=grid_metrics["post"], name="Post-Electrification", orientation='h'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Critical Grid Challenges:**")
    st.error("- Current shortfall: 87 GW additional needed")
    st.error("- Equivalent to 87,000 wind turbines or 435 nuclear reactors")
    st.error("- Rural load-shedding could worsen (8–12 hrs)")
    st.error("- Current grid losses of 18–20% make it worse")

# ---------------- Infrastructure ----------------
with selected_tab[2]:
    st.subheader("Infrastructure Investment Requirements")
    fig = px.bar(infrastructure_costs, x="component", y="cost", color="component",
                 labels={"cost": "Trillion PKR"})
    st.plotly_chart(fig, use_container_width=True)
    st.info("Total Investment Required: PKR 16–25 Trillion over 15 years")

    col1, col2 = st.columns(2)
    with col1:
        st.success("""**Generation Requirements**
- +87 GW new capacity
- Focus on renewables (currently 54%)
- Solar already 25% of generation
- PKR 10–15 trillion investment""")
    with col2:
        st.success("""**Storage & Distribution**
- 20–30 GWh battery storage by 2030
- 50–100% more transformers needed
- Smart grids for peak mgmt
- Reduce 18–20% losses""")

# ---------------- Timeline ----------------
with selected_tab[3]:
    st.subheader("Projected Peak Demand (2025–2030)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=projected_peak["year"], y=projected_peak["baseline"], mode="lines+markers", name="Baseline"))
    fig.add_trace(go.Scatter(x=projected_peak["year"], y=projected_peak["partial"], mode="lines+markers", name="50% Adoption"))
    fig.add_trace(go.Scatter(x=projected_peak["year"], y=projected_peak["full"], mode="lines+markers", name="Full Adoption"))
    st.plotly_chart(fig, use_container_width=True)

    st.warning("Without infra investment, blackouts could 2–3x with full electrification.")

    col1, col2 = st.columns(2)
    with col1:
        st.info("**Short-term (2025–2028)**\n- Full electrification impossible\n- 20–30 GW shortfalls\n- Load-shedding worsens\n- Start phased approach")
    with col2:
        st.info("**Long-term (2030+)**\n- Feasible with massive investment\n- +50 GW renewables\n- Smart metering for peak shifting\n- Subsidies for poor groups")

# ---------------- Insights ----------------
st.header("Key Insights & Recommendations")
col1, col2, col3 = st.columns(3)
col1.error("Critical Challenge: 3.5x current generation required (381 TWh vs 110 TWh now)")
col2.info("Infrastructure Gap: PKR 16–25 Trillion investment needed, 15 years")
col3.success("Feasible Solution: Phased approach, urban-first, renewables + smart grids")
