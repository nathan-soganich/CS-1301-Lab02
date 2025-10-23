# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import csv
import json
import random

import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Study Hours Data Collection Survey📝")
st.write("Please fill out the form below to the best of your abilities.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
hours = []
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
table_headers = ('Day of the Week', 'Hours Spent Studying')
data_list=[]

with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    hours.append(st.text_input("How many hours do you spend studying on a Monday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Tuesday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Wednesday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Thursday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Friday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Saturday?"))
    hours.append(st.text_input("How many hours do you spend studying on a Sunday?"))

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    
    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # Prepare the data as a list
        for i in range(len(days_of_week)):
            data_list.append({table_headers[0] : days_of_week[i],table_headers[1] :hours[i]})
        file_exists = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0
        st.success("Data saved successfully!")
        with open('data.csv', 'a', newline = "")as data:
            writer = csv.DictWriter(data, fieldnames = table_headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data_list)

        
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        
        st.success("Your data has been submitted!")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        # Read the CSV file into a pandas DataFrame.
        current_data_df = pd.read_csv('data.csv')
        
        # Check if dataframe is empty
        if current_data_df.empty:
            st.warning("The CSV file has no data rows yet.")
        else:
            # Display the DataFrame as a table.
            st.dataframe(current_data_df)
            st.success(f"Displaying {len(current_data_df)} rows of data")
            
    except pd.errors.EmptyDataError:
        st.error("The CSV file is empty or malformed. Please submit the survey to create new data!")
        
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.info("Try deleting the data.csv file and submitting the form again.")
else:
    st.warning("The 'data.csv' file is empty or does not exist yet. Submit the form above to create it!")

