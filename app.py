"""
CRUD File Handling System — Streamlit UI
Wraps Create / Read / Update / Delete file operations in a clean web interface.
Run with: streamlit run app.py
"""

import os
from pathlib import Path
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WORKDIR = Path("crud_files")   # all file operations are sandboxed to this folder
WORKDIR.mkdir(exist_ok=True)
DELETE_PASSWORD = "!@#$%"

st.set_page_config(
    page_title="CRUD File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Minimal custom styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .crud-card {
        background: #1a1d24;
        border: 1px solid #2a2e37;
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .crud-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    div[data-testid="stMetricValue"] { font-size: 1.4rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_path(filename: str) -> Path:
    """Keep every operation confined to WORKDIR, even if a user types a path."""
    return WORKDIR / Path(filename).name


def list_files():
    return sorted([p.name for p in WORKDIR.iterdir() if p.is_file()])


def file_size_kb(path: Path) -> float:
    return round(path.stat().st_size / 1024, 2)


# ---------------------------------------------------------------------------
# Sidebar — live file explorer
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 📁 Workspace")
    st.caption(f"Files are sandboxed in `./{WORKDIR}/`")

    files = list_files()
    st.metric("Total files", len(files))

    if files:
        for f in files:
            p = safe_path(f)
            st.write(f"📄 `{f}`  —  {file_size_kb(p)} KB")
    else:
        st.info("No files yet. Create one to get started.")

    st.divider()
    st.caption("Built with Python + Streamlit · CRUD demo")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🗂️ CRUD File Handling System")
st.caption("Create, Read, Update, and Delete files — all from a simple web UI.")

tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"]
)

# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------

with tab_create:
    st.markdown('<div class="crud-card">', unsafe_allow_html=True)
    st.markdown('<div class="crud-title">Create a new file</div>', unsafe_allow_html=True)

    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
    initial_content = st.text_area(
        "Initial content (optional)", placeholder="Leave blank for an empty file", key="create_content"
    )

    if st.button("Create File", type="primary", key="create_btn"):
        if not filename.strip():
            st.warning("Please enter a file name.")
        else:
            path = safe_path(filename)
            if path.exists():
                st.error(f"❌ `{filename}` already exists.")
            else:
                try:
                    path.write_text(initial_content or "", encoding="utf-8")
                    st.success(f"✅ `{filename}` created successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error occurred while creating file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------

with tab_read:
    st.markdown('<div class="crud-card">', unsafe_allow_html=True)
    st.markdown('<div class="crud-title">Read a file</div>', unsafe_allow_html=True)

    files = list_files()
    if not files:
        st.info("No files available. Create one first.")
    else:
        selected = st.selectbox("Choose a file to read", files, key="read_select")
        if st.button("Read File", key="read_btn"):
            path = safe_path(selected)
            try:
                content = path.read_text(encoding="utf-8")
                st.text_area("File content", content, height=260, key="read_output")
            except Exception as e:
                st.error(f"Error occurred while reading file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------

with tab_update:
    st.markdown('<div class="crud-card">', unsafe_allow_html=True)
    st.markdown('<div class="crud-title">Update a file</div>', unsafe_allow_html=True)

    files = list_files()
    if not files:
        st.info("No files available. Create one first.")
    else:
        action = st.radio(
            "Choose an action",
            ["Append", "Overwrite", "Rename"],
            horizontal=True,
            key="update_action",
        )

        if action == "Append":
            selected = st.selectbox("File to append to", files, key="append_select")
            new_text = st.text_area("Content to add", key="append_content")
            if st.button("Append", type="primary", key="append_btn"):
                try:
                    path = safe_path(selected)
                    with path.open("a", encoding="utf-8") as f:
                        f.write(new_text)
                    st.success(f"✅ Content appended to `{selected}`.")
                except Exception as e:
                    st.error(f"Error occurred while updating file: {e}")

        elif action == "Overwrite":
            selected = st.selectbox("File to overwrite", files, key="overwrite_select")
            new_text = st.text_area("New content (replaces everything)", key="overwrite_content")
            if st.button("Overwrite", type="primary", key="overwrite_btn"):
                try:
                    path = safe_path(selected)
                    path.write_text(new_text, encoding="utf-8")
                    st.success(f"✅ `{selected}` overwritten successfully.")
                except Exception as e:
                    st.error(f"Error occurred while updating file: {e}")

        elif action == "Rename":
            selected = st.selectbox("File to rename", files, key="rename_select")
            new_name = st.text_input("New file name", key="rename_new_name")
            if st.button("Rename", type="primary", key="rename_btn"):
                if not new_name.strip():
                    st.warning("Please enter a new file name.")
                else:
                    try:
                        old_path = safe_path(selected)
                        new_path = safe_path(new_name)
                        if new_path.exists():
                            st.error(f"❌ A file named `{new_name}` already exists.")
                        else:
                            os.rename(old_path, new_path)
                            st.success(f"✅ Renamed `{selected}` → `{new_name}`.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error occurred while renaming file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

with tab_delete:
    st.markdown('<div class="crud-card">', unsafe_allow_html=True)
    st.markdown('<div class="crud-title">Delete a file</div>', unsafe_allow_html=True)
    st.caption("Protected by a password, just like the original CLI version.")

    files = list_files()
    if not files:
        st.info("No files available.")
    else:
        selected = st.selectbox("File to delete", files, key="delete_select")
        pwd = st.text_input("Password", type="password", key="delete_pwd")

        if st.button("Delete File", type="primary", key="delete_btn"):
            if pwd != DELETE_PASSWORD:
                st.error("❌ Incorrect password. File not deleted.")
            else:
                try:
                    path = safe_path(selected)
                    os.remove(path)
                    st.success(f"✅ `{selected}` deleted successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error occurred while deleting file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
