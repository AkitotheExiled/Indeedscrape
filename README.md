# Indeedscraper

## Prereqs
>beautifulsoup4==4.7.1

numpy==1.16.2

pandas==0.24.2

python-dateutil==2.8.0

pytz==2019.1

selenium==3.141.0

six==1.12.0

soupsieve==1.9.1

urllib3==1.24.1

## Webdriver
I am currently using:
> Firefox Driver

## TODO
- [ ] Implement BS4 to allow extraction of job: description, salary, links
- [ ] Fix issue where column headers appear at the bottom of the file if you append jobs to an already create file
- [ ] Fix issue where appending jobs to a file introduces an additional row between each job
- [ ] Fix issue where elementnotinteracted trace can appear(possibly due to clicking on an nonexistent body of the page)
- [ ] Develop a function to scrape more than one page and allow users to customize the amount of pages
- [ ] Figure out a solution to where if the search parameters results in no jobs appearing
- [ ] Create a function to handle job duplicates before appending results to the file
- [ ] Eventually add functionality to sort the jobs by "type" using Python
