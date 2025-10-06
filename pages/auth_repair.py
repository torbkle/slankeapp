import streamlit as st
from supabase_admin import supabase as admin
from supabase_klient import supabase
from bekreft_epost import bekreft_epost
import datetime

st.set_page_config(page_title="Auth Repair", layout="centered")
st.title("🛠️ Supabase Auth Repair")

email = st.text_input("E-post").strip()
password = st.text_input("Nytt passord", type="password")

if st.button("Slett og registrer på nytt"):
    try:
        # 🔍 Finn bruker i Supabase Auth
        users = admin.auth.admin.list_users().users
        target_user = next((u for u in users if u.email == email), None)

        if target_user:
            uid = target_user.id
            st.warning(f"⚠️ Bruker finnes – sletter `{email}` med UID `{uid}`")
            admin.auth.admin.delete_user(uid)
            st.success("✅ Bruker slettet fra Supabase Auth.")
        else:
            st.info("ℹ️ Bruker finnes ikke – går rett til registrering.")

        # 🔐 Registrer på nytt
        signup_response = supabase.auth.sign_up({"email": email, "password": password})
        user = signup_response.user

        if not user:
            st.error("🚫 Registrering feilet – ingen bruker returnert.")
            st.stop()

        uid = user.id
        st.success(f"✅ Registrert! auth.uid(): `{uid}`")

        # 📬 Bekreft e-post via Admin API
        bekreft_response = bekreft_epost(uid)
        if bekreft_response.status_code == 200:
            st.info("📬 E-post bekreftet via Admin API.")
        else:
            st.warning("⚠️ Klarte ikke bekrefte e-post.")
            st.code(bekreft_response.text)

        # 🔁 Tving ny innlogging
        supabase.auth.sign_out()
        login_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = login_response.user

        if not user:
            st.error("🚫 Innlogging feilet – ingen bruker returnert.")
            st.stop()

        st.success(f"✅ Innlogget som `{user.email}`")

        # 🧪 Testinnsetting i `brukere`
        st.subheader("📥 Tester innsetting i `brukere`")
        test_data = {
            "id": user.id,
            "email": user.email,
            "fornavn": "Test",
            "etternavn": "Bruker",
            "alder": 42,
            "rolle": "bruker",
            "opprettet": datetime.datetime.utcnow().isoformat()
        }

        response = supabase.table("brukere").insert(test_data).execute()

        if response.status_code == 201:
            st.success("✅ Innsetting OK – RLS-policyen godtar deg.")
            st.json(test_data)
        else:
            st.error("🚫 Innsetting feilet – RLS blokkerer.")
            st.code(response.json())

    except Exception as e:
        st.error("🚫 Feil under Auth-reparasjon.")
        st.code(str(e))

st.markdown("📋 [Se registreringslogg](./registreringslogg)")
