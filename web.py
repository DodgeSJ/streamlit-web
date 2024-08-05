import pandas as pd
import streamlit as st
# from streamlit_gsheets import GSheetsConnection

# # Define your spreadsheet ID
# SPREADSHEET_ID = '1qqu0xTwXrtDMGqVxmLHJON8mNF-sQpRIrIFb08MSChk'

# # Establish connection
# conn = st.experimental_connection("gsheets", type=GSheetsConnection, spreadsheet=SPREADSHEET_ID)

# # Read data from the specified worksheet
# existing_data = conn.read(worksheet='collected_data', usecols=list(range(3)))
# existing_data = existing_data.dropna(how='all')

# st.dataframe(existing_data)

# Function to calculate the user type based on the score
def calculate_user_type(score):
    if score <= 5:
        return "Type A", "Description: ........."
    elif score <= 10:
        return "Type B", "Description: ........."
    elif score <= 15:
        return "Type C", "Description: ........."
    else:
        return "Type D", "Description: ........."

# Title of the web app
st.title("Find your type")

# Description
st.write("Answer the following questions to find out what type of person you are. Each question has four options, and each option carries a different score. Your total score will determine your type.")

# Input field for user's name
user_name = st.text_input("Please enter your name:")

# Ensure the user has entered a name before proceeding
if user_name:
    # Questions and answers with their respective scores
    questions = [
        {"question": "What is your favorite color?",
         "answers": {"Red": 1, "Blue": 2, "Green": 3, "Yellow": 4}},
        
        {"question": "What is your favorite animal?",
         "answers": {"Cat": 1, "Dog": 2, "Bird": 3, "Fish": 4}},
        
        {"question": "What is your favorite season?",
         "answers": {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}},
        
        {"question": "What is your favorite food?",
         "answers": {"Pizza": 1, "Burger": 2, "Sushi": 3, "Salad": 4}},
        
        {"question": "What is your favorite hobby?",
         "answers": {"Reading": 1, "Traveling": 2, "Sports": 3, "Gaming": 4}},
    ]

    # Manage session state for initialization, resetting, and rerunning
    if 'init' not in st.session_state:
        st.session_state.init = True
        st.session_state.scores = [None] * len(questions)
        st.session_state.re_run_key = 0  # Initialize rerun key

    # Iterate through questions and create radio buttons for each question
    for i, q in enumerate(questions):
        key = q["question"] + str(i) + "_" + str(st.session_state.re_run_key)  # Append rerun key to each question key
        answer = st.radio(q["question"], options=list(q["answers"].keys()), index=None, key=key)
        st.session_state.scores[i] = q["answers"].get(answer, None)

    submit = st.button("Submit")
    restart = st.button("Restart")

    # Submit functionality
    if submit:
        if None in st.session_state.scores:
            st.error("Please answer all questions.")
        else:
            # Calculate the total score
            total_score = sum(st.session_state.scores)
            
            # Determine the user type based on the combined score
            user_type, description = calculate_user_type(total_score)
            
            # Display the total score and user type on separate lines
            st.write(f"Your total score is: {total_score}")
            st.write(f"Your type is: {user_type}")
            st.write(description)

            # # Add result to Google Sheet
            # submit_data = pd.DataFrame(
            #     [
            #         {
            #             'Name': user_name,
            #             'Score': total_score,
            #             'Type': user_type
            #         }
            #     ]
            # )

            # updated_df = pd.concat([existing_data, submit_data], ignore_index=True)
            # conn.update(worksheet='collected_data', data=updated_df)

    # Restart functionality
    if restart:
        st.session_state.re_run_key += 1  # Increment rerun key to change the state keys
        st.session_state.scores = [None] * len(questions)  # Reset scores
        st.rerun()  # Use this to rerun the app and reset all inputs

else:
    st.write("Please enter your name to start the test.")
