# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json 
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

st.info("TODO: Add your data loading logic here.")
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    try:
        survey_df = pd.read_csv('data.csv')
        st.dataframe(survey_df)
        st.success(f"Loaded {len(survey_df)} rows from CSV!")
        
    except pd.errors.EmptyDataError:
        st.warning("The CSV file is empty!")
        survey_df = None
        
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        survey_df = None
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
    survey_df = None

# Load JSON data
st.subheader("JSON Data (Study Hours vs Test Scores)")
if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
    try:
        with open('data.json', 'r') as file:
            json_data = json.load(file)
        

        json_df = pd.DataFrame(json_data['data_points'])
        st.dataframe(json_df.head(10))  # Show first 10 rows
        st.success(f"Loaded {len(json_df)} data points from JSON!")
        
    except json.JSONDecodeError:
        st.error("The JSON file is malformed!")
        json_df = None
        
    except Exception as e:
        st.error(f"Error reading JSON: {e}")
        json_df = None
else:
    st.warning("The 'data.json' file is empty or does not exist yet.")
    json_df = None
st.divider()
st.header("Graphs")
# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.



# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Hours Studied vs. Test Score") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
st.line_chart(json_df, x= 'study_hours', y = 'test_score')
st.write("This graph shows randomly generated data associating hours studied with test scores, stored in  JSON file and shown as a graph in stremlit")


# GRAPH 2: DYNAMIC GRAPH
 # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.s     ession_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

st.subheader("Graph 2: Study Hours by Day (Dynamic View)")

if survey_df is not None and not survey_df.empty:
    
    # Check if the required columns exist
    if 'Hours Spent Studying' not in survey_df.columns:
        st.error("The CSV file doesn't have the expected columns. Please submit the survey first!")
        st.write("Current columns in CSV:", list(survey_df.columns))
    else:
        # Convert to numeric
        survey_df['Hours Spent Studying'] = pd.to_numeric(survey_df['Hours Spent Studying'], errors='coerce')    
    # Initialize session state for view type #NEW
    if 'view_type' not in st.session_state: #NEW
        st.session_state.view_type = "Average"
    
    # Radio button to choose view type #NEW
    view_type = st.radio( #NEW
        "Choose view:",
        options=["Average", "Total", "Count"],
        horizontal=True,
        key='view_selector'
    )
    
    st.session_state.view_type = view_type
    
    # Calculate based on selection
    if view_type == "Average":
        data_by_day = survey_df.groupby('Day of the Week')['Hours Spent Studying'].mean()
        label = "Average Hours"
    elif view_type == "Total":
        data_by_day = survey_df.groupby('Day of the Week')['Hours Spent Studying'].sum()
        label = "Total Hours"
    else:  # Count
        data_by_day = survey_df.groupby('Day of the Week').size()
        label = "Number of Entries"
    
    # Reorder by day
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data_by_day = data_by_day.reindex(day_order)
    
    # Display chart
    st.write(f"**{label} by Day of Week**")
    st.bar_chart(data_by_day)
    
    # Show summary
    st.info(f"**{label} across all days:** {data_by_day.sum():.2f}")
    
else:
    st.warning("No CSV data available!")
st.write("This graph takes the data appended to the data csv file appended every time someone submits the survey. if there is no graph displaying, ensure you have completed the survey. You can select boxes to then choose to display the average hours spent studying any day of the week or totals")



st.subheader("Graph 3: Interactive Quadratic Function")
st.write("""
This interactive graph allows you to create custom quadratic functions by adjusting three coefficient sliders (a, b, and c) that control the shape, tilt, and position of the parabola. Use the sliders to change the values and watch how the equation y = ax² + bx + c transforms in real-time, with the vertex (turning point) calculated automatically below the graph.
""")
st.write("""
Use the three sliders below to adjust the coefficients of a quadratic equation and see how the parabola changes shape in real-time. The coefficient 'a' controls the curve's steepness, 'b' controls the tilt, and 'c' moves it up or down.
""")
# Initialize session state #NEW
if 'a_coef' not in st.session_state:
    st.session_state.a_coef = 1.0
if 'b_coef' not in st.session_state:
    st.session_state.b_coef = 0.0
if 'c_coef' not in st.session_state:
    st.session_state.c_coef = 0.0

# Use sliders for coefficients #NEW
a = st.slider( #NEW
    "Coefficient a (x²):",
    min_value=-5.0,
    max_value=5.0,
    value=st.session_state.a_coef,
    step=0.1,
    key='slider_a'
)

b = st.slider(
    "Coefficient b (x):",
    min_value=-10.0,
    max_value=10.0,
    value=st.session_state.b_coef,
    step=0.5,
    key='slider_b'
)

c = st.slider(
    "Coefficient c (constant):",
    min_value=-20.0,
    max_value=100.0,
    value=st.session_state.c_coef,
    step=1.0,
    key='slider_c'
)

# Update session state
st.session_state.a_coef = a
st.session_state.b_coef = b
st.session_state.c_coef = c

# Display equation
st.latex(f"y = {a}x^2 + {b}x + {c}") #NEW

# Generate data points
import numpy as np
x = np.linspace(-10, 10, 200)
y = a * x**2 + b * x + c

quad_df = pd.DataFrame({
    'x': x,
    'y': y
})

# Create DataFrame
try:
    quad_df.to_csv('quadratic_data.csv', index=False)
except Exception as e:
    st.error(f"Error saving to CSV: {e}")

# READ FROM CSV FILE AND PLOT
try:
    # Read the data back from CSV
    plotted_data = pd.read_csv('quadratic_data.csv')
    
    # Plot using line chart
    st.line_chart(plotted_data.set_index('x'))
    
    st.info(f"📊 Plotted {len(plotted_data)} data points from CSV file")
    
except Exception as e:
    st.error(f"Error reading CSV for plotting: {e}")

# Calculate vertex
if a != 0:
    vertex_x = -b / (2 * a)
    vertex_y = a * vertex_x**2 + b * vertex_x + c
    st.write(f"**Vertex:** ({vertex_x:.2f}, {vertex_y:.2f})")

# GRAPH 3: DYNAMIC GRAPH
 # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

