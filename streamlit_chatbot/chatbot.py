import streamlit as st
import pandas as pd
import hashlib
from datetime import date
import json
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Daily Planner", page_icon="📆", layout="centered")

# --- DATA PERSISTENCE SETUP ---
DATA_FILE = "todo_data.json"

def load_data():
    """Loads tasks and settings from the JSON file if it exists."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data():
    """Saves the current session state to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(st.session_state.todo_data, file, indent=4)

def generate_stable_id(text):
    """Generates a stable, short string ID for widget keys."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:8]

# Initialize data structure
if "todo_data" not in st.session_state:
    st.session_state.todo_data = load_data()

# Ensure a default settings key exists for personalization
if "settings" not in st.session_state.todo_data:
    st.session_state.todo_data["settings"] = {
        "theme": "Sea View",  
        "font": "Modern Sans (Inter)",
        "custom_text": "#0F2D4A" # Default fallback text color
    }

# --- CONFIGURATION MAPS FOR THEMES & FONTS ---
THEMES = {
    "Light Brown": {
        "type": "color",
        "value": "#D2B48C",
        "text": "#4A3525"
    },
    "Sea View": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?auto=format&fit=crop&w=1200&q=80",
        "text": "#0F2D4A"
    },
    "Mountains": {
        "type": "image", 
        "value": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80", 
        "text": "#1A2E1A"
    },
    "City View": {
        "type": "image", 
        # Verified working direct CDN link for a bright concrete city layout
        "value": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=1200&q=80", 
        # Dark charcoal text so it's readable over the white/grey concrete buildings
        "text": "#1A1A24"
    }
}

FONTS = {
    "Default Sans": "sans-serif",
    "Modern Sans (Inter)": "'Inter', sans-serif",
    "Elegant Serif (Lora)": "'Lora', serif",
    "Minimal Code (Roboto Mono)": "'Roboto Mono', monospace"
}

# --- CALLBACK FOR LIVE VISUAL UPDATES ---
def update_settings_callback():
    """Maintains and writes the appearance configurations to the file."""
    st.session_state.todo_data["settings"] = {
        "theme": st.session_state.sb_theme,
        "font": st.session_state.sb_font,
        "custom_text": st.session_state.get("sb_custom_text", "#0F2D4A") # Saves custom text choice
    }
    save_data()

# --- SIDEBAR PERSONALIZATION CONTROLS ---
st.sidebar.title("🎨 Personalize App")
saved_settings = st.session_state.todo_data["settings"]

# Safe Font Loading
saved_font = saved_settings.get("font", "Modern Sans (Inter)")
if saved_font not in FONTS:
    saved_font = "Modern Sans (Inter)"
font_index = list(FONTS.keys()).index(saved_font)

selected_font = st.sidebar.selectbox(
    "Font Style", 
    list(FONTS.keys()), 
    index=font_index,
    key="sb_font",
    on_change=update_settings_callback
)

# Safe Theme Loading
saved_theme = saved_settings.get("theme", "Sea View")
if saved_theme not in THEMES:
    saved_theme = "Sea View"
theme_index = list(THEMES.keys()).index(saved_theme)

selected_theme = st.sidebar.selectbox(
    "Theme Preset", 
    list(THEMES.keys()), 
    index=theme_index,
    key="sb_theme",
    on_change=update_settings_callback
)

# Parse theme background styling configuration
theme_config = THEMES[selected_theme]
if theme_config["type"] == "image":
    bg_style = f"background-image: url('{theme_config['value']}') !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;"
else:
    bg_style = f"background-color: {theme_config['value']} !important;"

# DYNAMIC TEXT COLOR PICKER 
default_text_color = saved_settings.get("custom_text", theme_config["text"])
text_color = st.sidebar.color_picker("Text Color Override", default_text_color, key="sb_custom_text", on_change=update_settings_callback)

font_family = FONTS[selected_font]

# --- INJECT DYNAMIC CUSTOM CSS ---
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Lora:wght@400;600&family=Roboto+Mono&display=swap');

/* Apply background style safely across standard Streamlit target layout blocks */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    {bg_style}
}}

/* Light frosting effect on the sidebar layout to keep controls visible over background images */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.4) !important;
    backdrop-filter: blur(10px);
}}

/* Apply global font style and structural text color overrides */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stTabs [data-baseweb="tab"] p, .stCaption {{
    font-family: {font_family} !important;
    color: {text_color} !important;
}}

/* Remove sidebar arrow background wrapper */
[data-testid="stSidebarCollapseButton"] button {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Dynamic color assignment for the sidebar toggle arrow */
[data-testid="stSidebarCollapseButton"] svg {{
    fill: {text_color} !important;
    color: {text_color} !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- MAIN APPLICATION LOGIC ---
st.title("📆 Daily Notion-Style Planner")

# Calendar Picker
selected_date = st.date_input("Select a Date", date.today())
date_key = str(selected_date)

if date_key not in st.session_state.todo_data:
    st.session_state.todo_data[date_key] = {"active": [], "completed": []}

day_tasks = st.session_state.todo_data[date_key]

# --- CALLBACK TO ADD TASK & SAVE ---
def add_task_callback():
    widget_key = f"temp_input_{date_key}"
    text_entered = st.session_state[widget_key].strip()
    
    if text_entered:
        st.session_state.todo_data[date_key]["active"].append(text_entered)
        save_data()  
    
    # Safely clear text input state without crashing the lifecycle
    st.session_state[widget_key] = ""


st.write("---")
st.subheader(f"Tasks for {selected_date.strftime('%B %d, %Y')}")

tab_active, tab_completed = st.tabs(["📂 Active Tasks", "📁 Completed Archive"])

# --- FOLDER 1: ACTIVE TASKS ---
with tab_active:
    st.text_input(
        "", 
        placeholder="+ New task for this day...", 
        key=f"temp_input_{date_key}",
        on_change=add_task_callback
    )

    st.write("") 

    if not day_tasks["active"]:
        st.caption("No active tasks for this day.")
    else:
        to_complete = None
        
        for idx, todo in enumerate(day_tasks["active"]):
            col_bullet, col_text = st.columns([0.08, 0.92])

            stable_id = generate_stable_id(todo)
            if col_bullet.button("○", key=f"btn_act_{date_key}_{idx}_{stable_id}"):
                to_complete = idx

            col_text.markdown(f" {todo}")
        
        if to_complete is not None:
            task_to_move = day_tasks["active"].pop(to_complete)
            day_tasks["completed"].append(task_to_move)
            save_data()  
            st.rerun()

# --- FOLDER 2: COMPLETED TASKS ---
with tab_completed:
    if not day_tasks["completed"]:
        st.caption("No completed tasks recorded for this day.")
    else:
        to_delete = None
        
        for idx, done_todo in enumerate(day_tasks["completed"]):
            col_bullet, col_text, col_delete = st.columns([0.08, 0.82, 0.1])

            col_bullet.markdown("●") 
            col_text.markdown(f"~~{done_todo}~~")

            stable_id = generate_stable_id(done_todo)
            if col_delete.button("🗑️", key=f"btn_del_{date_key}_{idx}_{stable_id}"):
                to_delete = idx

        if to_delete is not None:
            day_tasks["completed"].pop(to_delete)
            save_data()  
            st.rerun()