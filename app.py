import csv
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_shortcuts import button, add_keyboard_shortcuts

import data_cleaning as dc

st.title("CVP Application Review App")

st.markdown(
    """ 
    This app is made to make the CVP application review easier to review with it's large pool of applicants

    Shortcuts:
    - Up Arrow and Down Arrow takes you to the previous/next applicant respectively
    - Left Arrow and Right Arrow takes you between tabs on an applicant's response (after an initial click)
    - Use the Input Index field below to jump to a particular applicant's index

    If there are any issues with the app, reach me at jeremym3817@gmail.com 
    """
)

# Initialize session state for index
if 'index' not in st.session_state:
    st.session_state.index = 0

if 'input_index' not in st.session_state:
    st.session_state.input_index = ""

def reset_index():
    st.session_state.input_index = st.session_state.user_index
    st.session_state.user_index = ""

def get_index():
    try:
        user_index = int(st.session_state.user_index) 
        if 1 <= user_index < len(dc.df_CSCE_data): 
            st.session_state.index = user_index - 1
        else:
            st.warning("Index out of range. Please enter a valid index.")
    except ValueError:
        st.warning("Invalid input. Please enter a numeric index.")
    reset_index()
        
# Callback functions to update index
def next_application():
    if st.session_state.index < len(dc.df_CSCE_data) - 1:
        st.session_state.index += 1

def last_application():
    if st.session_state.index > 0:
        st.session_state.index -= 1

def map_applications():
    # initialize fields
    df_offset = 4
    i = st.session_state.index

    user_branch_1 = dc.df_CSCE_data.loc[i, 'First Choice (confirmed)']
    
    # TODO: Get actual branch because people change their original choice 
    #user_branch_2 = dc.df_CSCE_data.loc[i, 'Second Choice']
    # this try-except is sketchy check for future bugs here
    #try:
    user_branch_2 = dc.df_CSCE_data.loc[i, 'Second Choice']
    #except:
     #   user_branch_2 = dc.df_CSCE_data.loc[i, 'Second Choice']

    user_branch_list = [user_branch_1, user_branch_2]
    user_dataframe_offset = []
    applicant_title = dc.df_contact_data.loc[i, 'Name']
    site_data_list = []

    try:
        for j in range(len(user_branch_list)):
            site_quals = dc.site_dict[user_branch_list[j].lower()] # get branch dict values 
            q_range = site_quals[1] + df_offset # get the offset to move to correct part of dataframe
            user_dataframe_offset.append([q_range, q_range + site_quals[3]]) # get correct offset for each site branch

            applicant_title += f" | Choice #{j + 1}: {user_branch_list[j]}" # append to applicant title

            cur_data = dc.df_cleaned.iloc[i, user_dataframe_offset[j][0]:user_dataframe_offset[j][1]]
            site_data_list.append(cur_data)

            try:
                user_branch_list[j + 1] = cur_data.iloc[-1]
                #st.write(user_branch_list[j + 1])
            except:
                #user_branch_list[1] = dc.df_CSCE_data.loc[i, 'Second Choice']
                continue
    except:
        st.write(f"Application {i + 1} of {len(dc.df_CSCE_data)}")
        st.write(dc.df_contact_data.loc[i, 'Name'], " | ", user_branch_1)
        st.write("This application's site is at ", user_branch_1, " which is out of the bounds of this program. Please look at this manually.")
        return pd.DataFrame({}), pd.DataFrame({}), pd.DataFrame({})    

    st.write(f"Application {i + 1} of {len(dc.df_CSCE_data)}")

    st.write(applicant_title)

    contact_data = dc.df_contact_data.loc[i, :]
 
    return contact_data, site_data_list[0], site_data_list[1]



# Create an input field and store value in session state
st.text_input("Input Index: ", placeholder="Insert Index Here", label_visibility='collapsed', key="user_index", on_change=get_index) 

contact_data, site_data_1, site_data_2 = map_applications()

tabs = st.tabs(['Contact Info', 'First Choice', 'Second Choice'])
data = [contact_data, site_data_1, site_data_2]

tabs[0].dataframe(data[0], use_container_width=True)
try:
    for i in range(1, 3):
        tabs[i].dataframe(data[i], use_container_width=True)
        tabs[i].write("What skills or previous experience do you have that will make you an effective volunteer with this site?")
        tabs[i].write(data[i].iloc[1])
        tabs[i].write("Notes about time selections and preferences (optional)")
        tabs[i].write(data[i].iloc[2])
except:
    st.write("There seems to be a problem loading this data. Please look at it manually or contact support.")

last, next = st.columns(2)

with last:
    button("Last", 'ArrowDown', key="last", on_click=last_application)

with next:
    button("Next", 'ArrowUp', key="next", on_click=next_application)

