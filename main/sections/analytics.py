""" 
The analytics
"""
import csv
import sqlite3


daily_duration = """
        CREATE TABLE IF NOT EXISTS daily_duration AS

        WITH durations AS (
        
        SELECT
            user_id
            , event_type
            , event_time
            , lag ( event_time, 1, 0) OVER ( PARTITION BY user_id ORDER BY event_time )

            , strftime('%s',
                        event_time
                        )
                -
             strftime('%s',
                        lag ( event_time, 1, 0) OVER ( PARTITION BY user_id ORDER BY event_time ) 
                        ) 
                AS the_dif
            
            FROM
                in_out
            WHERE
                event_time >= '2023-02-01'
                AND
                event_time <='2023-02-29'
                )

            SELECT 
                user_id
                , sum(the_dif) as total_time_in_office
            FROM
                durations
            WHERE
                event_type is 'GATE_OUT'
            GROUP BY
                user_id
            ORDER BY
                total_time_in_office DESC

                """




days_in_office = """
    CREATE TABLE IF NOT EXISTS days_in_office AS

    SELECT
        user_id
        ,count( 
            days_in_office
            ) AS total_days_in_office

    FROM(
        SELECT DISTINCT
            user_id
            ,  substr( event_time, 1, 10 ) AS days_in_office
        FROM 
            in_out
        WHERE
            event_time >= '2023-02-01'
            AND
            event_time <='2023-02-29'
        )
    GROUP BY
        user_id
"""


first_answer_query = """
    SELECT
        daily_duration.user_id
        , total_time_in_office / 3600 AS total_time_in_office
        , total_days_in_office
        , time( (total_time_in_office / total_days_in_office) , 'unixepoch')  AS average_per_day
        ,    RANK () OVER ( ORDER BY (total_time_in_office / total_days_in_office) DESC ) ValRank
    FROM
        daily_duration
    JOIN
        days_in_office
        ON
            daily_duration.user_id = days_in_office.user_id

"""


third_answer_query = """
    SELECT
        weekday
        ,min(head_count) as min_headcount
        ,avg(head_count) as avg_headcount
        ,max(head_count) as max_headcount
    FROM(SELECT
        weekday
        , weekday_int
        , count(user_id) head_count

    FROM    
        (SELECT DISTINCT
            user_id
            , substr( event_time, 1, 10 ) AS event_date
            ,  cast (strftime('%w', event_time) as integer) as weekday_int
            ,   case 
                    cast (strftime('%w', event_time) as integer)
                    when 0 then 'Sunday'
                    when 1 then 'Monday'
                    when 2 then 'Tuesday'
                    when 3 then 'Wednesday'
                    when 4 then 'Thursday'
                    when 5 then 'Friday'
                    else 'Saturday'
                end AS weekday
        FROM 
            in_out
        WHERE
            event_time >= '2023-02-01'
            AND
            event_time <='2023-02-29'
    )
    GROUP BY
        weekday, event_date)
    GROUP BY
        weekday
    ORDER BY
        weekday_int
"""


session_vs_break = """


    CREATE TABLE IF NOT EXISTS session_vs_break AS    

    SELECT
        *
        , CASE
            WHEN event_type IS 'GATE_OUT' THEN 'session'
            WHEN event_type IS 'GATE_IN' AND the_dif < 7200 THEN 'session'
            ELSE 'break'
        END AS session_identification
    FROM
    (            SELECT
            user_id
            , event_type
            , event_time
            , lag ( event_time, 1, 0) OVER ( PARTITION BY user_id ORDER BY event_time ) AS lagged_time

            , strftime('%s', event_time)
                -
             strftime('%s', lag ( event_time, 1, 0) OVER ( PARTITION BY user_id ORDER BY event_time ) )
                
                AS the_dif
            
            FROM
                in_out
            WHERE
                event_time >= '2023-02-01'
                AND
                event_time <='2023-02-29')  lagged
"""


second_answer_query = """
    WITH sessions AS (
    SELECT
        *
        , rowid
    FROM
        session_vs_break
    ), rankings AS
(
    SELECT
        user_id
        , event_type
        , event_time
        , lagged_time
        , the_dif
        , session_identification
        , rowid AS key_rank
        , DENSE_RANK() OVER(PARTITION BY user_id, session_identification  ORDER BY rowid) AS values_rank
        , rowid - DENSE_RANK() OVER(PARTITION BY user_id, session_identification  ORDER BY rowid) AS sequence_grouping
    FROM
        sessions )

    SELECT
        user_id
        , time (sum(the_dif),'unixepoch') AS session_length
         
    FROM
        rankings
    WHERE 
        session_identification IS 'session'
    GROUP BY
        user_id, sequence_grouping
    ORDER BY
        session_length DESC
    LIMIT 
        10

"""








def analytics(clean_data_folder, output_folder):

    con = sqlite3.connect(":memory:")
    # con = sqlite3.connect("in_out.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS in_out(user_id, event_type, event_time)" )

    insert_records = "INSERT INTO in_out (user_id, event_type, event_time) VALUES(?, ?, ?)"
 
    with open( clean_data_folder + "clean_data.csv", "r") as clean_data:
        print('Analytics says: I read the clean data') 
        clean_data_reader = csv.reader(clean_data)
        header = next(clean_data_reader)
    
        cur.executemany(insert_records, clean_data_reader)

        con.commit()



    cur.execute(daily_duration)
    cur.execute(days_in_office)
    cur.execute(session_vs_break)

    answer1_result = cur.execute(first_answer_query).fetchall()

    answer3_result = cur.execute(third_answer_query).fetchall()

    answer2_result = cur.execute(second_answer_query).fetchall()
    

    con.close()




    with open( output_folder + "first.csv", "w") as first_answer:
        print('Analytics says: This is answer1') 
        first_answer_writer = csv.writer(first_answer)
        header = ['user_id','time','days', 'average_per_day', 'rank']
        first_answer_writer.writerow(header)
        for line in answer1_result:
            first_answer_writer.writerow(line)



    with open( output_folder + "second.csv", "w") as second_answer:
        print('Analytics says: This is answer2')  
        second_answer_writer = csv.writer(second_answer)
        header = ['user_id','session_length']
        second_answer_writer.writerow(header)
        for line in answer2_result:
            second_answer_writer.writerow(line)



    with open( output_folder + "third.csv", "w") as third_answer:
        print('Analytics says: This is answer3') 

        third_answer_writer = csv.writer(third_answer)
        header = ['weekday','min_employee_presence','avg_employee_presence', 'max_employee_presence' ]
        third_answer_writer.writerow(header)
        for line in answer3_result:
            third_answer_writer.writerow(line)


