import speech_recognition as sr

def record_and_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Transcribing...")
        text = r.recognize_google(audio)
        with open('transcript.txt','a') as file:
            file.write(text + '\n')
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return ""

if __name__ == '__main__':
    record_and_transcribe()
