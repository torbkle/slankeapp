import streamlit as st

def vis_logo():
    st.image(
        "https://raw.githubusercontent.com/torbkle/slankeapp/main/assets/infera_logo.png",
        width=180
    )

def vis_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 14px;'>"
        "Slankeapp er utviklet av <strong>Infera</strong> – et norsk prosjekt for smartere helse og teknologi."
        "</div>",
        unsafe_allow_html=True
    )
