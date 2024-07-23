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
            margin-top: 20px;  /* Adjust this value as needed */
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
                <h1>YNG Pacific US Engagement Map</h1>
                <p>Connecting YNG Members</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar filters
    st.sidebar.title("Filters")
    chapter = st.sidebar.selectbox('Chapter', chapter_list)
    if chapter:
        zip_code_list = [''] + list(df[df['Chapter Affiliation'] == chapter]['Zip Code'].unique())
    else:
        zip_code_list = [''] + list(df['Zip Code'].unique())
    zip_code_list.sort()
    zip_code = st.sidebar.selectbox('Zip Code', zip_code_list)

    # Generate and display the map
    generate_html_map(df, 'data/yng_map.html', chapter_filter=chapter, zip_code_filter=zip_code)
    st.components.v1.html(open('data/yng_map.html').read(), height=600, scrolling=False)

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('data/geocoded_yng_members.csv', dtype={'Zip Code': str})

    # Define the constants
    APP_TITLE = 'YNG Pacific US Engagement Map'
    APP_SUB_TITLE = 'Connecting YNG Members'
    
    # Get the list of chapters
    chapter_list = [''] + list(df['Chapter Affiliation'].unique())
    chapter_list.sort()

    main()
