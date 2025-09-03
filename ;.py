import docx
import streamlit as st
from PIL import Image, ImageDraw
import math
import time
import random
import spacy
import base64
import inflect
import os
from mutagen import File
import wave
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    with st.spinner("Downloading spaCy model..."):
        download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    
p = inflect.engine()


main_container = st.empty()



if "page" not in st.session_state:
    st.session_state.page = "begin"
    st.session_state.info = None
    st.session_state.answer = None
    st.session_state.chosen = None
    st.session_state.answersList = None
    st.session_state.return_page = None
    st.session_state.question_count=0
    st.session_state.used_questions=[]
    st.session_state.incorrect_questions=[]
    st.session_state.incorrect_answers=[]
    st.session_state.correct_answers=[]
    st.session_state.correct_subjects=[]
    st.session_state.incorrect_subjects=[]
    st.session_state.total_questions=0
    st.session_state.total_wrong=0

    st.session_state.read_time=5
    st.session_state.minwait=1
    st.session_state.maxwait=5
    st.session_state.quiz_length=10
    st.session_state.play_sound=True
    st.session_state.sfxList=[False, False, True, False, False, False, False, False, False, False, False, False, False, False, False]
    st.session_state.audio=open(f"sfx/{os.listdir('sfx')[st.session_state.sfxList.index(True)]}","rb").read()
    st.session_state.fileType=f"audio/{os.listdir('sfx')[st.session_state.sfxList.index(True)].split(".")[-1]}"
    st.session_state.settings_rerun=False


audio = f"""
<audio autoplay>
  <source src="data:{st.session_state.fileType};base64,{base64.b64encode(st.session_state.audio).decode()}" type="{st.session_state.fileType}">
</audio>
"""
    


def set_page(page):
    st.session_state.page=page

def set_answer(answer):
    st.session_state.answer=answer





def BeginningPage():
    st.title("Place Holder Revision Thing TITLE PENDING")
    submit=True
    file = st.file_uploader("Upload a text file containing a list of facts to learn", type=["txt", "docx"])
    TypedFacts = st.text_area("Or enter them here (one per line):")

    if file is not None:
        if file.name.endswith("txt"):
            content = file.read().decode("utf-8").splitlines()
        elif file.name.endswith("docx"):
            doc = docx.Document(file)
            content = [para.text for para in doc.paragraphs if para.text.strip() != ""]
        st.session_state.uploaded_text = content
        submit=False

    elif TypedFacts.strip()!="":
        st.session_state.uploaded_text=TypedFacts.splitlines()
        submit=False

        if TypedFacts=="DEMO":
            file=open("demo.txt","r")
            st.session_state.uploaded_text=file.read().splitlines()
            file.close()
            set_page("home")
            st.rerun()

        

    col1, col2, col3=st.columns([1,3,1])
    with col2:
        if file is not None and TypedFacts.strip()!="":
            st.write("A file and text has been input, only the file will be used!")
    col1, col2, col3, col4, col5=st.columns(5)
    with col3:
        st.button("Submit", disabled=submit, on_click=set_page, args=['home'])




    
def HomePage():
    st.session_state.used_questions=[]
    st.session_state.question_count=0
    st.session_state.incorrect_questions=[]
    set_answer(None)
    
    with st.container():
        st.title("Place Holder Revision Thing TITLE PENDING")

        st.markdown("""
        <style>
        .stButton>button {
            width: 150px;
            height: 60px;
            border-radius: 10px;
            margin-top: 50px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.button("Relaxed Revision", on_click=set_page, args=['relaxed'])

        with col3:
            st.button("Pop Quiz", on_click=set_page, args=['pop'])

        with col5:
            st.button("Long Quiz", on_click=set_page, args=['long'])

        st.write("")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col2:
            st.button("Progress", on_click=set_page, args=['progress'])

        with col4:
            st.button("Settings", on_click=set_page, args=['settings'])





def RelaxedPage():
    st.button("←", on_click=set_page, args=['home'], key="back")

    st.session_state.return_page ="rest"
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { position: relative; }
    .timer {
      position: absolute;
      top: -375px;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 64px;
      font-weight: bold;
    }

    .info{
        position: absolute;

        font-size: 32px;
        font-weight: bold;
        z-index: 10;  
    }
    </style>
    """, unsafe_allow_html=True)

    st.session_state.info=st.session_state.uploaded_text[random.randint(0, len(st.session_state.uploaded_text)-1)]
    st.markdown(f"<div class='info'>{st.session_state.info}</div>", unsafe_allow_html=True)

    img = Image.new("RGB", (1000, 1000), "white")
    draw = ImageDraw.Draw(img)
    placeholder = st.empty()
    angle=270
    number_placeholder = st.empty()
    start=time.time()
    for i in range(72):
        for j in range(10):
            x = 500 + math.cos(math.radians(angle)) * 100
            y = 500 + math.sin(math.radians(angle)) * 100
            draw.line((500, 500, x, y), fill="blue", width=2)
            angle += 0.5
        placeholder.image(img)
        time.sleep(st.session_state.read_time/72)
        remaining = max(0, round(st.session_state.read_time - (time.time()-start)))
        number_placeholder.markdown(f"<div class='timer'>{remaining}</div>", unsafe_allow_html=True)

    st.session_state.page = "question"
    st.rerun()



    

def Question():
    info=nlp(st.session_state.info)
    st.button("←", on_click=set_page, args=['home'])
    

    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 5px;
            height:40px;
            width:150px;
            border: 1px solid #ccc;
            margin-top: 100px;
        }

        .styled-box {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-weight: 600;
        color: black;
        background-color: #f0f2f6;
        border: 1px solid #d3d3d3;
        border-radius: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        text-align: center;
        width: 100%;
        height: 20%;
        font-size:24px;
        font-family: Helvetica; 
        }
        </style>
        """, unsafe_allow_html=True)
    
    if st.session_state.answer==None:
        options = [token for token in nlp(st.session_state.info) if token.pos_ in ("NOUN", "PROPN", "VERB") and not token.is_stop and token.is_alpha]
        st.session_state.chosen=random.choice(options)
        if st.session_state.return_page=="pop":
            st.session_state.info=f"{st.session_state.question_count}) "+st.session_state.info
        st.markdown(f'<div class="styled-box">{st.session_state.info.replace(st.session_state.chosen.text,"___")}</div>', unsafe_allow_html=True)

        distractors=[]
        for i in range(len(st.session_state.uploaded_text)):
            doc = nlp(st.session_state.uploaded_text[i]) 
            for j in range(len(doc)):
                token = doc[j]
                
                if (token.morph==st.session_state.chosen.morph
                    and token.text.lower() not in st.session_state.info
                    and not token.is_stop and token.is_alpha
                    and token.text != st.session_state.chosen.text
                    and token.pos_ == st.session_state.chosen.pos_
                    and token.text.lower() not in distractors):
                    
                    distractors.append(token.text.lower())

        st.session_state.answersList=[st.session_state.chosen.text]
        while len(st.session_state.answersList)<4:
            distractor=random.choice(distractors)
            st.session_state.answersList.append(distractor)
            distractors.pop(distractors.index(distractor))
        random.shuffle(st.session_state.answersList)

        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,3,1,1,1,3,1])
        using=[col2, col6, col2, col6]
        for i in range(len(st.session_state.answersList)):
            with using[i]:
                st.button(st.session_state.answersList[i], on_click=set_answer, args=[st.session_state.answersList[i]])
            
    else:
        st.session_state.total_questions=st.session_state.total_questions+1
        subjects = set()
        for i in range(len(list(info.noun_chunks))):
            pro=False
            for j in range(len(list(info.noun_chunks)[i])):
                if list(info.noun_chunks)[i][j].pos_=="PRON":
                    pro=True
                    break
            if pro==False and list(info.noun_chunks)[i].root.dep_ in ("nsubj", "nsubjpass", "dobj", "pobj", "attr", "appos"):
                head=list(info.noun_chunks)[i].root
                noun=head.text.lower()
                if "Number=Sing" in head.morph:
                    noun=p.plural(noun)
                subjects.add(noun)
        
        st.markdown(f'<div class="styled-box">{st.session_state.info.replace(st.session_state.chosen.text, f"<span style=\'color:orange; font-weight:bold;\'>{st.session_state.chosen.text}</span>")}</div>',unsafe_allow_html=True)
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,3,1,1,1,3,1])
        using=[col2, col6, col2, col6]

        for i in range(len(st.session_state.answersList)):
            if st.session_state.answersList[i] == st.session_state.chosen.text:
                colour="lightgreen"
                if st.session_state.answer==st.session_state.chosen.text:
                    st.session_state.correct_subjects=st.session_state.correct_subjects+list(subjects)
            elif st.session_state.answersList[i] == st.session_state.answer and st.session_state.chosen.text!= st.session_state.answer:
                colour="tomato"
                st.session_state.incorrect_subjects=st.session_state.incorrect_subjects+list(subjects)
                st.session_state.total_wrong=st.session_state.total_wrong+1
                if st.session_state.page!="relaxed":
                    st.session_state.incorrect_questions.append(st.session_state.info)
                    st.session_state.incorrect_answers.append(st.session_state.answer)
                    st.session_state.correct_answers.append(st.session_state.chosen.text)

            else:
                colour="grey"

            with using[i]:
                button = f"""
                <button style="
                    background-color:{colour};
                    border-radius: 5px;
                    height:40px;
                    width:150px;
                    border: 1px solid #ccc;
                    font-size:16px;
                    margin-top: 100px;
                ">
                {st.session_state.answersList[i]}
                </button>
                """

                clicked = st.markdown(button, unsafe_allow_html=True)

        time.sleep(2)
        set_page(st.session_state.return_page)
        set_answer(None)
        st.rerun()





def rest():
    st.button("←", on_click=set_page, args=['home'])

    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pangolin&display=swap');
    .resttext{
        font-family: Pangolin;
        font-size:64px;
        margin-top:20%;
        margin-bottom:20%;
    }
    </style>
    """,
    unsafe_allow_html=True)

    col1, col2, col3, col4, col5=st.columns([1,2,2,1,1])
    with col3:
        st.markdown('<div class="resttext">Rest</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display: flex;
        justify-content: center;
        align-items: center;
        margin-left:10%;">
            <img src="data:image/png;base64,{base64.b64encode(open("tea.png", "rb").read()).decode("utf-8")}">
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(random.randint(st.session_state.minwait*60,st.session_state.maxwait*60))
    if st.session_state.play_sound==True:
        st.markdown(audio, unsafe_allow_html=True)
        
    set_page("relaxed")
    st.rerun()
    



    
def quiz():
    st.session_state.question_count+=1
    st.session_state.return_page=st.session_state.page

    question=random.choice(list(set(st.session_state.uploaded_text) ^ set(st.session_state.used_questions)))
    st.session_state.used_questions.append(question)
        
    if st.session_state.page=="pop":
        length=st.session_state.quiz_length
    elif st.session_state.page=="long":
        length=len(st.session_state.uploaded_text)

    st.write(st.session_state.question_count, length)
    if st.session_state.question_count<=length and len(st.session_state.uploaded_text)!=len(st.session_state.used_questions):
        st.session_state.info=question
        st.session_state.page = "question"
        st.rerun()
    else:
        st.session_state.page = "results"
        st.rerun()
    
    



def results():
    st.markdown("""
    <style>
    .stButton>button {
        width: 150px;
        height: 60px;
        border-radius: 10px;
        margin-top: 40%;
        margin-bottom:20%;
    }
    </style>
    """, unsafe_allow_html=True)

    
    score=st.session_state.question_count-len(st.session_state.incorrect_questions)
    if score==st.session_state.question_count:
        colour="blue"
    elif score >= (st.session_state.question_count/3)*2:
        colour="green"
    elif score > st.session_state.question_count/3:
        colour="orange"
    elif score <= st.session_state.question_count/3:
        colour="red"

        
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pangolin&display=swap');
        .result {{
            font-family: 'Pangolin', cursive;
            font-size: 64px;
            margin-left: 45%;
            color: {colour};
        }}

        .incorrect{{
            font-family: 'Pangolin', cursive;
            font-size: 80px;
            color: red;
            margin-left:5%;
        }}

        .correct{{
            font-family: 'Pangolin', cursive;
            font-size: 80px;
            color: green;
            margin-left:5%;
        }}

        .question{{
            font-size: 20px;
            text-align:center;
            margin-bottom:5%;
        }}

        .answer{{
            font-size: 20px;
            text-align:center;
            margin-bottom:20%;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="result">{score-1}/{st.session_state.question_count-1}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,1,1,2,3,1,1,1,1])
    with col5:
        st.button("Continue", on_click=set_page, args=['home'])

    if len(st.session_state.incorrect_questions)>0:
        st.markdown(f'<div class="incorrect">Wrong Answers ✘</div>', unsafe_allow_html=True)

        for i in range(len(st.session_state.incorrect_questions)):
            st.markdown(f'<div class="question">{st.session_state.incorrect_questions[i].replace(st.session_state.correct_answers[i],"___")}</div>', unsafe_allow_html=True)
            wrong = f"""
            <button style="
                background-color:tomato;
                border-radius: 5px;
                height:40px;
                width:150px;
                border: 1px solid #ccc;
                font-size:16px;
                margin-top: 15%;
                margin-bottom:25%;
            ">
            {st.session_state.incorrect_answers[i]}
            </button>
            """

            right = f"""
            <button style="
                background-color:lightgreen;
                border-radius: 5px;
                height:40px;
                width:150px;
                border: 1px solid #ccc;
                font-size:16px;
                margin-top: 15%;
                margin-bottom:25%;
            ">
            {st.session_state.correct_answers[i]}
            </button>
            """

            col1,col2,col3,col4,col5=st.columns([1,1,1,1,1])
            with col2:
                st.markdown(wrong, unsafe_allow_html=True)
            with col4:
                st.markdown(right, unsafe_allow_html=True)

            st.markdown(f'<div class="answer">{st.session_state.incorrect_questions[i].replace(st.session_state.correct_answers[i], f"<span style=\'color:orange; font-weight:bold;\'>{st.session_state.correct_answers[i]}</span>")}</div>',unsafe_allow_html=True)


    else:
        st.markdown(f'<div class="correct">No Wrong Answers To Report ✔</div>', unsafe_allow_html=True)





def progress():
    st.markdown("""
    <style>
    .stButton>button {
        width: 150px;
        height: 60px;
        border-radius: 10px;
        margin-top: 40%;
        margin-bottom:20%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    correct=[]
    incorrect=[]
    tempCorrect=st.session_state.correct_subjects
    tempIncorrect=st.session_state.incorrect_subjects
    temps=[tempCorrect, tempIncorrect]
    corrects=[correct, incorrect]
    for j in range(2):
        if len(temps[j])>0:
            for i in range(5):
                mode=max(set(temps[j]), key=temps[j].count)
                corrects[j].append(f"{i+1}) {mode}")
                while mode in temps[j]:
                    temps[j].remove(mode)
        else:
            corrects[j].append("None")
                
    st.write(f"Total Questions Answered: {st.session_state.total_questions}")
    st.write(f"Correct Answers: {st.session_state.total_questions-st.session_state.total_wrong}")
    st.write(f"Wrong Answers: {st.session_state.total_wrong}")
    st.write("Strongest Topics: ")
    for i in range(len(correct)):
        st.write(correct[i])
    st.write("Weakest Topics: ")
    for i in range(len(incorrect)):
        st.write(incorrect[i])

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,1,1,2,3,1,1,1,1])
    with col5:
        st.button("Continue", on_click=set_page, args=['home'])



        

def settings():
    if  st.session_state.settings_rerun==True:
        st.markdown(audio, unsafe_allow_html=True)
        st.session_state.settings_rerun=False
        
    readTimeSlider = st.slider('Read Timer Length (Seconds)', 5, 30, step=1, value=st.session_state.read_time)
    restRange = st.slider('Rest Time Range (Minutes)', 1, 60, (st.session_state.minwait, st.session_state.maxwait))
    quizLength = st.slider('Pop Quiz Number Of Questions', 5, 25, step=1, value=st.session_state.quiz_length)
    sound= st.checkbox("Play Sound Alert After Rest Time", value=st.session_state.play_sound)

    col1,col2,col3=st.columns(3)
    if sound==True:
        for i in range(len(os.listdir("sfx"))):
            if i%3==0:
                col=col1
            elif i%3==1:
                col=col2
            elif i%3==2:
                col=col3
            with col:
                sfx=st.checkbox(os.listdir("sfx")[i].split(".mp3")[0], value=st.session_state.sfxList[i])
            if sfx==True and st.session_state.sfxList[i]==False:
                for j in range(len(st.session_state.sfxList)):
                    st.session_state.sfxList[j]=False
                st.session_state.sfxList[i]=True
                st.session_state.audio=open(f"sfx/{os.listdir('sfx')[st.session_state.sfxList.index(True)]}","rb").read()
                st.session_state.fileType=f"audio/{os.listdir('sfx')[st.session_state.sfxList.index(True)].split(".")[-1]}"
                st.session_state.settings_rerun=True
                st.rerun()
                
        custom = st.file_uploader("Input custom sound (max 10 seconds)", type=["mp3", "wav", "m4a", "ogg"])
        if custom is not None:
            if custom.name.split(".")[-1]!="wav":
                length=File(custom).info.length
            else:
                custom.seek(0)
                customFile=wave.open(custom,"rb")
                length=customFile.getnframes()/float(customFile.getframerate())
                customFile.close()
            custom.seek(0)
            if length<=10:
                st.session_state.audio=custom.read()
                st.session_state.fileType=f"audio/{custom.name.split(".")[-1]}"
                for j in range(len(st.session_state.sfxList)):
                    st.session_state.sfxList[j]=False
                st.session_state.settings_rerun=True




                    

    st.button("Back", on_click=set_page, args=['home'])
    
    if st.button("Save And Continue"):
        set_page("home")
        st.session_state.read_time=readTimeSlider
        st.session_state.minwait=restRange[0]
        st.session_state.maxwait=restRange[1]
        st.session_state.quiz_length=quizLength
        st.session_state.play_sound=sound
        st.rerun()

    if st.button("Reset To Default Settings"):
        set_page("home")
        st.session_state.read_time=15
        st.session_state.minwait=5
        st.session_state.maxwait=10
        st.session_state.quiz_length=10
        st.session_state.play_sound=True
        st.session_state.sfxList=[False, False, True, False, False, False, False, False, False, False, False, False, False, False, False]
        st.rerun()




    
if st.session_state.page=="begin":
    with main_container.container():
        BeginningPage()
    
elif st.session_state.page=="home":
    with main_container.container():
        HomePage()
    
elif st.session_state.page=="relaxed":
    with main_container.container():
        RelaxedPage()

elif st.session_state.page=="question":
    with main_container.container():
        Question()

elif st.session_state.page=="rest":
    with main_container.container():
        rest()

elif st.session_state.page=="pop" or st.session_state.page=="long":
    with main_container.container():
        quiz()

elif st.session_state.page=="results":
    with main_container.container():
        results()

elif st.session_state.page=="progress":
    with main_container.container():
        progress()

elif st.session_state.page=="settings":
    with main_container.container():
        settings()


