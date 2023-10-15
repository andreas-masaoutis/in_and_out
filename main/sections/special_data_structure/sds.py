"""A Special Data Structure (sds), instead of a dataframe

We create a Special Data Structure (sds) for the pipeline 
that has to handle data with the following format:

- user_id: string like 98ea63ee-bba1-4ea5-8ada-1d0a2dd1f6fd
- event_type: one of the two strings ['GATE_IN, 'GATE_OUT']
- event_time: a string 2023-03-03T21:52:53.000Z

The data structure we are going to use in order to hold and manipulate the data 
is the following dictionary:

{
    user_id : {
        event_type : [ event_time, event_time, ... ]
    }
}

For example:
{
    user281f-79de-4937-ba87-aec8e7e731af : {
        'GATE_IN' : ['2023-02-01T08:00:00.000Z', '2023-02-02T08:00:00.000Z'],
        'GATE_OUT' : ['2023-02-01T16:00:00.000Z', '2023-02-02T16:00:00.000Z']
    },
    2feg281f-g6dh-4e34-bd87-5e68g7h736d5 : {
        'GATE_IN' : [...],
        'GATE_OUT' : [...]
    },
    ...
}

We provide two functions:
one that creates an SDS from individual data, and
another that transforms an SDS to a list 
"""

from datetime import datetime


def create_sds(array_of_csv_lines):
    """Read a collection of lines from a CSV and return a Special Data Structure

    Args:
        an array of arrays that are made of strings that represent
        user_id, event_type, event_time, like the following:
        [
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ...
        ]

    Returns:
        a dictionary where event_times are in chronological order
        {
        user_id : {
            event_type : [ event_time, event_time, ... ]
        }

    Raises:
        It should not raise anything because we have made sure that data is correct
    """

    sds = {}

    for the_line in array_of_csv_lines:
        user_id = the_line[0]
        event_type = the_line[1]
        event_time = the_line[2]

        if user_id not in sds:
            sds[user_id] = {"GATE_IN": [], "GATE_OUT": []}
            sds[user_id][event_type].append(
                datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            )
        else:
            sds[user_id][event_type].append(
                datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            )

    ## It is better to sort everything so that we
    ## can be sure data is in chronological order
    for user_id in sds:
        sds[user_id]["GATE_IN"] = sorted(sds[user_id]["GATE_IN"])
        sds[user_id]["GATE_OUT"] = sorted(sds[user_id]["GATE_OUT"])

    return sds


def sds_to_list(a_special_dict):
    """Read a Special Data Structure and return an array of potential CSV lines

    Args:
         a dictionary where event_times are in chronological order
        {
            user281f-79de-4937-ba87-aec8e7e731af : {
                'GATE_IN' : ['2023-02-01T08:00:00.000Z', '2023-02-02T12:00:00.000Z'],
                'GATE_OUT' : ['2023-02-01T11:00:00.000Z', '2023-02-02T16:00:00.000Z']
            },
            2feg281f-g6dh-4e34-bd87-5e68g7h736d5 : {
                'GATE_IN' : [...],
                'GATE_OUT' : [...]
            },
            ...
        }

    Returns:
        an array of arrays that are made of strings that represent
        user_id, event_type, event_time, like the following:
        [
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ['user_id','event_type','event_time'],
            ...
        ]
        Note: user_ids and event_types are grouped together and lexicographically ordered,
            while event_times are in chronological order

    Raises:
        It should not raise anything because we have made sure that data is correct
    """
    in_out_actions = []

    user_id_list = list(a_special_dict.keys())
    user_id_list.sort()

    for user_id in user_id_list:
        for event_type in a_special_dict[user_id]:
            for event_time in a_special_dict[user_id][event_type]:
                line = [
                    user_id,
                    event_type,
                    event_time.isoformat(sep="T", timespec="milliseconds") + "Z"
                    ## the +"Z" for the zulu time is a cheap hack
                    ## not all datasets will have this time zone
                ]
                in_out_actions.append(line)

    return in_out_actions
