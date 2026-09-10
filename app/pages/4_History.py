"""
pages/4_History.py — view past scans from MySQL, filter, and export as CSV.

Depends on app.db.crud.get_scan_history(user_id) — built in a later batch
alongside save_scan(). Until then this page loads but shows an error when
it tries to fetch data.
"""

import streamlit as st
import pandas as pd

from app.auth.auth_handler import require_login
from app.components.sidebar import render_sidebar

st.set_page_config(page_title="History — Ikraceya", page_icon="🗂️")

if not require_login():
    st.stop()

render_sidebar()

st.title("Scan History")

try:
    from app.db.crud import get_scan_history

    records = get_scan_history(user_id=st.session_state["user_id"])
except ModuleNotFoundError:
    st.info("History isn't wired up yet — app/db/crud.py comes in a later batch.")
    st.stop()
except Exception as e:
    st.error(f"Could not load history: {e}")
    st.stop()

if not records:
    st.info("No scans yet. Go scan something first.")
    st.stop()

df = pd.DataFrame(records)

# Turn the raw violations list (list of rule-id dicts) into a readable
# summary string for the table — e.g. "DECL-5, MRP-FORMAT" or "None".
def _summarize_violations(violations):
    if not violations:
        return "None"
    return ", ".join(v.get("rule_id", "?") for v in violations)

df["Violations"] = df["violations"].apply(_summarize_violations)
df = df.drop(columns=["violations"])

st.divider()

# --- Filters ---
col1, col2 = st.columns(2)
with col1:
    status_options = ["All"] + sorted(df["overall_status"].dropna().unique().tolist())
    status_filter = st.selectbox("Filter by status", status_options)
with col2:
    persona_options = ["All"] + sorted(df["persona"].dropna().unique().tolist())
    persona_filter = st.selectbox("Filter by persona", persona_options)

filtered_df = df.copy()
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["overall_status"] == status_filter]
if persona_filter != "All":
    filtered_df = filtered_df[filtered_df["persona"] == persona_filter]

# Sr. No. is a simple 1-based row count for easy reference in conversation
# ("row 3") — separate from scan_id, which is the real database key.
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.insert(0, "Sr. No.", range(1, len(filtered_df) + 1))

st.divider()
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.download_button(
    label="Download as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="scan_history.csv",
    mime="text/csv",
)