"""Read and load the clean data, perform SQL queries, and write final CSV files
"""
import csv
import sqlite3
from .queries import sql_queries
from .readers_n_writers import readers_n_writers
import logging

logger = logging.getLogger(__name__)


def analytics(clean_data_folder: str, output_folder: str) -> None:
    """Read and load the clean data, perform SQL queries, and write final CSV files"""

    logger.info("I am the analytics: I am in")

    ### Read the clean data ###

    clean_data = readers_n_writers.initial_reader(clean_data_folder + "clean_data.csv")

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

    logger.info("I am the analytics: I have set up the DB")

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
    readers_n_writers.final_writer(
        output_folder + "first.csv",
        answer1_result,
        ["user_id", "time", "days", "average_per_day", "rank"],
    )
    logger.info("I am the analytics: I have produced the first answer")

    ###### Question 2 ######
    answer2_result = cur.execute(sql_queries.SECOND_ANSWER_QUERY)
    readers_n_writers.final_writer(
        output_folder + "second.csv", answer2_result, ["user_id", "session_length"]
    )
    logger.info("I am the analytics: I have produced the second answer")

    ###### Question 3 ######
    answer3_result = cur.execute(sql_queries.THIRD_ANSWER_QUERY)
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
    logger.info("I am the analytics: I have produced the third answer")

    ###### Question 4 ######
    answer4_result = cur.execute(sql_queries.FOURTH_ANSWER_QUERY)
    readers_n_writers.final_writer(
        output_folder + "fourth.csv",
        answer4_result,
        [
            "weekday",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
        ],
    )
    logger.info("I am the analytics: I have produced the fourth answer")

    con.close()

    logger.info("I am the analytics: I am out")
