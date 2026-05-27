import streamlit as st
import streamlit.components.v1 as components
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
        "custom_text": "#0F2D4A",
        "animal": "🦊 Fox"        
    }




# --- CONFIGURATION MAPS FOR THEMES, FONTS & ANIMALS ---
THEMES = {
    "Default": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1764072566129-f3aa9ff43c36?auto=format&fit=crop&w=2400&q=1600",
        "text": "#4A3525"
    },
    "Sea View": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1610532693607-61c8d3b8fded?auto=format&fit=crop&w=2400&q=1600",
        "text": "#0F2D4A"
    },
    "Mountains": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1546587348-d12660c30c50?auto=format&fit=crop&w=2400&q=1600",
        "text": "#1A2E1A"
    },
    "City View": {
        "type": "image",
        "value": "https://images.unsplash.com/photo-1506606401543-2e73709cebb4?auto=format&fit=crop&w=2400&q=1600",
        "text": "#1A1A24"
    }
}




FONTS = {
    "Default Sans": "sans-serif",
    "Modern Sans (Inter)": "'Inter', sans-serif",
    "Elegant Serif (Lora)": "'Lora', serif",
    "Minimal Code (Roboto Mono)": "'Roboto Mono', monospace"
}




ANIMALS = {
    "None": None,
    "🦊 Fox": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f98a.svg",
    "🐼 Panda": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f43c.svg",
    "🐱 Cat": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f431.svg",
    "🐸 Frog": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f438.svg",
    "🐰 Bunny": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f430.svg",
    "🦁 Lion": "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/svg/emoji_u1f981.svg"
}




ANIMAL_CLASSES = {
    "🦊 Fox": "anim-fox",
    "🐼 Panda": "anim-panda",
    "🐱 Cat": "anim-cat",
    "🐸 Frog": "anim-frog",
    "🐰 Bunny": "anim-bunny",
    "🦁 Lion": "anim-lion"
}




def update_settings_callback():
    """Maintains and writes the appearance configurations to the file."""
    st.session_state.todo_data["settings"] = {
        "theme": st.session_state.sb_theme,
        "font": st.session_state.sb_font,
        "custom_text": st.session_state.get("sb_custom_text", "#0F2D4A"),
        "animal": st.session_state.get("sb_animal", "🦊 Fox")
    }
    save_data()




# --- SIDEBAR PERSONALIZATION CONTROLS ---
st.sidebar.title("🎨 Personalize App")
saved_settings = st.session_state.todo_data["settings"]




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




theme_config = THEMES[selected_theme]
if theme_config["type"] == "image":
    bg_style = f"background-image: url('{theme_config['value']}') !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;"
else:
    bg_style = f"background-color: {theme_config['value']} !important;"




default_text_color = saved_settings.get("custom_text", theme_config["text"])
text_color = st.sidebar.color_picker("Text Color Override", default_text_color, key="sb_custom_text", on_change=update_settings_callback)




st.sidebar.write("---")
st.sidebar.subheader("🐾 Sidebar Companion")




saved_animal = saved_settings.get("animal", "🦊 Fox")
if saved_animal not in ANIMALS:
    saved_animal = "🦊 Fox"
animal_index = list(ANIMALS.keys()).index(saved_animal)




selected_animal = st.sidebar.selectbox(
    "Choose a companion",
    list(ANIMALS.keys()),
    index=animal_index,
    key="sb_animal",
    on_change=update_settings_callback
)




if selected_animal != "None" and ANIMALS[selected_animal]:
    st.sidebar.write("")
    anim_class = ANIMAL_CLASSES.get(selected_animal, "animated-companion")
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <img src="{ANIMALS[selected_animal]}" class="{anim_class}" width="95">
        </div>
        """,
        unsafe_allow_html=True
    )




font_family = FONTS[selected_font]




# --- INJECT DYNAMIC CUSTOM CSS ---
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Lora:wght@400;600&family=Roboto+Mono&display=swap');




[data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    {bg_style}
}}




[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.4) !important;
    backdrop-filter: blur(10px);
}}




h1, h2, h3, h4, h5, h6, p, label, li, .stMarkdown, .stTabs [data-baseweb="tab"] p, .stCaption {{
    font-family: {font_family} !important;
    color: {text_color} !important;
}}




p, label, li, .stMarkdown p, .stTabs [data-baseweb="tab"] p, .stCaption {{
    font-size: 18px !important;
}}




[data-testid="stSidebarCollapseButton"] button {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}




[data-testid="stSidebarCollapseButton"] svg {{
    fill: {text_color} !important;
    color: {text_color} !important;
}}




/* --- CHARACTER ANIMATIONS --- */
@keyframes foxTilt {{ 0%, 100% {{ transform: rotate(0deg); }} 15% {{ transform: rotate(-10deg); }} 30% {{ transform: rotate(10deg); }} 45% {{ transform: rotate(0deg); }} }}
.anim-fox {{ animation: foxTilt 4s ease-in-out infinite; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}




@keyframes pandaSway {{ 0%, 100% {{ transform: translate(0, 0) rotate(0deg); }} 50% {{ transform: translate(2px, 2px) rotate(3deg) scaleY(0.95); }} }}
.anim-panda {{ animation: pandaSway 5s ease-in-out infinite; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}




@keyframes catWiggle {{ 0%, 70%, 100% {{ transform: translate(0, 0) scale(1); }} 73% {{ transform: translate(-2px, 0) rotate(-3deg); }} 76% {{ transform: translate(2px, 0) rotate(3deg); }} 79% {{ transform: translate(-2px, 0) rotate(-3deg); }} 85% {{ transform: translateY(-12px) scaleY(1.05); }} }}
.anim-cat {{ animation: catWiggle 4.5s ease-in-out infinite; transform-origin: bottom center; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}




@keyframes frogHop {{ 0%, 60%, 100% {{ transform: translateY(0) scale(1); }} 65% {{ transform: scaleY(0.75) scaleX(1.1); }} 70% {{ transform: translateY(-25px) scaleY(1.1) scaleX(0.9); }} 75% {{ transform: translateY(0) scaleY(0.85) scaleX(1.05); }} }}
.anim-frog {{ animation: frogHop 3.5s ease-in-out infinite; transform-origin: bottom center; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}




@keyframes bunnyHop {{ 0%, 40%, 70%, 100% {{ transform: translateY(0); }} 10%, 30% {{ transform: translateY(-1px) scaleY(1.02); }} 20% {{ transform: translateY(1px); }} 45% {{ transform: scaleY(0.8); }} 52% {{ transform: translateY(-18px) rotate(5deg); }} 60% {{ transform: translateY(0) scaleY(0.9); }} }}
.anim-bunny {{ animation: bunnyHop 4s ease-in-out infinite; transform-origin: bottom center; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}




@keyframes lionRoar {{ 0%, 70%, 100% {{ transform: scale(1) rotate(0); }} 75% {{ transform: scale(1.1) rotate(-2deg); }} 80%, 88% {{ transform: scale(1.15) translate(1px, -1px) rotate(2deg); }} 82%, 90% {{ transform: scale(1.15) translate(-1px, 1px) rotate(-2deg); }} 84% {{ transform: scale(1.15) translate(1px, 1px) rotate(1deg); }} 95% {{ transform: scale(1) rotate(0); }} }}
.anim-lion {{ animation: lionRoar 5s ease-in-out infinite; transform-origin: bottom center; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15)); }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)












# --- MAIN APPLICATION LOGIC ---
st.title("📆 Daily Notion-Style Planner")




# --- SECTION 1: TO-DO LIST AND DAY PLANNER ---
selected_date = st.date_input("Select a Date", date.today())
date_key = str(selected_date)




if date_key not in st.session_state.todo_data:
    st.session_state.todo_data[date_key] = {"active": [], "completed": []}




day_tasks = st.session_state.todo_data[date_key]




# Callback to add task and save
def add_task_callback():
    widget_key = f"temp_input_{date_key}"
    text_entered = st.session_state[widget_key].strip()
   
    if text_entered:
        st.session_state.todo_data[date_key]["active"].append(text_entered)
        save_data()  
   
    st.session_state[widget_key] = ""




st.subheader(f"Tasks for {selected_date.strftime('%B %d, %Y')}")




# --- PROGRESS BAR CALCULATIONS ---
num_active = len(day_tasks["active"])
num_completed = len(day_tasks["completed"])
total_tasks = num_active + num_completed




if total_tasks > 0:
    progress_percentage = int((num_completed / total_tasks) * 100)
    st.progress(num_completed / total_tasks)
    st.caption(f"📊 Progress: **{progress_percentage}%** ({num_completed}/{total_tasks} tasks done)")
else:
    st.progress(0.0)
    st.caption("📊 Progress: **0%** (No tasks scheduled for today)")




tab_active, tab_completed = st.tabs(["📂 Active Tasks", "📁 Completed Archive"])




# Folder 1: Active Tasks
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
           
            # Trigger confetti effect if the last active task was completed
            if len(day_tasks["active"]) == 0:
                st.balloons()
               
            st.rerun()




# Folder 2: Completed Tasks
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








# --- SECTION 2: STICKY NOTES INTERACTIVE DEDICATED WORKSPACE ---
st.write("---")
st.write("##### 📌 Interactive Scratchpad Board")




# Self-contained Canvas App that renders safely inside a designated box height
scratchpad_canvas_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    padding: 0;
    font-family: system-ui, -apple-system, sans-serif;
    overflow: hidden;
    background: transparent;
}
.board-container {
    width: 100%;
    height: 440px;
    position: relative;
    background-color: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    border: 2px dashed rgba(255, 255, 255, 0.4);
    border-radius: 16px;
    box-shadow: inset 0 4px 20px rgba(0,0,0,0.05);
}
.toolbar {
    display: flex;
    gap: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.5);
    border-bottom: 1px solid rgba(0,0,0,0.06);
    border-top-left-radius: 14px;
    border-top-right-radius: 14px;
}
.note-btn {
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.1s ease;
}
.note-btn:active { transform: scale(0.95); }
.yellow-btn { background: #FEF08A; color: #713F12; border: 1px solid #FDE047; }
.blue-btn { background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
.pink-btn { background: #FCE7F3; color: #9D174D; border: 1px solid #FBCFE8; }




.sticky-note {
    position: absolute;
    border-radius: 10px;
    box-shadow: 3px 6px 15px rgba(0,0,0,0.14);
    display: flex;
    flex-direction: column;
    z-index: 100;
    transition: box-shadow 0.2s ease;
   
    /* Dynamic UI Resize Additions */
    resize: both;
    overflow: hidden;
    min-width: 150px;
    min-height: 110px;
    max-width: 400px;
    max-height: 350px;
    box-sizing: border-box;
}
.sticky-note:focus-within {
    box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
}
.note-header {
    height: 26px;
    cursor: move;
    background: rgba(0,0,0,0.04);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.5px;
    user-select: none;
    flex-shrink: 0;
}
.note-close {
    cursor: pointer;
    font-size: 14px;
    opacity: 0.5;
    transition: opacity 0.2s;
}
.note-close:hover { opacity: 1; }
.note-body {
    flex: 1;
    border: none;
    outline: none;
    resize: none; /* Turn off internal textarea handle to prevent conflicts */
    background: transparent;
    padding: 10px;
    font-size: 14px;
    font-family: inherit;
    line-height: 1.4;
}
</style>
</head>
<body>
<div class="board-container" id="boardCanvas">
    <div class="toolbar">
        <button class="note-btn yellow-btn" onclick="addNote('yellow')">+ 🟡 Yellow Note</button>
        <button class="note-btn blue-btn" onclick="addNote('blue')">+ 🔵 Blue Note</button>
        <button class="note-btn pink-btn" onclick="addNote('pink')">+ 🌸 Pink Note</button>
    </div>
</div>




<script>
const canvas = document.getElementById('boardCanvas');




// Pull layout storage safely from the frame domain
let notes = JSON.parse(localStorage.getItem('embedded_sticky_notes') || '[]');




const themeConfigs = {
    yellow: { bg: '#FEF08A', text: '#713F12' },
    blue: { bg: '#E0F2FE', text: '#0369A1' },
    pink: { bg: '#FCE7F3', text: '#9D174D' }
};




function saveNotesToStorage() {
    localStorage.setItem('embedded_sticky_notes', JSON.stringify(notes));
}




function renderSingleNote(note) {
    const config = themeConfigs[note.color];
    const noteDiv = document.createElement('div');
    noteDiv.className = 'sticky-note';
    noteDiv.id = note.id;
    noteDiv.style.backgroundColor = config.bg;
    noteDiv.style.left = note.x + 'px';
    noteDiv.style.top = note.y + 'px';
   
    // Assign saved or default dimension parameters
    noteDiv.style.width = (note.w || 190) + 'px';
    noteDiv.style.height = (note.h || 140) + 'px';
   
    // Header Handle Section (Exclusively Handles Drags)
    const header = document.createElement('div');
    header.className = 'note-header';
    header.style.color = config.text;
    header.innerHTML = '<span>📌 Drag Handle</span>';
   
    const closeBtn = document.createElement('span');
    closeBtn.className = 'note-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = function(e) {
        e.stopPropagation();
        notes = notes.filter(n => n.id !== note.id);
        saveNotesToStorage();
        noteDiv.remove();
    };
    header.appendChild(closeBtn);
   
    // Dedicated Focusable Input Box
    const textarea = document.createElement('textarea');
    textarea.className = 'note-body';
    textarea.style.color = config.text;
    textarea.placeholder = 'Click here to write notes...';
    textarea.value = note.text;
   
    textarea.oninput = function() {
        note.text = textarea.value;
        saveNotesToStorage();
    };




    // Card background clicked triggers internal box autofocus perfectly
    noteDiv.onclick = function(e) {
        if(e.target !== header && e.target !== closeBtn) {
            textarea.focus();
        }
    };
   
    // Resize Observer: Watches sizing shifts and updates state instantly
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            note.w = noteDiv.offsetWidth;
            note.h = noteDiv.offsetHeight;
            saveNotesToStorage();
        }
    });
    resizeObserver.observe(noteDiv);
   
    // Core Isolated Draggable Mechanics
    header.onmousedown = function(e) {
        // Pull forward element visual layering stacking order
        document.querySelectorAll('.sticky-note').forEach(n => n.style.zIndex = "100");
        noteDiv.style.zIndex = "999";




        let shiftX = e.clientX - noteDiv.getBoundingClientRect().left;
        let shiftY = e.clientY - noteDiv.getBoundingClientRect().top;
       
        function moveAt(clientX, clientY) {
            let targetX = clientX - canvas.getBoundingClientRect().left - shiftX;
            let targetY = clientY - canvas.getBoundingClientRect().top - shiftY;
           
            // Boundary clamping adjusted dynamically to use note dimensions
            if (targetX < 4) targetX = 4;
            if (targetY < 55) targetY = 55;
            if (targetX > canvas.clientWidth - noteDiv.offsetWidth) targetX = canvas.clientWidth - noteDiv.offsetWidth;
            if (targetY > canvas.clientHeight - noteDiv.offsetHeight) targetY = canvas.clientHeight - noteDiv.offsetHeight;
           
            noteDiv.style.left = targetX + 'px';
            noteDiv.style.top = targetY + 'px';
            note.x = targetX;
            note.y = targetY;
            saveNotesToStorage();
        }
       
        function onMouseMove(event) {
            moveAt(event.clientX, event.clientY);
        }
       
        document.addEventListener('mousemove', onMouseMove);
        document.onmouseup = function() {
            document.removeEventListener('mousemove', onMouseMove);
            document.onmouseup = null;
        };
    };
   
    noteDiv.appendChild(header);
    noteDiv.appendChild(textarea);
    canvas.appendChild(noteDiv);
}




function addNote(color) {
    const stackingOffset = (notes.length * 20) % 160;
    const newNote = {
        id: 'note_' + Date.now(),
        color: color,
        text: '',
        x: 30 + stackingOffset,
        y: 80 + stackingOffset,
        w: 190,
        h: 140
    };
    notes.push(newNote);
    saveNotesToStorage();
    renderSingleNote(newNote);
}




// Initial hydration build frame loop execution block
notes.forEach(renderSingleNote);
</script>
</body>
</html>
"""




# Render the self-contained interactive board safely below the planner list
components.html(scratchpad_canvas_html, height=450)


