"""The helper functions for reading and writing CSV files

"""

import csv
import logging

logger = logging.getLogger(__name__)


def initial_reader(a_file_path:str) -> None:
    """Read a CSV and return a list of lines
    
    Args:
        Path to csv file - a string

    Returns
        A list of lists that in our case have the following format:
        [
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ...
        ]
    Raises:
        SystemExit - if the file cannot be processed, just kill it
    """

    line_collection = []
    try:
        with open(a_file_path, "r") as the_input_file:
            the_input_file_reader = csv.reader(the_input_file)
            ## Get rid of the header
            next(the_input_file_reader)

            for line in the_input_file_reader:
                user_id = line[0]
                event_type = line[1]
                event_time = line[2].strip("\n")

                line_collection.append([user_id, event_type, event_time])
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print("There was some error. See the logs for details.")
        print(f"The exception raised was: {e}")
        raise SystemExit("The solution will now terminate")

    return line_collection


def final_writer(a_file_path:str, an_iterator:list[list[str, str, str]], a_header:list[str, str, str] ) -> None:
    """Given a list of list, you'll get a CSV file
    
    Args:
        Path to csv file - a string
        A list of lists that in our case have the following format:
        [
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ...
        ]
        A list of strings for the CSV header
        ['user_id','event_type','event_time']

    Returns:
        A CSV file at the filepath provides, with the header as first line and the list content as rows

    Raises:
        SystemExit - if the file cannot be opened, just kill the process
    """

    try:
        with open(a_file_path, "w") as the_output_file:
            the_output_file_writer = csv.writer(the_output_file)
            the_output_file_writer.writerow(a_header)
            for the_line in an_iterator:
                the_output_file_writer.writerow(the_line)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print("There was some error. See the logs for details.")
        print(f"The exception raised was: {e}")
        raise SystemExit("The solution will now terminate")
