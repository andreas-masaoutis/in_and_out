"""The rules for assessing data quality and possible fixes

The pipeline ingests the raw data and has to deliver the clean data
with the following format:

- user_id: string like 98ea63ee-bba1-4ea5-8ada-1d0a2dd1f6fd
- event_type: one of the two strings ['GATE_IN, 'GATE_OUT']
- event_time: a string 2023-03-03T21:52:53.000Z which is a valid datetime in sqlite

The following has to be true for the clean data as well:

- There are no duplicate values
- There are no more user_ids than the registered employees
- For every entry there is a subsequent exit
- There is no exit without entry

In some case we can provide fixes of we find a problem
- Lowercase event_types to uppercase eg "gate_in" -> "GATE_IN"

We have not implemented yet the rules for treating data that do not conform
The bad_data CSV will accept this data for further inquiry 
"""

import re
from datetime import datetime


def check_user_id_format(astring:str) -> bool:
    """
    Return True if string conforms to standard, False otherwise

    standard: 'p3b4e81f-79de-4937-ba87-aec8e7e731af'
    """

    expr = r"[a-z\d]{8}-[a-z\d]{4}-[a-z\d]{4}-[a-z\d]{4}-[a-z\d]{12}"
    pattern = re.compile(expr)
    return bool(pattern.fullmatch(astring))


def check_event_type(astring:str, allowed_values:list[str,str]) -> bool:
    """
    Return True if string in allowed string, False otherwise

    allowed in our case = ["GATE_IN","GATE_OUT"]
    """
    try:
        return bool(astring in allowed_values)
    except TypeError as e:
        raise SystemExit("There has been an internal problem calling function 'check_event_type' in file pipeline.py; function was called with the wrong type for variable 'allowed_values'. \nThe solution will now terminate")


def fix_lowercase_entry_type(astring:str) -> bool:
    """
    Fix the lower case issue.
    If you cannot fix it, leave it as is
    """
    fixes = {"gate_in": "GATE_IN", "gate_out": "GATE_OUT"}
    try:
        return fixes[astring]
    except KeyError as e:
        return astring


def check_event_time(astring:str) -> bool:
    """
    Check if string represents datetime, of certain length

    format = "2023-02-15T09:56:31.000Z"
    """
    try:
        the_datetime = datetime.strptime(astring, "%Y-%m-%dT%H:%M:%S.%fZ")
        return bool(isinstance(the_datetime, datetime) and len(astring) == 24)
    except ValueError as e:
        return False


def check_employee_number(adict:dict, desired_number_of_keys:int) -> bool:
    """
    For a dictionary, verify that 1. dict not empty 2. up to as many keys
    """
    if not isinstance(desired_number_of_keys, int):
        print("The variable NUMBER_OF_EMPLOYEES set in the solution_config.py file, has to be an integer")
        raise SystemExit("The solution will now terminate")
    else:
        return bool(0 < len(adict.keys()) <= desired_number_of_keys)


def check_entry_exit_sequence_and_no_duplicates(adict:dict)-> tuple:
    """
    Verify that for each employee:
    1. there are no duplicates
    2. there is an exit if and only if there is a previous entry

    If there is any problem, sent all entries from user to bad_data
    Return, separately, the user_id that are ok, and the user_ids with problems like so:
     (
        ['good_user1', 'good_user2', ...],
        ['bad_user1', ... 'bad_usern']
        )
    """
    all_user_ids = adict.keys()

    good_data_user_id = []

    bad_data_user_id = []

    for user_id in adict.keys():
        ins = adict[user_id]["GATE_IN"]
        outs = adict[user_id]["GATE_OUT"]

        ## case of duplicate entries
        if (len(ins) != len(set(ins))) or (len(outs) != len(set(outs))):
            bad_data_user_id.append(user_id)
            break

        ## case of missing events
        if len(ins) != len(outs):
            bad_data_user_id.append(user_id)
            break

        ## zip([ins] + [outs]) -> [(in, out), (in, out), ...]
        ## if exit before entry we have violation of business rules
        for entry_time, exit_time in zip(ins, outs):
            if exit_time < entry_time:
                bad_data_user_id.append(user_id)

    good_data_user_id = all_user_ids - bad_data_user_id

    ## It is preferable to have the keys always sorted,
    ## so that clean data do not change among executions - same data different sort
    good_data_user_id = list(good_data_user_id)
    bad_data_user_id = list(bad_data_user_id)
    good_data_user_id.sort()
    bad_data_user_id.sort()

    return (good_data_user_id, bad_data_user_id)
