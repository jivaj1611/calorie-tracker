import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diet Tracker", layout="wide")

st.title("🥗 Smart Diet & Calorie Tracker")

# ---------------- FOOD DATABASE ---------------- #

food_data = {
    "Food": [
        "Rice (1 plate)", "Roti (1)", "Egg (1)", "Chicken (100g)",
        "Paneer (100g)", "Milk (1 glass)", "Banana (1)",
        "Apple (1)", "Soya Chunks (50g)", "Oats (50g)"
    ],
    "Calories": [250, 100, 70, 165, 265, 150, 100, 95, 170, 190],
    "Protein": [5, 3, 6, 31, 18, 8, 1, 0, 26, 6]
}

df_food = pd.DataFrame(food_data)

# ---------------- SESSION ---------------- #

if "diet" not in st.session_state:
    st.session_state.diet = []

# ---------------- INPUT ---------------- #

st.sidebar.header("Add Food")

food = st.sidebar.selectbox("Select Food", df_food["Food"])

quantity = st.sidebar.number_input("Quantity", min_value=1, value=1)

if st.sidebar.button("Add Food"):

    food_row = df_food[df_food["Food"] == food].iloc[0]

    entry = {
        "Food": food,
        "Calories": food_row["Calories"] * quantity,
        "Protein": food_row["Protein"] * quantity
    }

    st.session_state.diet.append(entry)

    st.sidebar.success("Added!")

# ---------------- DASHBOARD ---------------- #

if st.session_state.diet:

    df = pd.DataFrame(st.session_state.diet)

    total_cal = df["Calories"].sum()
    total_protein = df["Protein"].sum()

    col1, col2 = st.columns(2)

    col1.metric("🔥 Total Calories", f"{total_cal} kcal")
    col2.metric("💪 Protein Intake", f"{total_protein} g")

    # ---------------- TABLE ---------------- #

    st.subheader("🍽️ Food Log")
    st.dataframe(df)

    # ---------------- INSIGHTS ---------------- #

    st.subheader("🧠 Diet Insights")

    if total_cal < 1800:
        st.info("You are in calorie deficit (cutting)")
    elif total_cal > 2500:
        st.warning("High calorie intake (bulking)")
    else:
        st.success("Maintenance calories range")

    if total_protein < 80:
        st.warning("Low protein intake")
    elif total_protein > 120:
        st.success("Great protein intake")

else:
    st.info("Add food from sidebar to start tracking")
