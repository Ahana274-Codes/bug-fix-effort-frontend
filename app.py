
import streamlit as st
import requests
from datetime import date

st.set_page_config(
    page_title="Bug Fix Effort Predictor",
    page_icon="🐞",
    layout="wide"
)

st.title("🐞 AI-Powered Bug Fix Effort Predictor")
st.write(
    "Estimate software bug resolution time and identify potential risk "
    "using a trained Machine Learning model."
)

st.info("Enter bug-report details below to generate a prediction.")

with st.form("bug_form"):
    st.subheader("Bug Report Details")

    col1, col2 = st.columns(2)

    with col1:
        project = st.selectbox(
            "Project",
            ["Mozilla", "Novell", "OpenXchange", "W3C"]
        )
        classification = st.text_input("Classification", "Other")
        product = st.text_input("Product", "Other")
        component = st.text_input("Component", "Other")
        version = st.text_input("Version", "Other")
        priority = st.selectbox(
            "Priority", ["P1", "P2", "P3", "P4", "P5"]
        )
        severity = st.selectbox(
            "Bug Severity",
            ["blocker", "critical", "major", "normal", "minor", "trivial", "enhancement"]
        )
        platform = st.text_input("Reported Platform", "Other")
        operating_system = st.text_input("Operating System", "Other")
        reporter = st.text_input("Reporter", "unknown")
        mentor = st.text_input("Mentor", "unknown")

    with col2:
        created = st.date_input("Bug Creation Date", value=date(2024, 6, 15))
        reporter_accessible = st.selectbox("Reporter Accessible", [1, 0])
        cclist_accessible = st.selectbox("CC List Accessible", [1, 0])
        everconfirmed = st.selectbox("Ever Confirmed", [1, 0])
        restrict_comments = st.selectbox("Comments Restricted", [0, 1])
        comment_sort_order = st.text_input(
            "Comment Sort Order", "oldest_to_newest"
        )

    submitted = st.form_submit_button(
        "Predict Fix Effort",
        type="primary",
        use_container_width=True
    )

if submitted:
    payload = {
        "reporter_accessible": reporter_accessible,
        "cclist_accessible": cclist_accessible,
        "everconfirmed": everconfirmed,
        "restrict_comments": restrict_comments,
        "creation_year": created.year,
        "creation_month": created.month,
        "creation_day": created.day,
        "creation_dayofweek": created.weekday(),
        "creation_quarter": (created.month - 1) // 3 + 1,
        "classification": classification,
        "product": product,
        "component": component,
        "version": version,
        "rep_platform": platform,
        "op_sys": operating_system,
        "priority": priority,
        "bug_severity": severity,
        "reporter": reporter,
        "comment_sort_order": comment_sort_order,
        "project": project,
        "mentor": mentor
    }

    try:
        with st.spinner("Analyzing bug report..."):
            response = requests.post(
                "https://bug-fix-effort-predictor-api.onrender.com",
                json=payload,
                timeout=30
            )

        if response.ok:
            result = response.json()
            st.subheader("Prediction Results")

            a, b = st.columns(2)
            a.metric(
                "Estimated Resolution Time",
                f"{result['predicted_resolution_days']} days"
            )
            b.metric("Risk Category", result["risk_category"])

            st.markdown("### Recommended Action")
            st.write(result["recommended_action"])
            st.caption(result["note"])
        else:
            st.error(f"API error ({response.status_code}): {response.text}")

    except requests.RequestException as exc:
        st.error(
            "Could not connect to the backend. Make sure the FastAPI "
            "server is running on port 8000."
        )
        st.code(str(exc))

st.divider()
st.caption("Academic project prototype • Random Forest Regression • FastAPI + Streamlit")
