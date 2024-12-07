import streamlit as st
import openai
import pandas as pd
from io import BytesIO
import openpyxl

st.set_page_config(page_title="What should you do to your body",page_icon=":muscle:",layout="wide")

st.title("What should you do to your :blue[Body] :muscle:")

user_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

openai.api_key = user_api_key

if not user_api_key:
    st.error("Please enter a valid OpenAI API key to proceed.")





def get_openai_response(height, weight, age):
    # BMI Calculation
    height_m = height / 100  # Convert cm to meters
    bmi = weight / (height_m ** 2)

    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # For males; adjust for females as needed

    # Create pandas DataFrames for the meal plan and workout routine
    meals = {
        "Day": [f"Day {i}" for i in range(1, 8)],
        "Breakfast": ["Eggs & Oats"] * 7,  # Example meals
        "Lunch": ["Chicken & Veggies"] * 7,
        "Dinner": ["Salmon & Salad"] * 7
    }
    meals_df = pd.DataFrame(meals)

    workouts = {
        "Day": [f"Day {i}" for i in range(1, 8)],
        "Workout": ["Yoga" if i % 2 == 0 else "Strength Training" for i in range(1, 8)],
        "Duration": ["30 mins"] * 7,
        "Benefits": ["Flexibility and Relaxation" if i % 2 == 0 else "Strength Building" for i in range(1, 8)]
    }
    workouts_df = pd.DataFrame(workouts)

    # Prepare the prompt with these values for OpenAI
    prompt = f"""
    You are an exercise trainer and nutritionist. Based on the following information:
    - Height: {height} cm
    - Weight: {weight} kg
    - Age: {age} years
    
    1. Make the topic "BMI" large and calculate the **BMI**.
       Provide how to calculate the calories and
       give the client's calories and bmi standard with two columns: "Client's BMI", "BMI standard"
       and make the client's BMI column match the BMI standard. For example, if the client's BMI is 30, make it align with the BMI standard of 30.
       and hightlight the client what their BMI is.
       After that add a divider line.
    2. Make the topic "Calories" large and calculate the **Calories per day** 
       and provide how to calculate the calories 
       and the number of calories required per day for this person 
       and give the client's calories in a special column.
       After that add a divider line.
    3. Make the topic "7-day suggested meal plans" large 
       and provide a **meal plan for 7 days** with three columns: "Day", "Breakfast", "Lunch", and "Dinner" 
       and provide the number of calories of each meal in breakfast, lunch and dinner.
       After that add a divider line.
    4. Make the topic "7-day suggested workout plan" large 
       and provide a **workout plan for 7 days** with four columns: "Day", "Workout", "Duration", and "Benefits". 

    The meal plan should include common, healthy meals that suit this client’s caloric needs. 
    The workout plan should include a mix of cardio, strength training, and flexibility exercises, with clear benefits for each exercise.

    The response should be formatted as a simple table with the appropriate columns. 
    Display all the information (BMI, calories, meal plan, workout plan) in a clear and readable format.
    Use simple and friendly language.
    """

    # Calling the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure you're using the correct model
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": f"Height: {height} cm, Weight: {weight} kg, Age: {age} years"}]
        )

        # Extract response content
    chat_response = response['choices'][0]['message']['content']

    for_customer_df = pd.DataFrame({
        "BMI": [bmi], 
        "Calories Required": [bmr], 
        "Meal Plan": [meals_df], 
        "Workout Plan": [workouts_df]
    })


        # Return the response and the dataframes
    return chat_response, meals_df, workouts_df, for_customer_df



   
height = st.number_input("Please enter your height")
weight = st.number_input("Please enter your weight")
age = st.number_input("Please enter your age")

if st.button("Submit"):
    if height > 10 and weight > 10 and age > 0:
        # Get response from OpenAI and data for meal/workout plans
        chat_response, meals_df, workouts_df, for_customer_df = get_openai_response(height, weight, age)

        # Display the chatbot response
        st.write(chat_response)

        if not for_customer_df.empty:
            # Allow user to download the entire customer-specific data as an Excel file
            with BytesIO() as buf:
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    for_customer_df.to_excel(writer, sheet_name='User Data', index=False)
                buf.seek(0)
                st.download_button(
                    label="Download Complete Data",
                    data=buf,
                    file_name="user_health_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.write("Please enter valid values to get a response.")



