# udemy-rip
Scraped contents of 6 practice exams from paid [Udemy course](https://www.udemy.com/course/aws-certified-cloud-practitioner-practice-exams-c/). Each exam folder contains 3 files: readable txt file of questions, json file of questions (should you want to access the questions in a common data structure), html answer key. The answer keys have lost their formatting, so it takes a little extra effort to read them.


## Methodology
1. Manually log in to Udemy and get to first page (question) of practice exam
2. run script that will  
  i. iterate through and download questions as html files  
  ii. iterate through downloaded html files and scrape out questions and choices  
  iii. create json file of questions and choices plus readable version (txt)  
3. Manually download answers to questions as a single file

## Notes
- Could not directly scrape off Udemy as requests were flagged as bot activity
- Did not scrape off answer HTML files because did not see a way to distinguish breaks between sets of answer choices since not all questions have same number of choices
  - After further thought, this can probably be done by performing simple regex on question text (see if it contains "Select Two")
    - this would eliminate need for mouse and keyboard automation to download questions one by one
- Answer html files lost their formatting when downloaded
  - Further work could be done to scrape explanations and correct answers but did not seem worth the effort
