"""Read raw data, run quality checks, fix problems, and write clean/bad data
"""

from .rules_n_fixes import rules_n_fixes
from .special_data_structure import sds
from .readers_n_writers import readers_n_writers
import logging

logger = logging.getLogger(__name__)

NUMBER_OF_EMPLOYEES = 25


def pipeline(raw_data_file: str, clean_data_folder: str, bad_data_folder: str) -> None:
    """Read raw data, run quality checks, fix problems, and write clean/bad data

    Note: bad_data is determined at two stages: First when checking individual lines,
    and then when checking groups of lines.
    Eg well formatted lines for a user with only GATE_OUT
    See the data rules_n_fixes module for more info on data rules

    """
    logger.info("I am the pipeline: I am in")

    syntactically_correct_data = []
    bad_data = []

    lines_raw_data = readers_n_writers.initial_reader(raw_data_file)

    ##########################################################
    #### DATA CHECKS PART 1 - Individual field formatting ####
    ##########################################################

    ## if a line has data that does not follow the correct format
    ## send it to the bad_data
    ## otherwise send it to the syntactically_correct_data
    for line in lines_raw_data:
        user_id = line[0]
        event_type = line[1]
        event_time = line[2]

        ## The checks on individual data rows
        if not rules_n_fixes.check_user_id_format(user_id):
            bad_data.append(line)
            logger.warning("I am the pipeline: There is some bad data")
            break

        if not rules_n_fixes.check_event_type(event_type, ["GATE_IN", "GATE_OUT"]):
            ## try to fix 'gate_in' or 'gate_out'
            event_type = rules_n_fixes.fix_lowercase_entry_type(event_type)

            if not rules_n_fixes.check_event_type(event_type, ["GATE_IN", "GATE_OUT"]):
                bad_data.append(line)
                logger.warning("I am the pipeline: There is some bad data")
                break

        if not rules_n_fixes.check_event_time(event_time):
            bad_data.append(line)
            logger.warning("I am the pipeline: There is some bad data")
            break

        ## if no formatting problems proceed
        ## watch out - we do not use 'line' because it might have been modified
        syntactically_correct_data.append([user_id, event_type, event_time])

    logger.info("I am the pipeline: I have loaded the data")
    ## Not needed any more
    del lines_raw_data

    #######################################################
    #### DATA CHECKS PART 2 - Groups of lines together ####
    #######################################################
    correct_data_dict = sds.create_sds(syntactically_correct_data)
    del syntactically_correct_data

    if not rules_n_fixes.check_employee_number(correct_data_dict, NUMBER_OF_EMPLOYEES):
        logger.warning(
            "I am the pipeline: There is a problem with the NUMBER_OF_EMPLOYEES"
        )

    (
        good_data_user_id,
        bad_data_user_id,
    ) = rules_n_fixes.check_entry_exit_sequence_and_no_duplicates(correct_data_dict)

    ### Finally get the data together and write it to its destination ###

    clean_data_dict = {
        key: value
        for (key, value) in correct_data_dict.items()
        if key in good_data_user_id
    }
    bad_data_dict = {
        key: value
        for (key, value) in correct_data_dict.items()
        if key in bad_data_user_id
    }

    logger.info("I am the pipeline: I have prepared the data")
    ## Not needed any more
    del correct_data_dict

    final_clean_data = sds.sds_to_list(clean_data_dict)
    del clean_data_dict

    final_bad_data = sds.sds_to_list(bad_data_dict) + bad_data
    del bad_data_dict, bad_data

    readers_n_writers.final_writer(
        clean_data_folder + "clean_data.csv",
        final_clean_data,
        ["user_id", "event_type", "event_time"],
    )
    del final_clean_data

    readers_n_writers.final_writer(
        bad_data_folder + "bad_data.csv",
        final_bad_data,
        ["user_id", "event_type", "event_time"],
    )
    del final_bad_data

    logger.info("I am the pipeline: I have finally written the data")
    logger.info("I am the pipeline: I am out")
