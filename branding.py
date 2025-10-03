import streamlit as st

INFERA_GRØNN = "#4CAF50"
INFERA_FONT = "Helvetica, sans-serif"

def vis_logo():
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="color:{INFERA_GRØNN}; font-family:{INFERA_FONT};">
                🥗 Slankeapp fra Infera
            </h1>
            <p style="font-size:16px; color:#555;">Din personlige kaloriguide og vektlogg</p>
        </div>
    """, unsafe_allow_html=True)
