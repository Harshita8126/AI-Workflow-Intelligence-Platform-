import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page Configuration
st.set_page_config(
    page_title="Enterprise HR AI Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Helper for API requests with robust fallbacks
@st.cache_data(ttl=10)
def fetch_api(endpoint: str):
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

def post_api(endpoint: str, payload: dict):
    try:
        resp = requests.post(f"{API_BASE_URL}{endpoint}", json=payload, timeout=8)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        return {"error": str(e)}
    return None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Intelligence View:",
    ["📊 Executive Dashboard", "👤 Employee 360° Profile", "🧭 Career Path & Governed Agent", "📚 HR Policy Knowledge (RAG)", "⚙️ Live Attrition Predictor"]
)

# Check API Connectivity
health = fetch_api("/")
if health and health.get("status") == "online":
    st.sidebar.success(f"● Backend Connected ({API_BASE_URL})")
else:
    st.sidebar.warning("⚠️ Connecting to FastAPI Backend...")

# ==============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==============================================================================
if page == "📊 Executive Dashboard":
    st.markdown('<div class="main-title">AI WORKFORCE INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Predictive Attrition, Organizational Skills Heatmap, and Engagement Analytics</div>', unsafe_allow_html=True)
    
    summary = fetch_api("/dashboard/summary")
    if not summary:
        master_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "employee_intelligence_master.csv")
        gaps_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "organization_skill_gaps.csv")
        if os.path.exists(master_path):
            df_m = pd.read_csv(master_path)
            df_g = pd.read_csv(gaps_path)
            summary = {
                "total_employees": len(df_m),
                "high_risk_employees": int((df_m['attrition_risk_level'] == 'HIGH').sum()),
                "medium_risk_employees": int((df_m['attrition_risk_level'] == 'MEDIUM').sum()),
                "low_risk_employees": int((df_m['attrition_risk_level'] == 'LOW').sum()),
                "average_engagement_score": round(float(df_m['engagement_score'].mean()), 2),
                "average_readiness_pct": round(float(df_m['career_readiness_pct'].mean()), 2),
                "major_skill_gaps_count": int((df_g['severity_level'] == 'HIGH').sum())
            }
        else:
            summary = {"total_employees": 0, "high_risk_employees": 0, "average_engagement_score": 0, "major_skill_gaps_count": 0, "average_readiness_pct": 0}

    # Top KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Workforce", f"{summary.get('total_employees', 0):,}")
    col1.caption("Active Employee Records")
    
    col2.metric("High Attrition Risk", f"{summary.get('high_risk_employees', 0):,}", delta="At-Risk", delta_color="inverse")
    col2.caption(f"{summary.get('medium_risk_employees', 0)} medium risk")
    
    col3.metric("Avg Engagement", f"{summary.get('average_engagement_score', 0):.1f}%")
    col3.caption("Morale & Participation")
    
    col4.metric("Avg Career Readiness", f"{summary.get('average_readiness_pct', 0):.1f}%")
    col4.caption("Competency Fulfillment")
    
    col5.metric("Critical Skill Gaps", f"{summary.get('major_skill_gaps_count', 0)}")
    col5.caption("High-Severity Competencies")

    st.markdown("---")

    # Analytics Visualizations
    tab1, tab2, tab3 = st.tabs(["📉 Attrition & Department Risk", "🧩 Organization Skill Heatmap", "📈 Engagement & Performance"])
    
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("Attrition Risk Distribution")
            pie_data = pd.DataFrame({
                "Risk Level": ["High Risk (>=65%)", "Medium Risk (35-64%)", "Low Risk (<35%)"],
                "Employees": [
                    summary.get('high_risk_employees', 0),
                    summary.get('medium_risk_employees', 0),
                    summary.get('low_risk_employees', 0)
                ]
            })
            fig_pie = px.pie(
                pie_data, values="Employees", names="Risk Level",
                color="Risk Level",
                color_discrete_map={"High Risk (>=65%)": "#EF4444", "Medium Risk (35-64%)": "#F59E0B", "Low Risk (<35%)": "#10B981"},
                hole=0.45
            )
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("Attrition Risk by Department")
            dept_attr_data = fetch_api("/dashboard/attrition-by-department")
            if dept_attr_data:
                df_dept_attr = pd.DataFrame(dept_attr_data)
                fig_bar = px.bar(
                    df_dept_attr, x="department", y=["HIGH", "MEDIUM", "LOW"],
                    title="",
                    barmode="group",
                    color_discrete_map={"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#10B981"},
                    labels={"value": "Employees", "variable": "Risk Level"}
                )
                fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
                st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        st.subheader("Critical Organization-Wide Skill Gaps")
        gaps_data = fetch_api("/dashboard/skill-gaps")
        if gaps_data:
            df_gaps = pd.DataFrame(gaps_data)
            
            gc1, gc2 = st.columns([2, 1])
            with gc1:
                fig_gaps = px.bar(
                    df_gaps.head(10), x="employees_missing_count", y="skill_name",
                    orientation="h",
                    color="severity_level",
                    color_discrete_map={"HIGH": "#EF4444", "MEDIUM": "#F59E0B", "LOW": "#10B981"},
                    labels={"employees_missing_count": "Employees Missing Skill", "skill_name": "Competency / Tool"}
                )
                fig_gaps.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=10, b=10, l=10, r=10), height=380)
                st.plotly_chart(fig_gaps, use_container_width=True)
            with gc2:
                st.dataframe(
                    df_gaps[['skill_name', 'employees_missing_count', 'missing_percentage', 'severity_level']],
                    height=380,
                    use_container_width=True
                )

    with tab3:
        st.subheader("Department Engagement & Operational Metrics")
        eng_data = fetch_api("/dashboard/engagement-by-department")
        if eng_data:
            df_eng = pd.DataFrame(eng_data)
            st.dataframe(df_eng, use_container_width=True)
            
            fig_eng = px.bar(
                df_eng, x="department", y=["avg_engagement", "avg_performance", "avg_kpi"],
                barmode="group",
                title="Department Competency Comparison",
                color_discrete_sequence=["#3B82F6", "#8B5CF6", "#10B981"]
            )
            st.plotly_chart(fig_eng, use_container_width=True)

# ==============================================================================
# PAGE 2: EMPLOYEE 360° PROFILE
# ==============================================================================
elif page == "👤 Employee 360° Profile":
    st.markdown('<div class="main-title">Employee 360° Talent Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Inspect individual attrition probabilities, drivers, current competencies, and skill gaps.</div>', unsafe_allow_html=True)
    
    emp_list = fetch_api("/employees?limit=200")
    if emp_list:
        emp_options = {f"Employee #{e['employee_id']} — {e['job_role']} ({e['department']})": e['employee_id'] for e in emp_list}
        selected_label = st.selectbox("Select Employee:", list(emp_options.keys()))
        selected_id = emp_options[selected_label]
        
        emp = fetch_api(f"/employees/{selected_id}")
        if emp:
            pcol1, pcol2, pcol3, pcol4 = st.columns(4)
            pcol1.metric("Employee ID", f"#{emp['employee_id']}")
            pcol2.metric("Department", emp['department'])
            pcol3.metric("Current Role", emp['job_role'])
            pcol4.metric("Monthly Income", f"${emp['monthly_income']:,}")
            
            st.markdown("---")
            
            ec1, ec2 = st.columns(2)
            with ec1:
                st.subheader("Attrition Risk Assessment")
                risk_color = "#DC2626" if emp['attrition_risk_level'] == "HIGH" else "#D97706" if emp['attrition_risk_level'] == "MEDIUM" else "#059669"
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=emp['attrition_probability'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"Risk: {emp['attrition_risk_level']}", 'font': {'color': risk_color, 'size': 20}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': risk_color},
                        'steps': [
                            {'range': [0, 35], 'color': '#DCFCE7'},
                            {'range': [35, 65], 'color': '#FEF3C7'},
                            {'range': [65, 100], 'color': '#FEE2E2'}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 3},
                            'thickness': 0.75,
                            'value': emp['attrition_probability'] * 100
                        }
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            with ec2:
                st.subheader("Competency & Career Readiness")
                st.metric("Career Readiness Score", f"{emp['career_readiness_pct']:.1f}%")
                st.progress(emp['career_readiness_pct'] / 100.0)
                st.write(f"**Competencies Mastered:** {emp['current_skills_count']}")
                st.write(f"**Missing Competencies:** {emp['missing_skills_count']}")
                st.write(f"**Engagement & Morale Index:** {emp['engagement_score']:.1f}%")

            st.markdown("---")
            sc1, sc2 = st.columns(2)
            with sc1:
                st.subheader("Current Mastered Skills")
                if emp['current_skills']:
                    for s in emp['current_skills']:
                        st.markdown(f"- ✅ **{s}**")
                else:
                    st.info("No recorded skills in baseline profile.")
                    
            with sc2:
                st.subheader("Missing Competencies (Skill Gap)")
                if emp['missing_skills']:
                    for s in emp['missing_skills']:
                        st.markdown(f"- ⚠️ **{s}**")
                else:
                    st.success("No missing competencies for current role!")
                    
            st.markdown("---")
            st.subheader("🎯 Recommended Personalized Learning Plan")
            st.info(f"📚 **Assigned Courses:** {emp['recommended_learning_plan']}")

# ==============================================================================
# PAGE 3: CAREER PATH & GOVERNED AGENT
# ==============================================================================
elif page == "🧭 Career Path & Governed Agent":
    st.markdown('<div class="main-title">Governed Workforce Agent & Career Upskilling</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Orchestrate governed agent workflows for promotion pathing, role gap diagnosis, and targeted course roadmaps.</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        target_emp_id = st.number_input("Employee ID:", min_value=1, max_value=2068, value=1)
    with c2:
        target_role = st.selectbox(
            "Target Career / Promotion Role:",
            [
                "Sales Executive", "Research Scientist", "Software Engineer", 
                "Data Analyst", "Cybersecurity Specialist", "Accountant", 
                "Manager", "Marketing Executive", "HR Manager", "Content Strategist"
            ]
        )
    with c3:
        st.write("")
        st.write("")
        run_agent_btn = st.button("🚀 Run Governed Agent Workflow", type="primary", use_container_width=True)

    if run_agent_btn:
        with st.spinner("Agent orchestrator executing governed tool chain..."):
            payload = {
                "employee_id": int(target_emp_id),
                "target_role": target_role,
                "user_goal": f"Analyze career progression path to {target_role}"
            }
            res = post_api("/agent/orchestrate", payload)
            
            if res and "execution_trace" in res:
                st.success(f"Governance Status: {res['governance_status']}")
                
                rc1, rc2, rc3 = st.columns(3)
                rc1.metric("Target Role", res['target_role'])
                rc2.metric("Projected Readiness", f"{res['current_readiness']:.1f}%")
                rc3.metric("Missing Competencies", f"{res['skill_gap_count']}")
                
                st.markdown("---")
                st.subheader("Execution Trace & Tool Governance Boundary")
                for step in res['execution_trace']:
                    with st.expander(f"Step {step['step']}: Tool `{step['tool']}`", expanded=True):
                        st.write(step['output'])
                        
                st.markdown("---")
                st.subheader("🎯 Prioritized Upskilling Curriculum")
                if res['recommended_courses']:
                    for c in res['recommended_courses']:
                        st.markdown(f"📖 **{c}**")
                else:
                    st.success("Target role competency requirements already fulfilled!")
            else:
                st.error("Failed to execute agent workflow. Verify Employee ID exists.")

# ==============================================================================
# PAGE 4: HR POLICY KNOWLEDGE (RAG)
# ==============================================================================
elif page == "📚 HR Policy Knowledge (RAG)":
    st.markdown('<div class="main-title">HR Policy Knowledge Assistant (RAG)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Ask natural language questions grounded strictly in official corporate HR policy documents.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Sample Questions:**
    - *What is the company's parental leave policy for primary caregivers?*
    - *What are the hybrid work guidelines and technology stipend?*
    - *What is the annual tuition reimbursement allowance?*
    - *What are the performance review rating scales and promotion requirements?*
    - *What health, dental, and mental wellness benefits are offered?*
    """)
    
    query = st.text_input("Enter your HR Policy question:", "What is the parental leave duration and pay?")
    ask_btn = st.button("🔍 Retrieve Policy Answer", type="primary")
    
    if ask_btn and query:
        with st.spinner("Retrieving and grounding from corporate policy corpus..."):
            rag_res = post_api("/rag/query", {"query": query, "top_k": 3})
            if rag_res and "answer" in rag_res:
                st.markdown("### Grounded Response")
                st.markdown(rag_res['answer'])
                
                st.markdown("---")
                st.subheader("Retrieved Knowledge Chunks & Citations")
                for src in rag_res.get('retrieved_sources', []):
                    with st.expander(f"📄 Source: {src['source']} (Relevance: {src['score']:.3f})"):
                        st.markdown(src['snippet'])
            else:
                st.error("RAG retrieval failed. Please check backend status.")

# ==============================================================================
# PAGE 5: LIVE ATTRITION PREDICTOR
# ==============================================================================
elif page == "⚙️ Live Attrition Predictor":
    st.markdown('<div class="main-title">Live Attrition Risk Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Input individual employee attributes to evaluate live model predictions with real-time risk classification.</div>', unsafe_allow_html=True)
    
    with st.form("prediction_form"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            age = st.number_input("Age:", 18, 70, 34)
            dept = st.selectbox("Department:", ["Sales", "Research & Development", "Human Resources"])
            role = st.selectbox("Job Role:", ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Manager", "Human Resources"])
            income = st.number_input("Monthly Income ($):", 1000, 20000, 4500)
            overtime = st.selectbox("Overtime:", ["No", "Yes"])
            
        with fc2:
            travel = st.selectbox("Business Travel:", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
            distance = st.slider("Distance From Home (miles):", 1, 30, 8)
            tot_exp = st.number_input("Total Working Years:", 0, 45, 8)
            yrs_company = st.number_input("Years at Company:", 0, 30, 4)
            yrs_role = st.number_input("Years in Current Role:", 0, 20, 2)
            
        with fc3:
            job_sat = st.slider("Job Satisfaction (1-4):", 1, 4, 3)
            env_sat = st.slider("Environment Satisfaction (1-4):", 1, 4, 3)
            wlb = st.slider("Work Life Balance (1-4):", 1, 4, 3)
            promo_gap = st.number_input("Years Since Last Promotion:", 0, 15, 1)
            stock = st.slider("Stock Option Level (0-3):", 0, 3, 1)
            
        submit_btn = st.form_submit_button("⚡ Predict Attrition Risk", type="primary", use_container_width=True)
        
    if submit_btn:
        payload = {
            "age": age,
            "business_travel": travel,
            "daily_rate": 800,
            "department": dept,
            "distance_from_home": distance,
            "education": 3,
            "education_field": "Life Sciences",
            "environment_satisfaction": env_sat,
            "hourly_rate": 65,
            "job_involvement": 3,
            "job_level": 2,
            "job_role": role,
            "job_satisfaction": job_sat,
            "monthly_income": income,
            "monthly_rate": 15000,
            "num_companies_worked": 2,
            "over_time": overtime,
            "percent_salary_hike": 14,
            "performance_rating": 3,
            "relationship_satisfaction": 3,
            "stock_option_level": stock,
            "total_working_years": tot_exp,
            "training_times_last_year": 3,
            "work_life_balance": wlb,
            "years_at_company": yrs_company,
            "years_in_current_role": yrs_role,
            "years_since_last_promotion": promo_gap,
            "years_with_curr_manager": yrs_role
        }
        
        pred_res = post_api("/predict/attrition", payload)
        if pred_res and "attrition_probability" in pred_res:
            st.markdown("---")
            st.subheader("Model Prediction Output")
            p1, p2, p3 = st.columns(3)
            p1.metric("Attrition Probability", f"{pred_res['attrition_probability'] * 100:.2f}%")
            p2.metric("Risk Classification", pred_res['attrition_risk_level'])
            p3.metric("Model Version", pred_res['model_version'])
            
            st.subheader("Top Contributing Risk Factors")
            for f in pred_res.get('top_contributing_factors', []):
                st.write(f"- **{f['factor']}**: {f['impact']}")
        else:
            st.error("Prediction failed. Verify API connection.")
