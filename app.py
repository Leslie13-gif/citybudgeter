# CityBudgeter – Streamlit MVP

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Load city cost data
# -------------------------
cities_data = pd.DataFrame({
    "City": [
        "Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Leipzig", "Stuttgart",
        "Heidelberg", "Mainz", "Freiburg", "Gießen", "Mannheim", "Bonn", "Dresden", "Erlangen"
    ],
    "Rent": [
        1000, 1300, 1100, 1150, 950, 750, 1200,
        850, 800, 900, 700, 850, 800, 750, 770
    ],
    "Food": [
        300, 320, 310, 290, 280, 270, 310,
        270, 260, 275, 250, 265, 260, 255, 250
    ],
    "Transport": [
        80, 90, 85, 85, 80, 70, 90,
        75, 70, 75, 65, 75, 70, 65, 60
    ]
})

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="CityBudgeter", layout="centered")
st.title("🏙️ CityBudgeter – Student Living in Germany")

st.markdown("""
Compare the cost of living in different German cities and calculate whether your student budget allows for a comfortable life and additional savings.

**Minimum for student visa:** 11,904 € per year or 992 € per month
""")

# Monthly income input
income = st.slider("Your monthly budget (€):", 700, 3000, 992, step=50)

# Optional additional income (e.g. side job, support)
extra_income = st.slider("Additional income (e.g. from side job or family) (€):", 0, 1500, 0, step=50)

total_income = income + extra_income

# Savings goal input
with st.expander("🎯 Choose or set a savings goal"):
    goal_options = {
        "Bike": 400,
        "Smartphone": 800,
        "Laptop": 1200,
        "Trip to Spain": 600,
        "Car": 5000,
        "Custom goal": None
    }
    selected_goal = st.selectbox("Choose your savings goal:", list(goal_options.keys()))

    if selected_goal != "Custom goal":
        goal_name = selected_goal
        goal_amount = goal_options[selected_goal]
    else:
        goal_name = st.text_input("Enter custom goal name", "My Goal")
        goal_amount = st.number_input("Enter custom goal amount (€):", min_value=0, value=300, step=50)

    goal_months = st.slider("How many months to save for it:", 1, 24, 3)

# City selection
cities_selected = st.multiselect("Select up to 3 cities to compare:", cities_data["City"].tolist(), default=["Berlin", "Leipzig"])

# -------------------------
# Calculations and visualization
# -------------------------
if cities_selected:
    results = []

    for city in cities_selected:
        row = cities_data[cities_data["City"] == city].iloc[0]
        total_expenses = row["Rent"] + row["Food"] + row["Transport"]
        leftover = total_income - total_expenses
        total_savings = max(0, leftover * goal_months)
        enough_for_goal = total_savings >= goal_amount

        if not enough_for_goal:
            needed = goal_amount - total_savings
            extra_needed_per_month = int((needed / goal_months) + 1)
            suggestion = f"❗ Consider earning +{extra_needed_per_month}€/month to reach your goal"
        else:
            suggestion = "✅ Goal achievable with your current budget"

        results.append({
            "City": city,
            "Total Expenses (€)": total_expenses,
            "Leftover (€)": leftover,
            f"Savings in {goal_months} Months (€)": total_savings,
            "Can Reach Goal": "✅ Yes" if enough_for_goal else "❌ No",
            "Advice": suggestion
        })

    results_df = pd.DataFrame(results)

    # Display table
    st.subheader("📊 Comparison of selected cities")
    st.dataframe(results_df.set_index("City"))

    # Expenses and leftover bar chart
    fig = px.bar(
        results_df,
        x="City",
        y=["Total Expenses (€)", "Leftover (€)"],
        title="Monthly Expenses and Leftover Budget",
        labels={"value": "€", "variable": "Category"},
        barmode="stack",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one city to compare.")

