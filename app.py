import streamlit as st
import openai
st.title("What should you do about your :blue[Body] :muscle:")

user_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
openai.api_key = "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"
def get_openai_response(user_input):
       """
       This function sends the user input to OpenAI's Chat API and returns the model's response.
       """
       try:
           response = openai.ChatCompletion.create(
               model="gpt-4o-mini-2024-07-18",  # Specify the model for chat applications
               messages=[
                   {"role": "system", "content": "You are a helpful assistant."},
                   {"role": "user", "content": user_input},
               ]
           )
           # Extracting the text from the last response in the chat
           if response.choices:
               return response.choices[0].message['content'].strip()
           else:
               return "No response from the model."
       except Exception as e:
           return f"An error occurred: {str(e)}"

   # Streamlit app layout
   
st.title("Your Advanced Streamlit Chatbot")

user_input = st.text_input("What would you like to ask?")

if st.button("Submit"):
       if user_input:
           chatbot_response = get_openai_response(user_input)
           st.write(f"Chatbot: {chatbot_response}")
       else:
           st.write("Please enter a question or message to get a response.")
