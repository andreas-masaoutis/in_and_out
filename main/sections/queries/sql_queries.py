"""
The queries for the analytics

There is a series of final queries, that produce the results for the answers,
and some intermediate ones, written separately mostly for readability

The basis for all queries are the cleaned data in the table "in_out":
- user_id: string like 98ea63ee-bba1-4ea5-8ada-1d0a2dd1f6fd
- event_type: one of the two strings ['GATE_IN, 'GATE_OUT']
- event_time: a string 2023-03-03T21:52:53.000Z which is a valid datetime in sqlite

Each query produces extra data; take a look at each individual one for details
"""


############################
### Intermediate queries ###
############################

NET_OFFICE_HOURS = """
/* 
CONTEXT: 
- This is the first part of question 1, net hours spent in the office by each employee
RETURNS: (table: net_office_hours, with length = NUMBER_OF_EMPLOYEES that has ever entered office)
- user_id: the usual string
- total_time_in_office: an integer representing net hours, measured in seconds, eg 388288 
MECHANISM:
- Get the event_time lagged by one, so GATE_OUT time is at same row with previous GATE_IN
- Calculate the time differences so we know elapsed time between all event_types,
    either GATE_IN->GATE_OUT but also GATE_OUT->GATE_IN
- Group by users and sum for when employee was in the office
    (" WHERE event_type IS 'GATE_OUT' " is correct because event_type GATE_OUT - lagged GATE_IN)
*/

CREATE TABLE IF NOT EXISTS net_office_hours 
AS WITH lagged_eventsCTE AS
  (SELECT user_id,
          event_type,
          event_time,
          lag (event_time, 1, 0) OVER (PARTITION BY user_id
                                       ORDER BY event_time)  
                                            AS lagged_time, 
          strftime('%s', event_time) - strftime('%s', lag (event_time, 1, 0) OVER (PARTITION BY user_id
                                                                                 ORDER BY event_time)
                                                                                 ) AS event_type_duration
   FROM in_out
   WHERE event_time >= '2023-02-01'
     AND event_time <= '2023-02-29' )
SELECT user_id,
       sum(event_type_duration) AS total_time_in_office
FROM lagged_eventsCTE
WHERE event_type IS 'GATE_OUT'
GROUP BY user_id
ORDER BY total_time_in_office DESC

"""


DAYS_IN_OFFICE = """
/* 
CONTEXT: 
- This is the second part of question 1, the number of calendar days an employee entered the office
RETURNS: (table: days_in_office, with length = NUMBER_OF_EMPLOYEES that has ever entered the office)
- user_id: the usual string
- total_days_in_office: an integer representing calendar days, eg 19 
MECHANISM:
- Just count the distinct dates where there was an event type for each employee
*/

CREATE TABLE IF NOT EXISTS days_in_office AS
SELECT user_id ,
       count(days_in_office) AS total_days_in_office
FROM
  (SELECT DISTINCT user_id ,
                   substr(event_time, 1, 10) AS days_in_office
   FROM in_out
   WHERE event_time >= '2023-02-01'
     AND event_time <='2023-02-29' )
GROUP BY user_id
"""


SESSION_VS_BREAK = """
/* 
CONTEXT: 
- This for question 2, to figure out whether the duration between two events is session or break
RETURNS: (table: session_vs_break, with length = in_out - all the data)
- all the columns from in_out
- lagged_time: the lagged by 1 event_time for each employee
- the_dif: the time difference between event_types in seconds, eg 7250
- session_identification: ['session','break'] according to the rules
    (" WHEN event_type IS 'GATE_OUT' THEN 'session'" is correct because event_type GATE_OUT - lagged GATE_IN)
MECHANISM:
- Create the lagged time and time dif for each row
- Apply the rules and decide if each time duration is session or break
    ( when employee in office then session, but also when out of office for less than 7200 seconds (2 hours) )
*/

   CREATE TABLE IF NOT EXISTS session_vs_break AS
SELECT * ,
       CASE
           WHEN event_type IS 'GATE_OUT' THEN 'session'
           WHEN event_type IS 'GATE_IN'
                AND the_dif < 7200 THEN 'session'
           ELSE 'break'
       END AS session_identification
FROM
  (SELECT user_id ,
          event_type ,
          event_time ,
          lag (event_time, 1, 0) OVER (PARTITION BY user_id
                                       ORDER BY event_time) AS lagged_time ,
                                      strftime('%s', event_time) - strftime('%s', lag (event_time, 1, 0) OVER (PARTITION BY user_id
                                                                                                               ORDER BY event_time)) AS the_dif
   FROM in_out
   WHERE event_time >= '2023-02-01'
     AND event_time <='2023-02-29') lagged
"""


############################
### final answer queries ###
############################

FIRST_ANSWER_QUERY = """
/* 
CONTEXT: 
- This is answer1, the rankin of the average time spent in office per employee
RETURNS: ( iterator with length = NUMBER_OF_EMPLOYEES that has ever entered office)
- user_id: the usual string
- time: an integer representing hours spent in office, measured in hours (truncating min/sec), eg 73 
- days: an integer representing calendar days present in office, eg 19 
- average_per_day: string (05:10:11) representing the division of the two above
- rank: integer (1 to NUMBER_OF_EMPLOYEES) starting with highest average_per_day
MECHANISM:
- Join together the two tables net_office_hours and days_in_office
- And calculate the rest of the columns
*/

SELECT net_office_hours.user_id ,
       total_time_in_office / 3600 AS total_time_in_office ,
       total_days_in_office ,
       time((total_time_in_office / total_days_in_office) , 'unixepoch') AS average_per_day ,
       RANK () OVER (
                     ORDER BY (total_time_in_office / total_days_in_office) DESC) ValRank
FROM net_office_hours
JOIN days_in_office ON net_office_hours.user_id = days_in_office.user_id

"""


SECOND_ANSWER_QUERY = """
/* 
CONTEXT: 
- This is answer2, the longest uninterrupted session 
RETURNS: ( iterator with length 10 - asked for 1, added another 9 for reference)
- user_id: the usual string
- session_length: string (12:46:14) representing the session duration for an employee
MECHANISM:
( This is a variation of the gaps and islands problem 
https://mattboegner.com/improve-your-sql-skills-master-the-gaps-islands-problem/ )
- Use the session_vs_break table for the identification of session and breaks and then,
- calculate two ranks, one for session and break (values_rank) 
    and another for each contiguous group of session and breaks (sequence_grouping)
- then we only select sessions, group and sum for users and each individual sequence
*/

WITH sessions AS
  (SELECT * , rowid
   FROM session_vs_break),
     rankings AS
  (SELECT user_id ,
          event_type ,
          event_time ,
          lagged_time ,
          the_dif ,
          session_identification ,
          rowid AS key_rank ,
          DENSE_RANK() OVER(PARTITION BY user_id, session_identification ORDER BY rowid) AS values_rank , 
          rowid - DENSE_RANK() OVER(PARTITION BY user_id, session_identification ORDER BY rowid) AS sequence_grouping
   FROM sessions)
SELECT user_id ,
       TIME (sum(the_dif),
             'unixepoch') AS session_length
FROM rankings
WHERE session_identification IS 'session'
GROUP BY user_id,
         sequence_grouping
ORDER BY session_length DESC
LIMIT 10

"""


THIRD_ANSWER_QUERY = """
/* 
CONTEXT: 
- This is answer3, the employee presence in office for each day of the week
RETURNS: ( iterator with length up to 7 (as days of week))
- weekday: string, Monday to Sunday
- min_employee_presence: integer eg 18, for each weekday the min of employees that entered the office
- avg_employee_presence: integer eg 18, for each weekday the average of employees that entered the office
- max_employee_presence: integer eg 18, for each weekday the max of employees that entered the office
MECHANISM:
- From in_out we find the names of the weekdays
- then we group and and count distinct users that went in the office each calendar date
    (in our case in February)
- and finally, we group and count for weekdays, and get the stats we need
*/

SELECT weekday ,
       min(head_count) AS min_headcount ,
       avg(head_count) AS avg_headcount ,
       max(head_count) AS max_headcount
FROM
  (SELECT weekday ,
          weekday_int ,
          count(user_id) head_count
   FROM
     (SELECT DISTINCT user_id ,
                      substr(event_time, 1, 10) AS event_date ,
                      CAST (strftime('%w', event_time) AS integer) AS weekday_int ,
                           CASE CAST (strftime('%w', event_time) AS integer)
                               WHEN 0 THEN 'Sunday'
                               WHEN 1 THEN 'Monday'
                               WHEN 2 THEN 'Tuesday'
                               WHEN 3 THEN 'Wednesday'
                               WHEN 4 THEN 'Thursday'
                               WHEN 5 THEN 'Friday'
                               ELSE 'Saturday'
                           END AS weekday
      FROM in_out
      WHERE event_time >= '2023-02-01'
        AND event_time <='2023-02-29' )
   GROUP BY weekday,
            event_date)
GROUP BY weekday
ORDER BY weekday_int
"""

FOURTH_ANSWER_QUERY = """
/* 
CONTEXT: 
- This is answer4, the maximum ever employee presence in office for each day of the week, for each hour band
RETURNS: ( iterator with length up to 7 (as days of week))
- weekday: string, Monday to Sunday
- (multiple columns): from 7:00 to 22:00
MECHANISM:
- From the SESSION_VS_BREAK, where we have the lagged data, we compute, 
    for each hour from 7:00 to 22:00 whether the employee was in the office
- then we group for each daily date and we compute how many employees were in the office for each hour band
- and finally we group for each weekday and get the maximum presence ever in the office for each hour band
*/
SELECT weekday ,
       MAX(seven_AM) AS seven_AM ,
       MAX(eight_AM) AS eight_AM ,
       MAX(nine_AM) AS nine_AM ,
       MAX(ten_AM) AS ten_AM ,
       MAX(eleven_AM) AS eleven_AM ,
       MAX(twelve_NOON) AS twelve_NOON ,
       MAX(one_PM) AS one_PM ,
       MAX(two_PM) AS two_PM ,
       MAX(three_PM) AS three_PM ,
       MAX(four_PM) AS four_PM ,
       MAX(five_PM) AS five_PM ,
       MAX(six_PM) AS six_PM ,
       MAX(seven_PM) AS seven_PM ,
       MAX(eight_PM) AS eight_PM ,
       MAX(nine_PM) AS nine_PM ,
       MAX(ten_PM) AS ten_PM
FROM
  (SELECT user_id ,
          event_type ,
          event_time ,
          lagged_time ,
          strftime("%Y-%m-%d", lagged_time) AS daily_date ,
          CASE CAST (strftime('%w', event_time) AS integer)
              WHEN 0 THEN 'Sunday'
              WHEN 1 THEN 'Monday'
              WHEN 2 THEN 'Tuesday'
              WHEN 3 THEN 'Wednesday'
              WHEN 4 THEN 'Thursday'
              WHEN 5 THEN 'Friday'
              ELSE 'Saturday'
          END AS weekday ,
          CAST (strftime('%w', event_time) AS integer) AS weekday_int ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 7
                            AND 7 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS seven_AM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 8
                            AND 8 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS eight_AM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 9
                            AND 9 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS nine_AM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 10
                            AND 10 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS ten_AM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 11
                            AND 11 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS eleven_AM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 12
                            AND 12 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS twelve_NOON ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 13
                            AND 13 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS one_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 14
                            AND 14 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS two_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 15
                            AND 15 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS three_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 16
                            AND 16 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS four_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 17
                            AND 17 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS five_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 18
                            AND 18 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS six_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 19
                            AND 19 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS seven_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 20
                            AND 20 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS eight_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 21
                            AND 21 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS nine_PM ,
               sum(CASE
                       WHEN CAST(strftime("%H", lagged_time) AS INT) <= 22
                            AND 22 <= CAST(strftime("%H", event_time) AS INT) THEN 1
                       ELSE 0
                   END) AS ten_PM
   FROM session_vs_break
   WHERE event_type IS 'GATE_OUT'
   AND event_time >= '2023-02-01'
   AND event_time <= '2023-02-29'

   GROUP BY daily_date)
GROUP BY weekday
ORDER BY weekday_int

"""