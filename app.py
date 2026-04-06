import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Calorie Tracker", layout="wide")

st.title("🥗  Diet & Calorie Tracker")

# ---------------- USER GOALS ---------------- #

st.sidebar.header("🎯 Your Goals")

calorie_goal = st.sidebar.number_input("Daily Calorie Goal", value=2000)
protein_goal = st.sidebar.number_input("Daily Protein Goal (g)", value=120)

# ---------------- LOAD FOOD DATA ---------------- #

@st.cache_data
def load_data():
    return pd.read_csv("indian_food.csv")

df_food = load_data()

# ---------------- AI MODEL ---------------- #

# Simple training data
X = [
    [1800, 120],
    [2500, 60],
    [2000, 100],
    [3000, 40],
    [1700, 130]
]

y = [1, 0, 1, 0, 1]  # 1 = good diet, 0 = poor diet

model = LogisticRegression()
model.fit(X, y)

# ---------------- SESSION ---------------- #

if "diet" not in st.session_state:
    st.session_state.diet = []

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT ---------------- #

st.sidebar.header("🍽️ Add Food")

search = st.sidebar.text_input("Search Food")

filtered_food = df_food[df_food["Food"].str.contains(search, case=False)] if search else df_food

food = st.sidebar.selectbox("Select Food", filtered_food["Food"])

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

    # Save history
    st.session_state.history.append(total_cal)

    col1, col2 = st.columns(2)

    col1.metric("🔥 Total Calories", f"{total_cal} kcal", delta=total_cal - calorie_goal)
    col2.metric("💪 Protein Intake", f"{total_protein} g", delta=total_protein - protein_goal)

    # ---------------- PROGRESS ---------------- #

    st.subheader("📊 Progress vs Goals")

    progress_df = pd.DataFrame({
        "Metric": ["Calories", "Protein"],
        "Consumed": [total_cal, total_protein],
        "Goal": [calorie_goal, protein_goal]
    }).set_index("Metric")

    st.bar_chart(progress_df)

    # ---------------- FOOD LOG ---------------- #

    st.subheader("🍽️ Food Log")
    st.dataframe(df)

    # ---------------- AI INSIGHTS ---------------- #

    st.subheader("🧠 AI Diet Insights")

    cal_diff = total_cal - calorie_goal
    protein_diff = total_protein - protein_goal

    prediction = model.predict([[total_cal, total_protein]])[0]

    if prediction == 1:
        st.success(" Your diet pattern looks balanced")
    else:
        st.error("⚠️ Your diet pattern needs improvement")

    # Rule-based logic
    if cal_diff < -200:
        st.info("You are in a calorie deficit (cutting)")
    elif cal_diff > 200:
        st.warning("You are in a calorie surplus (bulking)")
    else:
        st.success("You are near maintenance calories")

    if protein_diff < -20:
        st.warning("Protein intake is low. Increase protein sources.")
    elif protein_diff > 0:
        st.success("Great protein intake!")

    # ---------------- SMART RECOMMENDATIONS ---------------- #

    st.subheader("🍽️ Smart Recommendations")

    if protein_diff < -20:
        high_protein = df_food.sort_values(by="Protein", ascending=False).head(5)
        st.write("🔼 High protein foods you should eat:")
        st.dataframe(high_protein[["Food", "Protein"]])

    if cal_diff < -200:
        high_cal = df_food.sort_values(by="Calories", ascending=False).head(5)
        st.write("🔥 High calorie foods for energy:")
        st.dataframe(high_cal[["Food", "Calories"]])

    # ---------------- TREND ---------------- #

    if len(st.session_state.history) > 1:
        st.subheader("📈 Calorie Trend")
        st.line_chart(st.session_state.history)

    # ---------------- RESET ---------------- #

    if st.button("🔄 Reset Day"):
        st.session_state.diet = []
        st.session_state.history = []
        st.success("Reset successful!")

else:
    st.info("Add food from sidebar to start tracking")
