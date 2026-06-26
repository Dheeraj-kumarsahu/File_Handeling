# 🗂️ CRUD File Handling System (Streamlit)

A simple, clean web UI for basic file CRUD (Create, Read, Update, Delete) operations,
built with Python and Streamlit. Originally a command-line script, converted into an
interactive web app.

## Features
- ➕ **Create** — make a new file with optional starting content
- 📖 **Read** — view the contents of any file in the workspace
- ✏️ **Update** — append, overwrite, or rename files
- 🗑️ **Delete** — password-protected file deletion
- 📁 Live sidebar showing all files and their sizes

## Run locally

```bash
pip install streamlit
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Notes
- All file operations are sandboxed to a local `crud_files/` folder so the demo
  is safe to run anywhere.
- Default delete password: `!@#$%` (change `DELETE_PASSWORD` in `app.py`). 