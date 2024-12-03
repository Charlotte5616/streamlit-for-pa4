import streamlit as st
import openai
st.set_page_config(page_title="What should you do about your body",page_icon=":muscle:",layout="wide")

st.title("What should you do about your :blue[Body] :muscle:")

user_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

openai.api_key = "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"

def get_openai_response(height, weight):
       """
       This function you need to act as an exercise trainer and nutritionist. My client wants to know how to gain or lose weight (through food and exercise) if their BMI is above or below the standard range. Please show their BMI and provide a table of recommended meals (breakfast, lunch, and dinner) for one month. Additionally, recommend workout videos and explain how they should exercise each day, describing the benefits of the videos. Use simple language and refer to any available evidence.
       """
       try:
           response = openai.ChatCompletion.create(
               model="gpt-4o-mini-2024-07-18",  # Specify the model for chat applications
               messages=[
                   {"role": "system", "content": "You are a helpful assistant."},
                   {"role": "user", "content": height and weight},
               ]
           )
           # Extracting the text from the last response in the chat
           if response.choices:
               return response.choices[0].message['content'].strip()
           else:
               return "No response from the model."
       except Exception as e:
           return f"An error occurred: {str(e)}"
       except openai.error.RateLimitError:
            # Handle rate limit error gracefully
            st.error("Rate limit exceeded. Please try again later.")
       except openai.error.OpenAIError as e:
            # Handle other OpenAI API errors
            st.error(f"An error occurred: {e}")

   # Streamlit app layout
   
height = st.text_input("Please enter your height")
weight = st.text_input("Please enter your weight")

if st.button("Submit"):
       if height and weight:
           chatbot_response = get_openai_response(height , weight)
           st.write(f"Chatbot: {chatbot_response}")
       else:
           st.write("Please enter a question or message to get a response.")

