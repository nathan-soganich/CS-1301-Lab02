# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st
import json
import random

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to the Data Dashboard! 📊")

# INTRODUCTORY TEXT
st.write("""
This application is designed to collect and visualize data.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey Page**: Go here to input new data into our CSV file.
- **Visuals Page**: Go here to see the data visualized in different graphs.

This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
#writing to my json file in this because i want random data
data2 = {
    "title": "Study Hours vs Test Scores",
    "description": "Random dataset showing relationship between study time and exam performance",
    "data_points": []
}
for i in range(50):
    study_hours = round(random.uniform(0, 10), 1)  # 0-10 hours
    # Test score has some correlation with study hours plus random noise
    base_score = study_hours * 7 + 30  # Base relationship
    noise = random.uniform(-15, 15)  # Add randomness
    test_score = round(min(100, max(0, base_score + noise)), 1)  # Keep between 0-100
    
    data2["data_points"].append({
        "student_id": i + 1,
        "study_hours": study_hours,
        "test_score": test_score
    })

# Save to JSON file
with open('data.json', 'w') as file:
    json.dump(data2, file, indent=4)
