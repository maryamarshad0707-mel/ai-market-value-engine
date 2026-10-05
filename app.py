import streamlit as st
import requests

st.set_page_config(page_title="Executive Market Value Engine", page_icon="⚡", layout="wide")

st.title("⚡ AI Market Value & Flight Risk Intelligence Engine")
st.caption("Full-Stack Enterprise Portfolio System — Powered by FastAPI, Scikit-Learn, and LLM Microservices")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📋 Candidate Profile")
    age = st.slider("Age", 20, 65, 29)
    years_exp = st.slider("Years of Experience (YoE)", 0, 30, 4)
    current_salary = st.number_input("Current Salary ($)", min_value=30000, max_value=500000, value=95000, step=5000)
    target_role = st.selectbox("Target Specialization", ["AI/ML Engineer", "Senior Software Engineer", "Data Architect", "Engineering Manager"])
    primary_skill = st.text_input("Core Technical Stack", "PyTorch / FastAPI")
    
    submit = st.button("Run Market Intelligence Analysis", use_container_width=True)

API_URL = "http://127.0.0.1:8000/analyze-market-value"
API_KEY = "my-secret-token-123"

with col_right:
    st.subheader("📊 Market Assessment & Strategic Analysis")
    
    if submit:
        headers = {"X-API-Key": API_KEY}
        payload = {
            "age": float(age),
            "years_experience": float(years_exp),
            "current_salary": float(current_salary),
            "target_role": target_role,
            "primary_skill": primary_skill
        }
        
        with st.spinner("Evaluating compensation benchmarks and executing generative AI coach..."):
            try:
                res = requests.post(API_URL, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    
                    # Top Metrics Row
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Market Valuation", f"${data['market_valuation']:,.2f}")
                    m2.metric("Market Delta", f"${data['compensation_delta']:,.2f}", delta_color="normal")
                    m3.metric("Flight Risk Warning", data['flight_risk_assessment'])
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Executive AI Career Strategy")
                    st.info(data['executive_ai_strategy'])
                else:
                    st.error(f"Error {res.status_code}: Authorization or request issue.")
            except Exception as e:
                st.error(f"Could not reach FastAPI server: {e}")
    else:
        st.write("👈 Configure candidate metrics on the left panel and click **Run Market Intelligence Analysis**.")