import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools  # type: ignore
from langchain.tools import BaseTool
from typing import List
import json
import requests
import openai
from googletrans import Translator
import secrets

def main():
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Home","Self Learn","Discover","Mentor Guidance","Skill Test","Job Opportunities","Career Guidance","Education Loans / Schemes","Course Recommendations","About us"])
    
    with tab1:
        st.title("**Home**")
    
    with tab2:
        st.title("**Self Learn**")
        st.info("You can upload your study material and get best the way to learn")
        format = st.selectbox("Select the format of your study material",("Select","Text","Image","Video"))
        
        if format == "Text":
            input = st.text_input("Paste your study material here")
            
        elif format == "Image":
            input = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png", "gif"])
            
        elif format == "Video":
            input = st.text_input("Paste the Youtube link of the video here")
            
            if st.button("Search"):
                if input:
                    st.video(input)
                    res = video_description(input)
                    st.write(res)

                else:
                    st.warning("Paste the Youtube link of the video")
                    
        if format != "Select" and format == "Text":
            col1 , col2 = st.columns(2)
            
            with col1:
                st.subheader("Summarize")
                if st.button("Summarize the text material"):
                    res = summarize(input)
                    st.write(res)
                
            with col2:
                st.subheader("Translate")
                lan = st.selectbox("Select the language",("Select","Hindi","Tamil","Telugu","Kannada","Malayalam","Marathi","Bengali","Gujarati","Punjabi","Urdu"))
                if lan != "Select":
                    lan_code = get_language_code(lan)
                    res = translate(input,lan_code)
                    #res
                    st.write(res)
                    

        
        
    with tab3:
        st.title("**Discover**")

    with tab4:
        st.title("**Mentor Guidance**")
        input_topic = st.text_input("Enter the topic you want to learn")
        loc = st.text_input("Enter your location")
        if st.button("Search"):
            result = mentor(input_topic,loc)
            st.markdown("---")
            for i in result:
                if 'title' in i:
                    st.write("**Title** : "+i['title'])
                if 'address' in i:
                    st.write("**Address** : "+i['address'])
                if 'category' in i:
                    st.write("**Category** : "+i['category'])
                if 'phoneNumber' in i:
                    st.write("**Phone Number** : "+i['phoneNumber'])
                if 'rating' in i:
                    st.write("**Rating** : "+ str(int(i['rating'])))
                if 'ratingCount' in i:
                    st.write("**Rating Count** : "+ str(i['ratingCount']))
                if 'website' in i:
                    st.write("**Website** : "+i['website'])
                st.markdown("---")                
                
        
    with tab5:
        st.title("**Skill Test**")
        input_skill = st.text_input("Enter the skill you want to test")
        if input_skill:
            res_skill = skill(input_skill)
            st.markdown("---")
            for i, question in enumerate(res_skill):
                if 'question' in question:
                    st.write("**Question**: " + question['question'])
                    selected_option = st.radio("Options", question['options'])
                    if selected_option == question['answer']:
                        st.write("Correct Answer!")
                    else:
                        st.write("Incorrect Answer.")
                    st.write("Explanation: " + question['explanation'])
                st.markdown("---")
        
    with tab6:
        st.title("**Job Opportunities")
        
    with tab7:
        st.title("**Career Guidance**")
        
    with tab8:
        st.title("**Education Loans / Schemes")
        
    with tab9:
        st.title("**Course Recommendations**")
        
    with tab10:
        st.title("**About us**")
        
def skill(input_skill):
    
    query = (
        f"I need 5 Multiple choice questions in {input_skill} to test my skill. "
        "For this, I need 5 questions  with 4 options for each question. "
        "The JSON format should look like: "
        'skill : [{"question": "question", '
        '"options": ["option1", "option2", "option3", "option4"], '
        '"answer": "answer", '
        '"explanation": "explanation" }]'
    )
    
    messages = [
        {"role": "system", "content": "You are a kind helpful assistant."},
        {"role": "user", "content": query},
    ]
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    
    reply = chat.choices[0].message.content
    
    result = json.loads(reply)
    
    print(result)
    
    return result
    
    

def mentor(input_topic,loc):
    
    query = input_topic + "educational mentor in " + loc
    
    url = "https://google.serper.dev/places"

    payload = json.dumps({
    "q": query
    })
    headers = {
    'X-API-KEY': secrets.SERPER_API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #return only places
    res = json.loads(response.text)
    
    return res['places']

   
        
def summarize(input):
    
    query = input + "summarize it into simple paragraph with simple words and short sentences. in the given language of the input" 
    
    messages = [
        {"role" : "system", "content" : "You are a kind healpful assistant."},
    ]
    
    messages.append(
            {"role" : "user", "content" : query},
        )
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    
    reply = chat.choices[0].message.content
    
    print(reply)
    
    return reply
        
        
def get_language_code(lan):
    if lan == "Hindi":
        return "hi"
    elif lan == "Tamil":
        return "ta"
    elif lan == "Telugu":
        return "te"
    elif lan == "Kannada":
        return "kn"
    elif lan == "Malayalam":
        return "ml"
    elif lan == "Marathi":
        return "mr"
    elif lan == "Bengali":
        return "bn"
    elif lan == "Gujarati":
        return "gu"
    elif lan == "Punjabi":
        return "pa"
    elif lan == "Urdu":
        return "ur"
    else:
        return "en"
    
def translate(input,lan_code):
    translator = Translator()
    result = translator.translate(input, dest=lan_code)
    return result.text
    
        
        
def video_description(input):
    url = "https://youtube-summary-multilanguage.p.rapidapi.com/summarize/long/gpt-3.5-turbo"

    payload = {
        "url": input,
        "lang": "en"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": secrets.TRANSLATION_API_KEY,
        "X-RapidAPI-Host": "youtube-summary-multilanguage.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    
    print(data.get("summary",{}).get("text",""))
    
    return data.get("summary",{}).get("text","")

        
if __name__ == "__main__":
    main()