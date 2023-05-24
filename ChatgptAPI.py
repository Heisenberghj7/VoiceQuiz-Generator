import openai

openai.api_key="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"

message_history = []

def chat(file, role="user"):
    content=""
    with open(file,'r') as f:
       input_text= f.readlines()
       for text in input_text:
           content+=text
    message_history.append({"role": role, "content": f"{content}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    print(message_history)
    return reply_content

if __name__ == '__main__':
    with open('ChatGPT_Answer.txt','w') as f:
      f.write(chat("transcript.txt"))
    