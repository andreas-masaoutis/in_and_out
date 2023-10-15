"""Read and load the clean data, perform SQL queries, and write final CSV files
"""
import csv
import sqlite3
from .queries import sql_queries
from .readers_n_writers import readers_n_writers



def analytics(clean_data_folder:str, output_folder:str) -> None:
    """Read and load the clean data, perform SQL queries, and write final CSV files"""

    ### Read the clean data ###
    try:
        clean_data = readers_n_writers.initial_reader( clean_data_folder + "clean_data.csv" )
    except Exception as e:
        print("The analytics could not read the clean data.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")


    ### Connect to DB and load the data  ###
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS in_out(user_id, event_type, event_time)")
    insert_records = (
        "INSERT INTO in_out (user_id, event_type, event_time) VALUES(?, ?, ?)"
    )
    cur.executemany(insert_records, clean_data)
    con.commit()

    ## Not needed any more
    del clean_data

    #########################################
    ### Intermediate queries - no returns ###
    #########################################
    cur.execute(sql_queries.NET_OFFICE_HOURS)
    cur.execute(sql_queries.DAYS_IN_OFFICE)
    cur.execute(sql_queries.SESSION_VS_BREAK)

    #############################################
    ### final answer queries and csv creation ###
    #############################################

    ###### Question 1 ######
    answer1_result = cur.execute(sql_queries.FIRST_ANSWER_QUERY)
    try:
        readers_n_writers.final_writer(
            output_folder + "first.csv",
            answer1_result,
            ["user_id", "time", "days", "average_per_day", "rank"],
        )
    except Exception as e:
        print("The analytics could not write answer1.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")

    ###### Question 2 ######
    answer2_result = cur.execute(sql_queries.SECOND_ANSWER_QUERY)
    try:
        readers_n_writers.final_writer(
            output_folder + "second.csv", answer2_result, ["user_id", "session_length"]
        )
    except Exception as e:
        print("The analytics could not write answer2.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")

    ###### Question 3 ######
    answer3_result = cur.execute(sql_queries.THIRD_ANSWER_QUERY)
    try:
        readers_n_writers.final_writer(
            output_folder + "third.csv",
            answer3_result,
            [
                "weekday",
                "min_employee_presence",
                "avg_employee_presence",
                "max_employee_presence",
            ],
        )
    except Exception as e:
        print("The analytics could not write answer2.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")
    
    con.close()
