# Brave Career Mini Challenge
### Web Scraper for Visitor Classification
The goal of this challenge was to build a tool that takes a URL as input, scrapes the site's content, and generates questions using artificial intelligence to classify its visitors.

My solution is a full-stack app that will scrape a given site using Selenium, and use key insights to prompt ChatGPT for survey questions.
The backend (found at [/amplify/backend/api/flask/src/](https://github.com/Bdeering1/brave-career-challenge/tree/main/amplify/backend/api/flask/src)) and database can be easily spun-up with docker, and are fully configured for hosting on AWS Amplify.

### Solution Stack
**Front End**: Typescript, React, Redux, Tailwind CSS \
**Back End**: Python, Flask, Selenium, Docker \
**Database**: PostgreSQL \
**Hosting**: Amazon Web Services
