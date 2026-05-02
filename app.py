import streamlit as st
import pandas as pd
import joblib
from risk_probability import calculate_risk

# Load models
tumor_model = joblib.load("tumor_model.pkl")
tumor_features = joblib.load("tumor_features.pkl")

risk_model = joblib.load("risk_model.pkl")
risk_features = joblib.load("risk_features.pkl")

# Page config
st.set_page_config(page_title="Medical AI System", layout="wide")

st.title("🧠 Medical Risk Intelligence System")
st.write("AI-powered multi-disease prediction dashboard")

st.markdown("---")

# =========================
# MODE SELECTION
# =========================
mode = st.selectbox(
    "Select Analysis Type",
    ["Tumor Diagnosis", "Health Risk Score", "Risk Probability"]
)

st.markdown("---")

# =========================
# 🧬 TUMOR DIAGNOSIS
# =========================
if mode == "Tumor Diagnosis":

    st.subheader("🧬 Tumor Diagnosis (Cancer Prediction)")

    inputs = []

    st.write("Enter patient parameters:")

    # use only first 10 features for UI simplicity
    for feature in tumor_features[:10]:
        val = st.slider(feature, 0.0, 30.0, 1.0)
        inputs.append(val)

    if st.button("Predict Tumor Risk"):

        df = pd.DataFrame([inputs], columns=tumor_features[:10])

        prediction = tumor_model.predict(df)
        prob = tumor_model.predict_proba(df)[0]

        if prediction[0] == 1:
            st.success("✅ Benign (Low Risk)")
        else:
            st.error("⚠ Malignant (High Risk)")

        st.write("Prediction Confidence:")
        st.write(prob)

        st.progress(int(prob[1] * 100))


# =========================
# ❤️ HEALTH RISK SCORE
# =========================
elif mode == "Health Risk Score":

    st.subheader("❤️ Health Risk Score Analysis")

    age = st.slider("Age", 18, 80, 30)
    bmi = st.slider("BMI", 15.0, 40.0, 22.0)
    smoking = st.selectbox("Smoking", ["No", "Yes"])
    activity = st.selectbox("Activity Level", ["Low", "Medium", "High"])
    diet = st.slider("Diet Score", 1, 10, 5)

    smoking_val = 1 if smoking == "Yes" else 0
    activity_val = {"Low": 1, "Medium": 2, "High": 3}[activity]

    if st.button("Analyze Health Risk"):

        df = pd.DataFrame([[
            age, bmi, smoking_val, activity_val, diet
        ]], columns=risk_features)

        prediction = risk_model.predict(df)
        prob = risk_model.predict_proba(df)[0]

        risk_score = prob[1] * 100

        if prediction[0] == 1:
            st.error("⚠ High Health Risk")
        else:
            st.success("✅ Low Health Risk")

        st.write(f"Risk Confidence: {risk_score:.2f}%")
        st.progress(int(risk_score))


# =========================
# 📊 RISK PROBABILITY
# =========================
elif mode == "Risk Probability":

    st.subheader("📊 Risk Probability Estimator")

    age = st.slider("Age", 18, 80, 30)
    bmi = st.slider("BMI", 15.0, 40.0, 22.0)
    smoking = st.selectbox("Smoking", ["No", "Yes"])
    activity = st.selectbox("Activity Level", ["Low", "Medium", "High"])
    diet = st.slider("Diet Score", 1, 10, 5)

    if st.button("Calculate Risk Probability"):

        risk_percent = calculate_risk(
            age,
            bmi,
            smoking == "Yes",
            activity,
            diet
        )

        if risk_percent > 70:
            st.error("⚠ High Risk")
        elif risk_percent > 40:
            st.warning("⚠ Moderate Risk")
        else:
            st.success("✅ Low Risk")

        st.write(f"Risk Score: {risk_percent}%")
        st.progress(risk_percent)