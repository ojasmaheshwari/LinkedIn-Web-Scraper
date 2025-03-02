# %% [markdown]
# ### Imports

# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import logging
import traceback

# %% [markdown]
# ### Load profiles from excel sheet

# %%
# Read excel file for linkedin profile urls
dataframe = pd.read_excel('Assignment.xlsx')
rows = len(dataframe)

profiles = []
for i in range(rows):
    profile_url = dataframe.iloc[i]['LinkedIn URLs']
    profiles.append(profile_url)


# %% [markdown]
# ### Open an output csv file to push results into

# %%
csv_file = open('Scraped_profiles.csv', mode='a', newline='')
column_names = ["LinkedIn URL", "Name", "Bio", "Experience", "Education"]
writer = csv.DictWriter(csv_file, fieldnames=column_names)
writer.writeheader()

# %% [markdown]
# ### Initialize driver

# %%
cService = webdriver.ChromeService(executable_path='chromedriver')
driver = webdriver.Chrome(service = cService)

# %% [markdown]
# ### Account email and password for login

# %%
user_email = "YOUR_LINKEDIN_EMAIL_HERE"
user_password = "YOUR_LINKEDIN_PASSWORD_HERE"

# %% [markdown]
# ### Login to LinkedIn

# %%
# Login to LinkedIn
driver.get("https://linkedin.com/login")
username_input_elem = driver.find_element(By.ID, "username")
password_input_elem = driver.find_element(By.ID, "password")
username_input_elem.send_keys(user_email)
password_input_elem.send_keys(user_password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# %% [markdown]
# ### Main loop to scrape profiles

# %%
for profile_url in profiles:
    try:
        # Load profile page
        driver.get(profile_url)

        # Scroll to the bottom of the page
        start = time.time()
        initialScroll = 0
        finalScroll = 1000
        scrollTime = 10
        while True:
            driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000
            time.sleep(3)
            end = time.time()
            if round(end - start) > scrollTime:
                break

        # Get source code and parse it
        source_code = driver.page_source
        soup = BeautifulSoup(source_code, 'lxml')

        # Scrape fullname and bio
        intro_elem = soup.find('div', {'class': 'POxtDRifotsubMPVakmTWlMDSDIbH'})
        if not intro_elem:
            # This is likely not a profile page or the profile does not exist so continue
            print("No profile found for url: " + profile_url)
            continue

        fullname = intro_elem.find('h1', {'class': 'JtDmvATzwQtgDgNLDeDrrAGfeaVHRqsTx'}).getText()
        bio = intro_elem.find_all()[-1].getText().strip()
        if not bio:
            # If the user does not have a bio then set it to NA
            # I am suspicious a user without a bio exists but for the safe side
            bio = 'NA'

        # Categorize sections into experience section and education section in order to scrape them separately
        sections = soup.find_all('section', {'class' : 'artdeco-card pv-profile-card break-words mt2'})
        if not sections:
            # If a user does not have any sections on his profile page which I again am suspicious of
            writer.writerow({
                "LinkedIn URL" : profile_url,
                "Name" : fullname,
                "Bio" : bio,
                "Experience" : "NA",
                "Education" : "NA"
            })
            csv_file.flush()
            continue;
        
        global experiences
        global education
        for section in sections:
            if section.find('div', {'id' : 'experience'}):
                experiences = section
            elif section.find('div', {'id' : 'education'}):
                education = section

        # Scrape experiences
        experience_data = []
        if experiences:
            companies = experiences.find_all('div', {'class' : 'zSLireyqsWFZsKhRrJCPCIfVadBWViQ hvLOkFrYLvhhSPwCmWgiLpqjsfYlJkRQOMo PMuJZoDTtpXHdyfOGwaTHubPatVxRtab'})

            for company in companies:
                company_name = company.find('div', {'class' : 'display-flex flex-wrap align-items-center full-height'})
                company_name = company_name.find('span', {'class' : 'visually-hidden'})
                company_name = company_name.getText().strip()

                roles_list = []

                # Check if company name is given in description, in which case reverse how we store the object
                additional_info = company.find('span', {'class' : 't-14 t-normal'})
                if (additional_info):
                    additional_info = additional_info.find('span', {'class' : 'visually-hidden'})
                    additional_info = additional_info.getText().strip()
                    role, company_name = company_name, additional_info
                    experience_data.append({
                        company_name : [role]
                    })
                else:
                    roles = company.find('ul', {'class' : 'SCMYUuIWSpttAlXtxktgkPZIFJQMwugqGHJMPqM'})
                    if roles:
                        roles = roles.find_all('div', {'class' : 'display-flex flex-column align-self-center flex-grow-1'})
                        for role in roles:
                            role = role.find('div', {'class' : 'display-flex align-items-center mr1 hoverable-link-text t-bold'})
                            role = role.find('span', {'class' : 'visually-hidden'})
                            role = role.getText().strip()
                            roles_list.append(role)
                
                    experience_data.append({
                        company_name : roles_list
                    })

        # Scrape education history
        education_data = []
        if education:
            institutes = education.find_all('div', {'class' : 'zSLireyqsWFZsKhRrJCPCIfVadBWViQ hvLOkFrYLvhhSPwCmWgiLpqjsfYlJkRQOMo PMuJZoDTtpXHdyfOGwaTHubPatVxRtab'})

            for institute in institutes:
                institute_name = institute.find('div', {'class' : 'display-flex flex-wrap align-items-center full-height'})
                institute_name = institute_name.find('span', {'class' : 'visually-hidden'})
                institute_name = institute_name.getText().strip()

                degree = institute.find('span', {'class' : 't-14 t-normal'})
                if (degree):
                    degree = degree.find('span', {'class' : 'visually-hidden'})
                    degree = degree.getText().strip()
                else:
                    degree = 'NA'
                    
                education_data.append({
                    institute_name : degree 
                })

        # Write output into CSV file
        writer.writerow({
            "LinkedIn URL" : profile_url,
            "Name" : fullname,
            "Bio" : bio,
            "Experience" : experience_data,
            "Education" : education_data
        })
        csv_file.flush()

        print(fullname)
    except Exception as e:
        logging.error(traceback.format_exc())

# %% [markdown]
# ### Clean up

# %%
print("SUCCESSFULLY SCRAPED ALL PROFILES! CRAZY HOW YOU DIDN'T GET BANNED")
# Clean up
csv_file.close()


