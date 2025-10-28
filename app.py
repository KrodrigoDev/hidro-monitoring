import streamlit as st

st.write("Session State:", st.session_state)

if st.session_state.get('authentication_status'):
    st.switch_page("../hidro-monitoring/pages/1_dashboard.py")
else:
    st.switch_page("pages/login.py")
