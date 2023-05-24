from GoogleFormsAPI import Quiz
from Speech_To_text import record_and_transcribe
from ChatgptAPI import chatAnswer
import streamlit as st

def start():
    # Start recording
    record_and_transcribe()
    chatAnswer("ChatGPT_Answer.txt","w")
    st.write('here is the google form Link for your Quiz: '+ Quiz("token.json"))

def main():
    st.title("Microphone Recorder")
    st.write("Click the button below to start.")
    if st.button('Start App'):
        st.write('Starting...')
        start()
        

if __name__ == "__main__":
    main()