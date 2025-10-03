import streamlit as st

# 🎨 Farger og typografi
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#f9f9f9"
TEXT_COLOR = "#333"
FONT_FAMILY = "Arial, sans-serif"

def css():
    st.markdown(f"""
        <style>
        html, body, [class*="css"] {{
            font-family: {FONT_FAMILY};
            color: {TEXT_COLOR};
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        </style>
    """, unsafe_allow_html=True)

def ramme(tittel, innhold):
    st.markdown(f"""
        <div style="border:2px solid {PRIMARY_COLOR}; padding:20px; border-radius:10px; background-color:{SECONDARY_COLOR}">
        <h4 style="color:{PRIMARY_COLOR}">{tittel}</h4>
        <p>{innhold}</p>
        </div>
    """, unsafe_allow_html=True)

def seksjon(tittel):
    st.markdown(f"<h3 style='color:{PRIMARY_COLOR}'>{tittel}</h3>", unsafe_allow_html=True)

def ikonlinje(tekst, emoji="✅"):
    st.markdown(f"<p style='font-size:16px'>{emoji} {tekst}</p>", unsafe_allow_html=True)
