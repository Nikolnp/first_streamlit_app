from random import random
import streamlit as st
import pandas as pd
from database import load_emissions

# =========================================================
# 🌍 HOUSEHOLD SUSTAINABILITY CALCULATOR (SQL + IQR READY)
# =========================================================
def  sustainability_section():
    st.title("🌍 Household Sustainability Calculator")
    # ---------------- CONSTANTS ----------------
    FACTORS = {
        "electricity": 0.4,
        "water": 0.34,
        "car": 0.2,
        "diet": {
            "Plant-based": 120,
            "Mixed": 200,
            "Meat-heavy": 350
        }
    }   
    # ---------------- CORE CALC ----------------
    def calculate_emissions(electricity, water, car_km, diet):
        electricity_em = electricity * FACTORS["electricity"]
        water_em = water * FACTORS["water"]
        car_em = car_km * FACTORS["car"]
        food_em = FACTORS["diet"][diet]

        total = electricity_em + water_em + car_em + food_em

        return {
            "electricity": electricity_em,
            "water": water_em,
            "car": car_em,
            "food": food_em,
            "total": total,
            "yearly": total * 12
        } 
    # ---------------- FORM ----------------
    with st.form("sustainability_form"):

        name = st.text_input("Name (required)")
        email = st.text_input("Email (required)")

        electricity = st.number_input("Electricity (kWh)", value=200)
        water = st.number_input("Water usage (m³)", value=3)
        car_km = st.number_input("Car travel (km)", value=0)

        diet = st.selectbox("Diet type", ["Plant-based", "Mixed", "Meat-heavy"])
        submitted = st.form_submit_button("Calculate & Save")
        
    # =========================================================
    # 🚨 EVERYTHING BELOW ONLY RUNS AFTER SUBMIT
    # =========================================================

    if submitted:

        # ---------------- VALIDATION ----------------
        if not name or not email:
            st.error("Name and Email are required!")
            st.stop()

        # ---------------- CALCULATE ----------------
        results = calculate_emissions(electricity, water, car_km, diet)

        # ---------------- OUTPUT ----------------
        st.header("📊 Results")
        st.write(f"Monthly CO₂: **{results['total']:.2f} kg**")
        st.write(f"Yearly CO₂: **{results['yearly']:.2f} kg**")

        df = pd.DataFrame({
            "Category": ["Electricity", "Water", "Transport", "Food"],
            "Emissions": [
                results["electricity"],
                results["water"],
                results["car"],
                results["food"]
            ]
        })

        st.bar_chart(df.set_index("Category"))

        # =========================================================
        # 💾 DATABASE SAVE (SAFE INSIDE SUBMIT BLOCK)
        # =========================================================
        try:
            from database import save_user, email_exists
        except Exception:
            st.error("Database module not properly configured.")
            st.stop()

        user_payload = {
            "name": name,
            "email": email,
            "electricity": electricity,
            "water": water,
            "car_km": car_km,
            "diet": diet,
            "monthly_total": results["total"],
            "yearly_total": results["yearly"]
        }
        
        if email_exists(email):
            st.warning("Email exists → updating record")
        else:
            st.info("New user → inserting record")

        save_user(user_payload)
        st.success("Saved successfully!")
        st.subheader("📊 Stored Emissions Data")
        df = load_emissions()
        
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No records stored yet.")
        # =========================================================
        # 📈 IQR OUTLIER ANALYSIS
        # =========================================================
        st.subheader("📈 Outlier Detection (IQR)")

        try:
            #implement the method
            data = get_all_users()
            df_all = pd.DataFrame(data)

            if len(df_all) >= 4 and "monthly_total" in df_all.columns:

                q1 = df_all["monthly_total"].quantile(0.25)
                q3 = df_all["monthly_total"].quantile(0.75)
                iqr = q3 - q1

                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr

                df_all["outlier"] = (
                    (df_all["monthly_total"] < lower) |
                    (df_all["monthly_total"] > upper)
                )

                st.write(f"IQR range: {lower:.2f} → {upper:.2f}")
                st.dataframe(df_all)

                st.bar_chart(df_all.set_index("email")["monthly_total"])

            else:
                st.info("Not enough data yet for IQR analysis.")

        except Exception as e:
            st.warning("Could not load analytics data yet.")
    return None

def get_all_users():
    try:
        from database import get_all_users
        return get_all_users()
    except Exception as e:
        st.warning(f"Could not load users: {e}")
        return []