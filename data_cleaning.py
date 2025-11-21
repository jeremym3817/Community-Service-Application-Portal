import csv
import pandas as pd
import numpy as np
import streamlit as st

pd.set_option('display.max_columns', None)

file_path = "C:/Users/Jerem/Downloads/CVP_Application_Spring_2025.csv"
cleaned_file_path = "C:/Users/Jerem/OneDrive/Python-Projects/CVP_Application_App/CVP_Application_Spring_2025_cleaned.csv"

# Read and clean the CSV while preserving embedded newlines and special characters
with open(file_path, 'r', encoding='ISO-8859-1', errors='ignore', newline='') as infile, \
     open(cleaned_file_path, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.reader(infile, delimiter=',', quotechar='"')
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for row in reader:
        cleaned_row = [cell.replace('\n', ' ').replace('\r', ' ') if isinstance(cell, str) else cell for cell in row]
        writer.writerow(cleaned_row)

# Load the cleaned CSV into pandas
df_cleaned = pd.read_csv(
    cleaned_file_path,
    encoding='utf-8',
    quotechar='"',
    escapechar='\\',
    engine='python'
)

# Preview the cleaned DataFrame
#df_cleaned.head()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

df_contact_data = df_cleaned[['Email', 'Name', 'Preferred Pronouns', 'Are you an undergraduate or graduate student?', 'Major(s)',
                              'Expected Year of Graduation', 'Language(s) Spoken', 'Phone Number']]

#print(df_contact_data.head())   

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

df_CSCE_data = df_cleaned[['Have you participated in any of the following CSCE programs in the past?',
                           'Are there any reasons you may have for not being able to commit to a full semester of CVP?\xa0',
                           'Please describe your reasons. What other commitments do you have this semester? (examples include clubs, sports, and academic or class conflicts)',
                           'Are there any volunteer tasks you are not able to do or would need special accommodations for?',
                           'Please specify these tasks or special accommodations.\xa0',
                           'What are you hoping to gain from participating in CVP?\xa0',
                           "Briefly describe any previous experience you've had with volunteering.",
                           'What organization would you like to volunteer with? Please note the sites in red are no longer accepting applications. If you choose those sites, your application will not be considered!\xa0',
                           'What would your secondary preferred site be?\xa0',
                           'Please select your FIRST preferred site again, to take you to that section of the application. Please note the sites in red are no longer accepting applications. If you choose those sites, your applic']]

df_CSCE_data.columns = ['Returning to CSCE', "Can't do Full Semester", "Why Can't do Full Semester",
                'Accommodations', "What are Accommodations", 'Why CVP', 'Experience', 'First Choice', 'Second Choice', 'First Choice (confirmed)']
#df_CSCE_data.head()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This is where the current Site list should go
current_sites = ['Community Servings', '826 Boston*', 'Boston Building Resources', 'Boston Outdoor Preschool Network*',
                 'Boy With A Ball', 'Roxbury Tenants of Harvard*^', 'Artists for Humanity*^', 'Little Brothers Friends of the Elderly*',
                 'Hyde Square Task Force*^', 'Thrifty Threads', 'Camp Harbor View*', 'EVkids*', 'Boys & Girls Clubs of Boston: Orchard Gardens Club*^',
                 'Link Health', 'No secondary site/Finished application']
current_sites = [s.lower() for s in current_sites]
# This is where each site's corresponding first question goes (-1 is for no secondary site)
sites_index = [19, 23, 29, 33, 39, 43, 49, 55, 62, 68, 72, 78, 84, 90, 94, -1]
# This is where we determine whether a site is CORI/SORI or not
sites_CORI_SORI = []
# This is where we determine how many questions a site has
sites_n_of_questions = []
# This is where we determine whether a site is only open to US Citizens
sites_US_only = []

for i in range(len(current_sites)):
    if '*' in current_sites[i]:
        sites_CORI_SORI.append(True)
        sites_n_of_questions.append(6)
    else:
        sites_CORI_SORI.append(False)
        sites_n_of_questions.append(4)

    if '^' in current_sites[i]:
        sites_US_only.append(True)
    else:
        sites_US_only.append(False)

site_dict = {}
for i in range(len(current_sites)):
    site_dict[current_sites[i]] = [i, sites_index[i], sites_CORI_SORI[i], sites_n_of_questions[i], sites_US_only[i]]

# number of questions edge cases
site_dict['little brothers friends of the elderly*'][3] = 7

#print(site_dict)