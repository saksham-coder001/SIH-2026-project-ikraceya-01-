"""
pages/2_Scan.py — capture or upload a label image, then run the pipeline.

Depends on app.pipeline.pipeline_runner.run_pipeline(image).
Persona defaults to "consumer" if not explicitly set — no forced detour
through Persona Selection; users can switch anytime from the sidebar.
"""

import streamlit as st
from PIL import Image

from app.auth.auth_handler import require_login
from app.components.sidebar import render_sidebar

st.set_page_config(page_title="Scan — Ikraceya", page_icon="📷")

if not require_login():
    st.stop()

# Default to consumer instead of forcing a detour through persona selection.
st.session_state.setdefault("persona", "consumer")

render_sidebar()

st.title("Scan a Product Label")
st.caption(
    f"Scanning as: **{st.session_state['persona']}** "
    "— switch anytime from the sidebar."
)

tab_upload, tab_camera = st.tabs(["📁 Upload Image", "📷 Use Camera"])

captured_image = None

with tab_upload:
    uploaded_file = st.file_uploader("Upload a label photo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        captured_image = Image.open(uploaded_file)
        st.image(captured_image, caption="Uploaded image", use_column_width=True)

with tab_camera:
    camera_file = st.camera_input("Take a photo of the label")
    if camera_file is not None:
        captured_image = Image.open(camera_file)
        st.image(captured_image, caption="Captured image", use_column_width=True)

st.divider()

if captured_image is not None:
    if st.button("Run Scan", type="primary", use_container_width=True):
        with st.spinner("Reading label and checking compliance..."):
            try:
                # Deferred import — only needed once you actually run a scan,
                # and avoids crashing this whole page before pipeline exists.
                from app.pipeline.pipeline_runner import run_pipeline

                result = run_pipeline(captured_image)
                st.session_state["scan_image"] = captured_image
                st.session_state["scan_result"] = result
                st.switch_page("pages/3_Results.py")
            except ModuleNotFoundError as e:
                st.error(
                    f"Import failed: **{e}**\n\n"
                    "Check that every folder under app/ (pipeline, rules, utils) "
                    "has an empty `__init__.py` file, and that all packages in "
                    "requirements.txt installed without errors."
                )
            except Exception as e:
                st.error(f"Something went wrong while scanning: {e}")
else:
    st.info("Upload or capture an image to enable scanning.")