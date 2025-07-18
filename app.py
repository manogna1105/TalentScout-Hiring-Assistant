import streamlit as st
import random

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.candidate = {
        "name": "",
        "email": "",
        "phone": "",
        "experience": "",
        "position": "",
        "location": "",
        "tech_stack": [],
        "answers": {}
    }
    st.session_state.tech_index = 0
    st.session_state.tech_questions = []
    st.session_state.current_question = 0

# Technical question bank
tech_questions = {
    "python": [
        "What are decorators in Python?",
        "Explain list comprehensions.",
        "Difference between list and tuple?"
    ],
    "javascript": [
        "What is event delegation?",
        "Difference between '==' and '==='?",
        "Explain closures in JavaScript."
    ]
}
default_questions = [
    "Your strongest skills?",
    "Challenging project in this tech?",
    "Best practices you follow?"
]

def get_questions(tech):
    tech = tech.lower()
    return random.sample(tech_questions.get(tech, default_questions), 3)

st.title("🧠 TalentScout Hiring Assistant")

# Step-by-step input flow
if st.session_state.stage == "start":
    st.session_state.stage = "name"

if st.session_state.stage == "name":
    st.subheader("👋 What's your full name?")
    name = st.text_input("Full Name")
    if name:
        st.session_state.candidate["name"] = name
        st.session_state.stage = "email"
        st.rerun()

if st.session_state.stage == "email":
    st.subheader("📧 Your Email Address?")
    email = st.text_input("Email")
    if email:
        st.session_state.candidate["email"] = email
        st.session_state.stage = "phone"
        st.rerun()

if st.session_state.stage == "phone":
    st.subheader("📱 Your Phone Number?")
    phone = st.text_input("Phone")
    if phone:
        st.session_state.candidate["phone"] = phone
        st.session_state.stage = "experience"
        st.rerun()

if st.session_state.stage == "experience":
    st.subheader("💼 Years of Experience?")
    experience = st.text_input("Experience")
    if experience:
        st.session_state.candidate["experience"] = experience
        st.session_state.stage = "position"
        st.rerun()

if st.session_state.stage == "position":
    st.subheader("🎯 Position You're Applying For?")
    position = st.text_input("Position")
    if position:
        st.session_state.candidate["position"] = position
        st.session_state.stage = "location"
        st.rerun()

if st.session_state.stage == "location":
    st.subheader("📍 Your Current Location?")
    location = st.text_input("Location")
    if location:
        st.session_state.candidate["location"] = location
        st.session_state.stage = "tech_stack"
        st.rerun()

if st.session_state.stage == "tech_stack":
    st.subheader("🛠️ Your Tech Stack?")
    techs = st.text_input("Comma-separated technologies (e.g. Python, JavaScript)")
    if techs:
        st.session_state.candidate["tech_stack"] = [t.strip().lower() for t in techs.split(",")]
        st.session_state.tech_questions = get_questions(st.session_state.candidate["tech_stack"][0])
        st.session_state.stage = "tech_questions"
        st.rerun()

if st.session_state.stage == "tech_questions":
    tech_list = st.session_state.candidate["tech_stack"]
    if st.session_state.tech_index < len(tech_list):
        tech = tech_list[st.session_state.tech_index]
        questions = st.session_state.tech_questions
        i = st.session_state.current_question

        st.subheader(f"🧪 Questions on {tech.title()}")
        question = questions[i]
        answer = st.text_input(f"Q{i+1}: {question}", key=f"q_{tech}_{i}")
        if answer:
            st.session_state.candidate["answers"][f"{tech} - {question}"] = answer
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(questions):
                st.session_state.tech_index += 1
                st.session_state.current_question = 0
                if st.session_state.tech_index < len(tech_list):
                    next_tech = tech_list[st.session_state.tech_index]
                    st.session_state.tech_questions = get_questions(next_tech)
                else:
                    st.session_state.stage = "summary"
            st.rerun()

if st.session_state.stage == "summary":
    st.success("✅ Screening Complete!")
    st.subheader("📝 Candidate Summary")
    for key, value in st.session_state.candidate.items():
        if key != "answers":
            st.markdown(f"**{key.capitalize()}:** {', '.join(value) if isinstance(value, list) else value}")
    st.subheader("💬 Technical Answers")
    for q, a in st.session_state.candidate["answers"].items():
        st.markdown(f"**Q:** {q}  \n**A:** {a}")
    st.balloons()
