import streamlit as st
import pandas as pd
import os
from generate_html_map import generate_html_map

def main():
    # Set the page configuration
    st.set_page_config(APP_TITLE, layout='wide')
    
    # Add CSS for background color and custom styling
    st.markdown(
        """
        <style>
        .reportview-container .main {
            background-color: #d3dadd;
        }
        .sidebar .sidebar-content {
            background-color: #2e2e2e;
        }
        .stApp {
            padding: 0 !important;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        .header img {
            width: 150px;
            margin-top: 0px;  /* Adjust this value as needed */
        }
        .header h1 {
            margin-left: 20px;
            margin-bottom: 0;
        }
        .header p {
            margin-left: 20px;
            margin-top: 0;
            font-size: 18px;
        }
        .no-results-popup {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            color: black;  /* Set text color to black */
            padding: 20px;
            border: 2px solid black;
            z-index: 9999;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the logo and title in a horizontal layout
    st.markdown(
        """
        <div class="header">
            <img src="https://i.imgur.com/U5vCbok.png" alt="YNG Logo"/>
            <div>
                <h1>Pacific US Engagement Map</h1>
                <p>NOTE: ALL USER DATA BELOW IS RANDOMLY GENERATED AND NOT REAL!</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar filters
    st.sidebar.title("Filters")
    chapter = st.sidebar.selectbox('Chapter', chapter_list)
    interest = st.sidebar.selectbox('Interest', interest_list)
    industry = st.sidebar.selectbox('Industry', industry_list)

    # Generate and display the map
    data_found = generate_html_map(df, 'data/yng_map.html', chapter_filter=chapter, interest_filter=interest, industry_filter=industry)
    st.components.v1.html(open('data/yng_map.html').read(), height=600, scrolling=False)

    if not data_found:
        st.markdown(
            """
            <div class="no-results-popup">
                Sorry, we didn't find anything that matches your criteria.
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('data/geocoded_yng_members.csv', dtype={'Zip Code': str})

    # Define the constants
    APP_TITLE = 'YNG Pacific US Engagement Map'
    APP_SUB_TITLE = 'Connecting YNG Members'
    
    # Get the list of chapters
    chapter_list = ['Pacific US Region'] + list(df['Chapter Affiliation'].unique())
    chapter_list.sort()

    # Get the list of interests
    interest_list = ['Any'] + list(set([interest for sublist in df['Interests'].str.split(', ') for interest in sublist]))
    interest_list.sort()

    # Get the list of industries
    industry_list = ['Any'] + list(df['Industry'].unique())
    industry_list.sort()

    main()
