import streamlit as st
import os
import requests
import PyPDF2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

os.makedirs("drawings", exist_ok=True)
st.set_page_config(
    page_title="study with me", page_icon="🎀", layout="centered")
 #دالة الai
def ai(prompt):
    key = st.secrets["GEMINI_API_KEY"]
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(
            url,
            headers={
                "x-goog-api-key": key,
                "Content-Type": "application/json"
            },
            json=data
        )

        result = response.json()

        if "error" in result:
            return "Gemini error"

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return "Something went wrong"


def go(page):
    st.session_state.page = page
    st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "Home"


#home

if st.session_state.page == "Home":
    st.title("Study with me 🎀 ")
    st.write("Lets Study Together With AI 🎀🌝✨")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(" Ai Assistant 🤖"):
            go("Planner")

        if st.button('dictionary 📖'):
            go("Dictionary")

    with col2:
        if st.button("Planner 📅"):
            go("Planner")

        if st.button("Drawing 🎨"):
            go("Drawing")

# ai assistant
 
elif st.session_state.page == "ai":
   st.title("ai assistant ")
   if st.button("home"):
       go ("home")

   question = st.text_input("ask gemini any thing you want")
   if st.button("ask") and question:
            st.write(ai(question))

# dictionary

elif st.session_state.page == "dictionary":
    st.title(" dictionary")
    if st.button("home"):
      go("home")

    word = st.text_input("enter aword")
    if st.button("explain") and word:
        st.write(ai("explian this word simply and give an example:"+word))

        #planner   

    elif st.session_state.page == "planner":
            st.title(" planner")
            if st.button("home"):
                go("home")

    subject = st.text_input(" subject")
    date = st.date_input(" date")
    time = st.time_input(" time")
    if st.button("add session"):
            with open("planner.txt", "a") as f:
                st.success(f"{subject} - {date} - {time}\n")






# DRAWING

elif st.session_state.page == "Drawing":

    st.title(" Drawing Notes 🖌📍")

    if st.button("🏠 Home"):
        go("Home")

    name = st.text_input(" Note name ")
    color = st.color_picker(" Choose a color 🎨 ", "#D13D56")

    canvas = st_canvas(
        stroke_width=st.slider(" Pen size ✏️", 1, 20, 3),
        stroke_color=color,
        background_color="white",
        height=400,
        width=700,
        key="drawing"
    )

    if st.button("💾 Save"):
        if name:
            Image.fromarray(
                canvas.image_data.astype("uint8")
            ).save(f"drawings/{name}.png")
            st.success("Saved 🎀💟")
    files = os.listdir("drawings")

    if files:
        selected = st.selectbox("📂 My Notes", files)
        st.image(f"drawings/{selected}")