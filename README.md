# in_and_out
A data analysis demo using IoT data

### The definition of the problem
There is an office with 25 registered employees. The office has a keycard entry system that registers the entry and exit time for each individual employee. Te data produced by the system is of the form:

> user_id,event_type,event_time

where, the event type can be either denote entry or exit, and event time when the action took place.

The data come as a csv file.

#### Questions:
1. For each employee, for the month of February, calculate the following:
    - total_time_in_office: the net amount of hours spent in the office.
    - unique_days_in_office: the number of unique calendar days the employee was present in the office.
    - average_employee_time_per_day: the total time spent in the office divided by the unique days the employee was present in the office.
    - employee_ranking_average_time: the ranking of the employees along average time per day spent in the office.

2. Which employee had the longest work session in February?

    From the first entry to the last exit, each entry and exit form a chain. If there are more than two (2) hours between an exit and the next entry, then the session has ended. For example, either when leaving the office in the evening and returning next morning, or whenever during the day when a break from the office is for more that two hours, a session has ended

    eg, IN 8, OUT 12, IN 13, OUT 18, (IN next day) this counts as one session from 8 to 18

    eg. IN 8, OUT 12, IN 15, OUT 18, (IN next day) these count as two sessions from 8 to 12 and from 15 to 18

3. (Optional) From the perspective of the office, assuming that the 25 registered employees denote the maximum capacity, what is the utilisation percent? Report the min, median, and max, taking care of outliers:
    - per weekday
    - per hour

#### Deliverables:
1. For question 1, return a CSV file with user_id, total_time_in_office_per_employee, unique_days_in_office_per_employee, average_employee_time_per_day, employee_ranking_average_time, for each employee

2. For question 2, return a CSV file, with user_id and session_length

3. And for question 3, return two (2) CSV files
    - One with weekday, min, median, max of utilisation percent, with data for each of the seven (7) days of the week.
    - And another, with hour, min, median, max of utilisation percent, with data for each of the twenty-four (24) hours of the day.

4. A report on data quality issues, with discarded values, or modified values, etc. Specific form TBD

### What you will find in this repo
TBD