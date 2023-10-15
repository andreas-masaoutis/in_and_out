"""Read raw data, run quality checks, fix problems, and write clean/bad data
"""

from .rules_n_fixes import rules_n_fixes
from .special_data_structure import sds
from .readers_n_writers import readers_n_writers

NUMBER_OF_EMPLOYEES = 25

def pipeline(raw_data_file:str, clean_data_folder:str, bad_data_folder:str) -> None:
    """Read raw data, run quality checks, fix problems, and write clean/bad data
    
    Note: bad_data is determined at two stages: First when checking individual lines,
    and then when checking groups of lines.
    Eg well formatted lines for a user with only GATE_OUT
    See the data rules_n_fixes module for more info on data rules

    """
    syntactically_correct_data = []
    bad_data = []

    try:
        lines_raw_data = readers_n_writers.initial_reader(raw_data_file)
    except Exception as e:
        print("The pipeline could not read the raw data.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")

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
            break

        if not rules_n_fixes.check_event_type(event_type, ["GATE_IN", "GATE_OUT"]):
            ## try to fix 'gate_in' or 'gate_out'
            event_type = rules_n_fixes.fix_lowercase_entry_type(event_type)

            if not rules_n_fixes.check_event_type(event_type, ["GATE_IN", "GATE_OUT"]):
                bad_data.append(line)
                break

        if not rules_n_fixes.check_event_time(event_time):
            bad_data.append(line)
            break

        ## if no formatting problems proceed
        ## watch out - we do not use 'line' because it might have been modified
        syntactically_correct_data.append([user_id, event_type, event_time])

    ## Not needed any more
    del lines_raw_data

    #######################################################
    #### DATA CHECKS PART 2 - Groups of lines together ####
    #######################################################
    correct_data_dict = sds.create_sds(syntactically_correct_data)
    del syntactically_correct_data

    if not rules_n_fixes.check_employee_number(correct_data_dict, NUMBER_OF_EMPLOYEES):
        print("Houston, we have a problem with the NUMBER_OF_EMPLOYEES")

    good_data_user_id, bad_data_user_id = rules_n_fixes.check_entry_exit_sequence_and_no_duplicates(correct_data_dict)

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

    ## Not needed any more
    del correct_data_dict

    final_clean_data = sds.sds_to_list(clean_data_dict)
    del clean_data_dict

    final_bad_data = sds.sds_to_list(bad_data_dict) + bad_data
    del bad_data_dict, bad_data


    try:
        readers_n_writers.final_writer(
        clean_data_folder + "clean_data.csv",
        final_clean_data,
        ["user_id", "event_type", "event_time"],
        )
    except Exception as e:
        print("The pipeline could not write the clean data.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")

    del final_clean_data



    try:
        readers_n_writers.final_writer(
        bad_data_folder + "bad_data.csv",
        final_bad_data,
        ["user_id", "event_type", "event_time"],
        )
    except Exception as e:
        print("The pipeline could not write the bad data.")
        print(f"The exception raised was: {e}") 
        raise SystemExit("The solution will now terminate")
    
    del final_bad_data