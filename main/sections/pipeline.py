""" 
The pipeline

REFACTOR!!!!!!
"""

import re
import csv
from datetime import datetime

NUMBER_OF_EMPLOYEES = 25

def rule1(astring):
    """
    Return True if string conforms to standard, False otherwise

    standard: 'p3b4e81f-79de-4937-ba87-aec8e7e731af'

    """

    expr = "[a-z\d]{1,8}-[a-z\d]{1,4}-[a-z\d]{1,4}-[a-z\d]{1,4}-[a-z\d]{1,12}"
    pattern = re.compile(expr)
    if pattern.fullmatch(astring):
        return True
    else: ## if sting does not match pattern
        return False


def rule2(astring, allowed_values):
    """
    Return True if string in allowed string, False otherwise

    allowed in our case = ["GATE_IN","GATE_OUT"]
    """
    if astring in allowed_values:
        return True
    else:
        return False


def fix1_rule2(astring):
    """

    """
    fixes = {
        "gate_in" : "GATE_IN",
        "gate_out" : "GATE_OUT"
    }

    return fixes[astring]


def rule3(astring):
    """
    Check if string represent datetime, of certain length

    format = "2023-02-15T09:56:31.000Z"
    """

    the_datetime = datetime.strptime(astring, "%Y-%m-%dT%H:%M:%S.%fZ")

    if isinstance(the_datetime, datetime) and len(astring) == 24:
        return True
    else:
        return False


def rule4(adict, desired_number_of_keys):
    """
    For a dictionary, verify that 1. dict not empty 2. up too as many keys
    """
    if 0 < len( adict.keys() ) <= desired_number_of_keys:
        return True
    else:
        return False



def rule5(adict):
    """
    Verify that for each employee, there is an exit if and only if there is a previous entry
    Return, separately, the user_ids with problems, and the user_id that are ok
    """
    all_user_ids = adict.keys()

    good_data_user_id = []

    bad_data_user_id = []

    for user_id in adict.keys():
        ins = adict[user_id]['GATE_IN']
        outs = adict[user_id]['GATE_OUT']

        if len(ins) != len(outs):
            print("Houston, we have a problem with missing events")
            bad_data_user_id.append(user_id)


        ## zip([ins] + [outs]) -> [(in, out), (in, out), ...]
        ## if exit before entry we have violation of business rules
        for entry_time, exit_time in zip(ins, outs):
            if exit_time < entry_time:
                print("Houston, we have a problem with events' sequence")
                bad_data_user_id.append(user_id)

    good_data_user_id = all_user_ids - bad_data_user_id

    ## It is preferable to have the keys always sorted, 
    ## so that clean data do not change among executions - same data different sort
    good_data_user_id = list(good_data_user_id)
    bad_data_user_id = list(bad_data_user_id)
    good_data_user_id.sort()
    bad_data_user_id.sort()
    
    return (good_data_user_id, bad_data_user_id)
                
    

def pipeline(raw_data_file, clean_data_folder, bad_data_folder):

    raw_data_dict_repr = {}

    with open( raw_data_file, "r") as raw_data:
        print('Pipeline says: I read the raw data')

        raw_data_reader = csv.reader(raw_data)
        header = next(raw_data_reader)

        for line in raw_data_reader:
            user_id = line[0]
            event_type = line[1]
            event_time = line[2].strip('\n')

            if not rule1(user_id):
                print(user_id, event_type, event_time)

            if not rule2(event_type, ["GATE_IN","GATE_OUT"]):
                event_type = fix1_rule2(event_type)

                if not rule2(event_type, ["GATE_IN","GATE_OUT"]):
                    print(user_id, event_type, event_time)

            if not rule3(event_time):
                print(user_id, event_type, event_time)

            ## The dict representation of the csv
            if user_id not in raw_data_dict_repr:
                raw_data_dict_repr[user_id] = { 
                    "GATE_IN" : [],
                    "GATE_OUT" : []
                }
                raw_data_dict_repr[user_id][event_type].append( datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ") )
            else:
                raw_data_dict_repr[user_id][event_type].append( datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ") )

        if not rule4(raw_data_dict_repr, NUMBER_OF_EMPLOYEES):
            print("Houston, we have a problem with the NUMBER_OF_EMPLOYEES")

        good_data_user_id, bad_data_user_id = rule5(raw_data_dict_repr)



    with open( clean_data_folder + "clean_data.csv", "w") as clean_data:
        print('Pipeline says: I created the clean data') 
        clean_writer = csv.writer(clean_data)
        header = ['user_id','event_type','event_time']
        clean_writer.writerow(header) 

        for user_id in good_data_user_id:
            for event_type in raw_data_dict_repr[user_id]:
                for event_time in raw_data_dict_repr[user_id][event_type]:
                    clean_writer.writerow([
                        user_id,event_type,event_time.isoformat(sep = 'T', timespec = 'milliseconds').replace('+00:00', 'Z')
 
                        ])



    with open( bad_data_folder + "bad_data.csv", "w") as bad_data:
        print('Pipeline says: I, unfortunately, created the bad data') 
        bad_writer = csv.writer(bad_data)
        header = ['user_id','event_type','event_time']
        bad_writer.writerow(header)

        for user_id in bad_data_user_id:
            for event_type in raw_data_dict_repr[user_id]:
                for event_time in raw_data_dict_repr[user_id][event_type]:
                    bad_writer.writerow([
                        user_id,event_type,event_time.isoformat(sep = 'T', timespec = 'milliseconds').replace('+00:00', 'Z')

                        ])

