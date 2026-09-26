import streamlit as st

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 AgriDSS AI")

st.subheader("AI-Powered Agricultural Decision Support System")

st.write(
    "This is the new AgriDSS AI application."
)

st.success("NEW APP IS RUNNING")

st.info(
    "If you can see this message normally, the HTML rendering problem is bypassed."
)

st.metric(
    label="System Status",
    value="Online"
)
