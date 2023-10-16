# in_and_out
A data analysis demo using IoT data

### The definition of the problem
There is an office with 25 registered employees. The office has a keycard entrance system that registers the entry and exit time for each individual employee. Te data produced by the system is of the form:

> user_id,event_type,event_time

where, the event type can be either denote entry or exit, and event time when the action took place.

The data come as a csv file.

### Questions:
1. For each employee, for the month of February, calculate the following:
    - total_time_in_office: the net amount of hours spent in the office.
    - unique_days_in_office: the number of unique calendar days the employee was present in the office.
    - average_employee_time_per_day: the total time spent in the office divided by the unique days the employee was present in the office.
    - employee_ranking_average_time: the ranking of the employees along average time per day spent in the office.

2. Which employee had the longest work session in February?

    From the first entry to the last exit, each entry and exit form a chain. If there are more than two (2) hours between an exit and the next entry, then the session has ended. For example, either when leaving the office in the evening and returning next morning, or whenever during the day when a break from the office is for more that two hours, a session has ended

    eg, IN 8, OUT 12, IN 13, OUT 18, (IN next day) this counts as one session from 8 to 18

    eg. IN 8, OUT 12, IN 15, OUT 18, (IN next day) these count as two sessions from 8 to 12 and from 15 to 18

3. (Optional) From the perspective of the office, assuming that the 25 registered employees denote the maximum capacity, how many people joined the office every day? Report the weekday, and the daily min_presence, median_presence, and max_presence in the office for every of the seven (7) weekdays.

4. From the perspective of the office, what was the maximum number of employees that joined the office every day, for each hourly band between 07:00 and 22:00?  Report the weekday, the hourly bands, and the max presence in the office for every of the seven (7) weekdays.

### Deliverables:
1. For question 1, return a CSV file with user_id, total_time_in_office, unique_days_in_office, average_employee_time_per_day, employee_ranking_average_time, for each employee

2. For question 2, return a CSV file, with user_id and session_length, having a single entry user the user that had the longest work session

3. And for question 3, return a CSV file with weekday, min_presence, average_presence, and max_presence of number of persons that visited the office, with data for each of the seven (7) days of the week. For the central tendency, the correct metric would be the median_presence, but it is relatively complicated to do so in SQLite

### What you will find in this repo
- In the `project_documentation` folder you will find the user documentation, with which you are advised to start, with instruction on how to use the solution, along with the technical documentation for lower level details.
- In the `main` folder you will find all the code base, starting with solution.py which is the main entry point, along with the lower level modules, and the testing suites.
- In `data`, there is the raw data that we start with, the outputs/answers to the questions and some intermediate data that we need for the solution.

### Main ingredients
This project is made of mostly Python and its Standard Library, SQLite that is part of the standard, and some cheating with Black and Pylint for the formatting.