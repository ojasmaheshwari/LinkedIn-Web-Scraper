# How to use
- Ensure you have python installed on your system.
- Simply run `pip install -r requirements.txt` to install all dependencies and packages.
- Edit "main.py" or "main.ipynb" file and replace `user_email` and `user_password` with your linkedin email and password.
- Edit "main.py" or "main.ipynb" file and replace `Assignment.xlsx` in `Load profiles from excel sheet` section with the path to your input sheet.
- Do "python main.py" or run all code from .ipynb file.
- If you get an error regarding `chromedriver` having a different version from chrome installed on your system then find the correct version of chromedriver for your chrome on the internet and download it. Place it in project root.

# It can scrape the following data
- Full name as a string
- Bio as a string
- Experiences as an array of objects
- Education history as an array of objects

# Requirement it does not satisfy
- Scraping socials
    - I could not scrape socials simply because I could not find where the socials were present in a user's LinkedIn page. If you let me know where the socials are present, I can scrape that data easily too.
- I was only able to scrape like 23 profiles because then I got restricted by LinkedIn. I was not able to scrape all 50 profile links given in sheet. Though you can do that by making a new LinkedIn account and making use of a VPN.

# Development Process and My Thoughts
Web scraping is actually pretty straightforward. While you can't just extract an information in one find command, you have to keep digging down and use multiple find queries to get to your data.
Initially I thought of not using Selenium and just using requests module so I won't have to simulate a browser. But there were some obvious problems. The main problem being that I just could not get dynamically created html which was 
handled by javascript. So I had to use Selenium. The rest of the process was straightforward once I understood how web scraping was actually done. It is just a little tedious but straight-forward process.
