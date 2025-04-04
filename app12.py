import streamlit as st
from datetime import datetime
st.set_page_config(
    page_title="My college Helper",
    page_icon="🧑‍🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "conversation" not in st.session_state:
    st.session_state.conversation = [{
        "role": "Assistant",
        "content": "Hello! I'm your college helper, here to listen and guide you on your amazing journey ahead!",
        "time": datetime.now().strftime("%H:%M"),
        "type": "greeting"
    }]

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "rerun_trigger" not in st.session_state:
    st.session_state["rerun_trigger"] = False


if "query_history" not in st.session_state:
    st.session_state.query_history = {}  
if "last_query_type" not in st.session_state:
    st.session_state["last_query_type"] = "General"


query_categories = {
    "admissions": "Admissions Process",
    "courses": "Available Courses",
    "fees": "Fee Structure",
    "scholarships": "Scholarship & Financial Aid",
    "campus_life": "Hostel & Student Activities",
    "placements": "Placements & Career Opportunities"
}

if "last_query_type" not in st.session_state:
    st.session_state["last_query_type"] = "General"  # Default category


import random

import re



















import time
import torch

@st.cache_resource
def load_device():
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"

device = load_device()  # Now cached, reducing startup time

def update_query_tracking(user_input):
    """Analyzes user input and categorizes it into college-related topics."""
    if "query_metrics" not in st.session_state:
        st.session_state.query_metrics = {"total_queries": 0, "categories": {}}

    query_keywords = {
        "admissions": ["admission", "apply", "eligibility", "deadline", "process"],
        "courses": ["course", "subject", "program", "degree", "syllabus"],
        "fees": ["fees", "cost", "tuition", "payment", "scholarship"],
        "scholarships": ["scholarship", "financial aid", "grants", "funding"],
        "campus_life": ["hostel", "dorm", "clubs", "activities", "facilities"],
        "placements": ["placement", "job", "internship", "career", "recruitment"]
    }

    detected_category = "general"
    for category, keywords in query_keywords.items():
        if any(word in user_input.lower() for word in keywords):
            detected_category = category
            break

    # Update query tracking metrics
    st.session_state.query_metrics["total_queries"] += 1
    st.session_state.query_metrics["categories"].setdefault(detected_category, 0)
    st.session_state.query_metrics["categories"][detected_category] += 1




def update_query_tracker(query_type):
    """Updates the query tracker based on detected category."""
    query_map = {
        "admissions": "📜 Admissions Process",
        "courses": "📚 Available Courses",
        "fees": "💰 Fee Structure",
        "scholarships": "🎓 Scholarships & Financial Aid",
        "campus_life": "🏠 Campus Life & Hostels",
        "placements": "🚀 Placements & Career Opportunities",
        "general": "❓ General Inquiry"
    }
    
    
    st.session_state["last_query_type"] = query_map.get(query_type, "❓ General Inquiry")












query_categories = {
    "default": "❓ General Inquiry",
    "admissions": "📜 Admissions Process",
    "courses": "📚 Available Courses",
    "fees": "💰 Fee Structure",
    "scholarships": "🎓 Scholarships & Financial Aid",
    "campus_life": "🏠 Campus Life & Hostels",
    "placements": "🚀 Placements & Career Opportunities"
}

st.markdown("""
<style>
    /* Overall App Styling */
    .main {
        background-color: #fafafa;
        padding: 2rem;
    }
    
    /* Header Styling */
    h1 {
        color: #4285F4;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Chat Container */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Chat Bubbles */
    .chat-bubble {
        border-radius: 18px;
        padding: 12px 16px;
        margin-bottom: 12px;
        max-width: 80%;
        word-wrap: break-word;
        position: relative;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background-color: #E2F2FF;
        color: #1E3A8A;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-bubble {
        background-color: #F0F4F9;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.7rem;
        color: #888;
        margin-top: 4px;
        text-align: right;
    }
    
    /* Input box styling */
    .stTextInput input {
        border-radius: 25px !important;
        padding: 10px 20px !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    .stTextInput input:focus {
        border-color: #4285F4 !important;
        box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2) !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 25px;
        background-color: #4285F4;
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #3367D6;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Resource cards */
    .resource-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #4285F4;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Query Category Indicator */
    .query-category {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    .query-category.selected {
        background-color: #E2F2FF;
        border-color: #4285F4;
    }

</style>
""", unsafe_allow_html=True)


st.sidebar.header("🎓 College Query Assistant")
st.sidebar.write(f"**Last Query Category:** {st.session_state.get('last_query_type', '❓ General Inquiry')}")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/College_building_icon.svg/512px-College_building_icon.svg.png", width=50)  # Placeholder for a college logo
    st.title("College Query Assistant")

    st.sidebar.subheader("📌 Common Query Categories")
    st.sidebar.markdown(f"### {st.session_state.get('last_query_type', '❓ General Inquiry')}")  

    st.markdown("""
    ## Need More Help?
    Check out the official college resources below:
    """)
    
    st.info("""
    - **[Admissions Portal](https://www.google.com/search?q=admissions+guide+for+class+12+students+in+india&oq=admissions+guide+for+class+12+students+in+india&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQLhhA0gEJMTIzODhqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8)**
    - **[Course Catalog](https://www.example.com/courses)**
    - **[Fee Structure](https://www.example.com/fees)**
    - **[Scholarship Information](https://www.example.com/scholarships)**
    - **[Campus Life](https://www.example.com/campus)**
    """)

    st.warning("""
    ### 📞 Contact College Support:
    - **Phone:** +91 8076817885  
    - **Email:** 2229122@kiit.ac.in  
    - **Office Hours:** Mon-Fri, 9 AM - 5 PM  
    """)
    
    
import streamlit as st
from datetime import datetime

st.sidebar.markdown("## 🎓 College Query Categories")
st.sidebar.caption("What would you like to know?")


query_map = {
    "admissions": "📜 Admissions",
    "courses": "📚 Courses",
    "fees": "💰 Fees & Payments",
    "scholarships": "🎓 Scholarships",
    "campus_life": "🏠 Campus Life",
    "placements": "🚀 Placements",
    "general": "❓ General Inquiry"
}


st.markdown("""
    <style>
    div.stButton > button {
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 10px;
        background-color: #4A90E2;
        color: white;
        border: none;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


cols = st.sidebar.columns(3)  
for i, (query_value, query_text) in enumerate(query_map.items()):
    with cols[i % 3]:  
        if st.button(query_text, key=f"query_btn_{query_value}"):
            st.session_state.last_query_type = query_value
            today = datetime.now().strftime("%Y-%m-%d")
            if "query_history" not in st.session_state:
                st.session_state.query_history = {}
            st.session_state.query_history[today] = query_text


if "last_query_type" in st.session_state:
    current_query_display = query_map.get(st.session_state.last_query_type, "❓ General Inquiry")
    st.sidebar.markdown(f"### Selected Query: {current_query_display}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Info")

    query_tips = {
        "admissions": "📜 Admissions are open! Check application deadlines and eligibility on the official website.",
        "courses": "📚 Explore available courses, syllabus details, and elective options.",
        "fees": "💰 Find tuition fees, payment methods, and due dates for this semester.",
        "scholarships": "🎓 Learn about available scholarships and financial aid opportunities.",
        "campus_life": "🏠 Discover hostel facilities, student clubs, and extracurricular activities.",
        "placements": "🚀 Get insights on placements, top recruiters, and internship opportunities.",
        "general": "❓ Ask any general queries related to the college experience."
    }

    current_query_tip = query_tips.get(st.session_state.last_query_type, "Need more help? Feel free to ask anything!")
    st.sidebar.info(current_query_tip)



    






@st.cache_data
def preprocess_text(text):
    """Preprocess text with tokenization and lemmatization."""
    text = text.lower()
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized)
















if "context_memory" not in st.session_state:
    st.session_state.context_memory = []


if "last_query_type" not in st.session_state:
    st.session_state["last_query_type"] = "General Inquiry"


query_map = {
    "admissions": "📜 Admissions",
    "courses": "📚 Courses",
    "fees": "💰 Fees & Payments",
    "scholarships": "🎓 Scholarships",
    "campus_life": "🏠 Campus Life",
    "placements": "🚀 Placements",
    "general": "❓ General Inquiry"
}


import random
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)  

def find_best_response(user_input):
    """Uses Google Gemini API to generate a response and detect query type."""
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  
        response = model.generate_content([user_input])  
        bot_response = response.text.strip()
        
        
        query_model = genai.GenerativeModel("gemini-1.5-flash-latest")
        query_analysis = query_model.generate_content([
            f"Categorize this college-related query: '{user_input}'. "
            "Return only one word from this list: admissions, courses, fees, scholarships, campus_life, placements, general."
        ])

        detected_query = query_analysis.text.strip().lower()

        return bot_response, detected_query  

    except Exception as e:
        print("Error:", e)
        return "I'm here to assist you with college queries. Can you provide more details?", "general"




















    
    st.session_state.context_memory.append(user_input)
    if len(st.session_state.context_memory) > 3:
        st.session_state.context_memory.pop(0)

    
    if detected_query and detected_query in query_map:
        st.session_state["last_query_type"] = query_map[detected_query]

    return response











def generate_college_response(user_input):
    """Generate chatbot response using Google Gemini API for college-related queries."""
    response, detected_query = find_best_response(user_input)  
    update_query_tracker(detected_query)  
    return response if response else "I'm here to help! What would you like to know about?"












import streamlit as st
from datetime import datetime

def on_send():
    user_msg = st.session_state.get("input_text", "").strip()

    if user_msg:
        timestamp = datetime.now().strftime("%H:%M")

        
        st.session_state["conversation"].append({
            "role": "User",
            "content": user_msg,
            "time": timestamp
        })

        
        if not is_relevant(user_msg):
            st.session_state["conversation"].append({
                "role": "Assistant",
                "content": "I'm here to help with college-related queries. Let me know if you have questions about admissions, courses, fees, or anything else.",
                "time": datetime.now().strftime("%H:%M")
            })
            st.session_state["input_text"] = ""  
            return

        
        if "query_metrics" not in st.session_state:
            st.session_state["query_metrics"] = {
                "total_queries": 0,
                "user_queries": 0,
                "bot_responses": 0,
                "categories": {}
            }

        
        st.session_state["query_metrics"]["user_queries"] += 1
        st.session_state["query_metrics"]["total_queries"] += 1

        
        update_query_tracking(user_msg)

        
        simulate_bot_typing()

        
        st.session_state["input_text"] = ""











import threading
import time
from datetime import datetime

def simulate_bot_typing():
    """Simulate chatbot typing, consider past messages, and generate responses."""
    user_messages = [msg["content"] for msg in st.session_state.conversation if msg["role"] == "User"]

    if user_messages:
        last_user_msg = user_messages[-1]
        st.session_state.is_typing = True
        time.sleep(1)  # Short delay for typing effect

        bot_msg = generate_college_response(last_user_msg)

        st.session_state.conversation.append({
            "role": "Assistant",
            "content": bot_msg,
            "time": datetime.now().strftime("%H:%M")
        })

        # ✅ Increment Bot Responses Count
        st.session_state.query_metrics["bot_responses"] += 1

        st.session_state.is_typing = False








 






if "rerun_trigger" in st.session_state and st.session_state["rerun_trigger"]:
    st.session_state["rerun_trigger"] = False  











st.title("🎓 College Query Assistant")
st.caption("Ask about admissions, courses, fees, scholarships, and more!")

tab_chat, tab_resources, tab_insights = st.tabs(["💬 Chat", "📚 College Resources", "📊 Query Insights"])

#  Chat Tab
with tab_chat:
    
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
    
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.conversation:
        bubble_class = "assistant-bubble" if msg["role"] == "Assistant" else "user-bubble"
        st.markdown(
            f"""
            <div class="chat-bubble {bubble_class}">
                <p>{msg["content"]}</p>
                <div class="timestamp">{msg["time"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # If the bot is 'typing', show indicator
    if st.session_state.is_typing:
        st.markdown(
            """
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if "typing_triggered" not in st.session_state or not st.session_state.typing_triggered:
        st.session_state.typing_triggered = True  
        simulate_bot_typing()  
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User input + Send button
    st.text_input("Type your question here:", key="input_text", on_change=on_send)

    st.button("Send", on_click=on_send)
    
#  Resources Tab
with tab_resources:
    st.subheader("📚 College Resources")
    st.markdown("""
    - [📜 Admissions Guide](https://www.example.com/admissions)
    - [📚 Course Catalog](https://www.example.com/courses)
    - [💰 Fee Structure](https://www.example.com/fees)
    - [🎓 Scholarship Information](https://www.example.com/scholarships)
    - [🏠 Campus Life & Hostels](https://www.example.com/campus-life)
    """)

    st.markdown("---")
    st.info("Need help? Visit the official college website or contact the support desk.")

# Insights Tab
with tab_insights:
    st.subheader("📊 Query Insights")
    
    # Ensure query metrics are initialized
    if "query_metrics" not in st.session_state:
        st.session_state["query_metrics"] = {
            "total_queries": 0,
            "user_queries": 0,
            "bot_responses": 0,
            "categories": {}
        }

    # Safely initialize specific metrics if missing
    st.session_state["query_metrics"].setdefault("user_queries", 0)
    st.session_state["query_metrics"].setdefault("bot_responses", 0)

    # Display User and Bot Messages
    user_queries = st.session_state["query_metrics"]["user_queries"]
    bot_responses = st.session_state["query_metrics"]["bot_responses"]

    st.write(f"**Total User Queries:** {user_queries}")
    st.write(f"**Total Bot Responses:** {bot_responses}")

    # Display categories discussed
    category_data = st.session_state["query_metrics"].get("categories", {})
    if category_data:
        st.write("**Categories Discussed:**")
        for category, count in category_data.items():
            st.write(f"- {category}: {count} times")
    else:
        # Fallback if no topics are detected
        if "conversation" in st.session_state and st.session_state["conversation"]:
            recent_msgs = [msg["content"] for msg in st.session_state["conversation"] if msg["role"] == "User"]
            if recent_msgs:
                st.write("No specific categories detected yet, but I noticed you mentioned:")
                for msg in recent_msgs[-3:]:  # Show the last 3 user messages
                    st.write(f"💬 \"{msg}\"")
                st.write("Feel free to ask about admissions, courses, fees, or placements!")
            else:
                st.write("No conversation data yet. Ask your first question!")
        else:
            st.write("No conversation data yet. Ask your first question!")

# Initialize session memory for context tracking
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

import re

def is_relevant(user_input):
    """Enhanced relevancy filter for college-related queries with context awareness."""
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Append the current message to the conversation history
    st.session_state.conversation_history.append(user_input.lower())
    
    # Combine the last 3 messages for context
    context_window = " ".join(st.session_state.conversation_history[-3:])

    # ✅ College-related keywords
    relevant_keywords = [
        # 📜 Admissions
        "admission", "apply", "application", "eligibility", "requirements", 
        "deadlines", "cutoff", "merit list", "entrance exam",

        # 📚 Courses & Academics
        "courses", "subjects", "syllabus", "curriculum", "degree", "credits",
        "electives", "specialization", "major", "minor", "faculty", "professor",

        # 💰 Fees & Scholarships
        "fees", "tuition", "scholarship", "financial aid", "grants", "loans",
        "waiver", "payment methods", "fee structure",

        # 🏠 Campus Life & Facilities
        "hostel", "dorm", "accommodation", "clubs", "extracurricular", 
        "cafeteria", "library", "sports", "student council", "events",

        # 🚀 Placements & Career
        "placements", "internship", "recruiters", "package", "job offers", 
        "career services", "resume", "interview prep", "alumni network",

        # ❓ General College Queries
        "timings", "attendance", "grading system", "holidays", "faculty contact", 
        "email", "official website", "college rules", "help desk", "office hours"
    ]

    
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "what's up"]

    
    if any(word in user_input.lower() for word in relevant_keywords + greetings):
        return True

    
    if len(user_input.split()) > 5 or len(context_window.split()) > 20:
        return True

    return False








