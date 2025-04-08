import streamlit as st
import urllib.parse

# --- Page Setup ---
st.set_page_config(page_title="📄 ORGANIZER KINERJA OPSIS UP2B SISTEM MAKASSAR", layout="wide")

# --- Simple Password Protection ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Masukkan Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Masukkan Password:", type="password", on_change=password_entered, key="password")
        st.error("Password salah")
        return False
    else:
        return True

if check_password():
    st.title("📄 ORGANIZER KINERJA OPSIS UP2B SISTEM MAKASSAR")

    # --- Dark Mode Toggle ---
    dark_mode = st.toggle("🌙 Enable Dark Mode", value=True)

    # --- Styling ---
    if dark_mode:
        st.markdown("""
            <style>
            body, .stApp { background-color: #0e1117; color: #ffffff; }
            .stTextInput > div > input { color: white; background-color: #1e222d; }
            iframe { filter: invert(1) hue-rotate(180deg); }
            a.button-link > button {
                background-color: #444; color: white; border: 1px solid white;
                padding: 0.4rem 1rem; margin-bottom: 0.5rem;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            a.button-link > button {
                background-color: #f0f0f0; color: black; border: 1px solid #ccc;
                padding: 0.4rem 1rem; margin-bottom: 0.5rem;
            }
            </style>
        """, unsafe_allow_html=True)

    # --- Preset Spreadsheet Link ---
    preset_url = "https://docs.google.com/spreadsheets/d/1NNsIJ7cXVwOh02WVo-O7UqLnWoveAFYKcvXXNh_uIFk/edit?usp=sharing"
    st.markdown("#### 🔗 LINK SPREADSHEET KINERJA")
    st.code(preset_url, language='markdown')
    copy_button = st.button("📋 Salin & Tempel Link ke Kolom Input")

    if copy_button:
        st.session_state['sheet_url'] = preset_url
        st.toast("✅ Link berhasil disalin ke input!")

    st.markdown(f"""
        <script>
            const btn = window.parent.document.querySelector('button[title="📋 Salin & Tempel Link ke Kolom Input"]');
            if (btn) {{
                btn.onclick = () => {{
                    navigator.clipboard.writeText("{preset_url}");
                }};
            }}
        </script>
    """, unsafe_allow_html=True)

    # --- Input Spreadsheet URL ---
    sheet_url = st.text_input("🔗 Paste your **public Google Sheets URL**:", value=st.session_state.get('sheet_url', ''))

    # --- Sheet List and Mapping ---
    sheet_gid_map = {
        "DASHBOARD 2025": "1985013477",
        "KINERJA 2025": "1713998840",
        "Data Dashboard 2025": "928968380",
        "DASHBOARD 2024": "593461904",
        "KINERJA 2024": "706409339",
    }
    sheet_names = list(sheet_gid_map.keys())

    # --- Search ---
    search_query = st.text_input("🔍 Search tabs")
    filtered_sheets = [name for name in sheet_names if search_query.lower() in name.lower()]

    # --- Embed View ---
    if sheet_url:
        try:
            sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        except IndexError:
            st.error("🚫 Invalid Google Sheets URL format.")
        else:
            st.markdown("### 📁 Select Sheet to Preview")
            for sheet_name in filtered_sheets:
                gid = sheet_gid_map.get(sheet_name, "0")
                embed_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/preview#gid={gid}"
                open_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={gid}"

                with st.expander(f"📄 {sheet_name}", expanded=False):
                    st.markdown(f"""
                        <a href="{open_url}" target="_blank" class="button-link">
                            <button>🔗 Open in New Tab</button>
                        </a>
                        <iframe src="{embed_url}" width="100%" height="600" style="border:none;"></iframe>
                    """, unsafe_allow_html=True)
    else:
        st.info("Paste your public Google Sheets link to begin.")
