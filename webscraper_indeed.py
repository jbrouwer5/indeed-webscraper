import requests
from bs4 import BeautifulSoup
# By Jackson Brouwer
# Scapes job postings from Indeed.com

# developer notes
# indeed url -> https://www.indeed.com/
# indeed when searching for keyword python ->
# https://www.indeed.com/jobs?q=python&l=&vjk=87e4c9af8163f702
# indeed when searching for keyword python job in chicago ->
# https://www.indeed.com/jobs?q=python&l=Chicago%2C+IL&vjk=87e4c9af8163f702
# URL can be broken down into
# URL = https://www.indeed.com/jobs?q= + JOB + &l= + CITY + %2C+ STATE + &vjk=87e4c9af8163f702
# where spaces in JOB and CITY are replaced by +
# for example, python developer = python+developer, New York = New+York
# states should be given as two letter abbreviations

# returns the 15 most relevant jobs in indeed.com matching the search
# each job shows title, company, and location


def indeed_scraper():
    results = None
    while results == None:
        # asks for job input and stores in job variable
        print("Input the job that you are looking for!")
        job = input()

        # job input string modifications
        # final result must be lower case words separated by '+'
        job.lower()

        # replaces spaces with '+'
        job = job.split(" ")
        job_len = len(job)
        temp = job
        job = ""
        for i in range(job_len-1):
            job += temp[i]
            job += "+"
        job += temp[job_len-1]

        # asks for city input and stores in city variable
        print("Input the city in which you are job searching.")
        city = input()

        # city input string modifications
        city.lower()
        city[0].upper()

        is_abbrev = False
        while not is_abbrev:
            print(
                "Input the two letter abbreviation of the state the city is located in.")
            state = input()
            if len(state) == 2:
                is_abbrev = True

        state.upper()

        # URL = https://www.indeed.com/jobs?q= + JOB + &l= + CITY + %2C+ STATE + &vjk=87e4c9af8163f702
        URL = "https://www.indeed.com/jobs?q=" + job + \
            "&l=" + city + "%2C+" + state + "&vjk=261a6748688d29d6"

        # gets API data from indeed.com
        page = requests.get(URL)

        # starts html parsing
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="mosaic-provider-jobcards")

        if results == None:
            print("One of the inputs could not be found. Please try again")

    python_jobs = results.find_all(
        "div", "job_seen_beacon"
    )

    python_job_elements = [
        h2_element for h2_element in python_jobs
    ]

    job_count = 0
    print("\nThe relevant jobs are:\n\n")
    for job_element in python_job_elements:
        # finds html element with title, company, and job
        title_element = job_element.find("h2", class_="jobTitle")
        company_element = job_element.find("span", class_="companyName")
        location_element = job_element.find("div", class_="companyLocation")

        # if elements were found print them together
        if title_element != None and company_element != None and location_element != None:
            print(title_element.text.strip())
            print(company_element.text.strip())
            print(location_element.text.strip())
            job_count += 1

        print()

    print(str(job_count) + " total jobs were found!")


indeed_scraper()
