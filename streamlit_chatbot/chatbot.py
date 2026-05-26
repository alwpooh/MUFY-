import streamlit as st
import pandas as pd

import streamlit as st

# Initialize session state for active and completed tasks
if "active_todos" not in st.session_state:
    st.session_state.active_todos = ["Buy groceries", "Finish presentation", "Call the bank"]
if "completed_todos" not in st.session_state:
    st.session_state.completed_todos = ["Setup Streamlit app project"]

st.title("📝 Notion-Style To-Do")

# Create "Folders" using Streamlit tabs
tab_active, tab_completed = st.tabs(["📂 Active Tasks", "📁 Completed Archive"])

# --- FOLDER 1: ACTIVE TASKS ---
with tab_active:
    # Inline quick-add text input (Notion style)
    new_todo = st.text_input("", placeholder="+ New task...", key="new_todo_input")
    if new_todo.strip():
        st.session_state.active_todos.append(new_todo.strip())
        st.rerun()

    st.write("")  # Spacing

    if not st.session_state.active_todos:
        st.caption("No active tasks. Type above to add one!")
    else:
        # Render tasks as interactive bullet points
        for idx, todo in enumerate(st.session_state.active_todos):
            col_bullet, col_text = st.columns([0.05, 0.95])
            
            # The bullet point behaves as the "complete" trigger
            if col_bullet.button("○", key=f"todo_{idx}", help="Click to mark as completed"):
                # Move from Active to Completed folder
                task_to_move = st.session_state.active_todos.pop(idx)
                st.session_state.completed_todos.append(task_to_move)
                st.rerun()
            
            # Display the task text next to the bullet
            col_text.markdown(f" {todo}")

# --- FOLDER 2: COMPLETED TASKS ---
with tab_completed:
    if not st.session_state.completed_todos:
        st.caption("No completed tasks yet.")
    else:
        for idx, done_todo in enumerate(st.session_state.completed_todos):
            col_bullet, col_text, col_delete = st.columns([0.05, 0.85, 0.1])
            
            # Filled bullet point to show it is done
            col_bullet.markdown("●")
            # Strikethrough text
            col_text.markdown(f"~~{done_todo}~~")
            
            # Optional: Permanent delete button inside the archive folder
            if col_delete.button("🗑️", key=f"del_{idx}", help="Permanently delete"):
                st.session_state.completed_todos.pop(idx)
                st.rerun()