"""A comparison between actual data produced by our solution, and desired ones

This file controls the acceptance tests for the whole solution.
In the acceptance_tests_scenarios there is a list of folders with the test data.
Given a raw data file, when processed by the solution, then we get the outputs.
For every scenario scenario, we start with initial raw data, that is being fed 
to the analytics solution, which then produces an actual output, that it finally
is compared to the expected output for the given initial raw data.
The result of the comparison is then presented to the user:
If the actual output and the expected output match, the solution works as intended.
If the actual output and the expected output DO NOT match, we get a print out of the differences
"""

import os
import difflib
from pprint import pprint
import solution


## The folders with the test cases
ACCEPTANCE_TESTS_POOL = "acceptance_tests_scenarios"
individual_scenarios = os.listdir(ACCEPTANCE_TESTS_POOL)


## Iterate over the scenarios
## For each one we'll run the acceptance tests
for scenario in individual_scenarios:
    print(scenario)
    individual_scenario = os.path.join(ACCEPTANCE_TESTS_POOL, scenario)

    raw_data_folder = os.path.join(individual_scenario, "raw_data/")
    desired_response_folder = os.path.join(individual_scenario, "desired_response/")
    actual_response_folder = os.path.join(individual_scenario, "actual_response/")
    actual_clean_data_folder = os.path.join(individual_scenario, "actual_clean_data/")

    ## Remove actual responses from last run
    for afile in os.listdir(actual_clean_data_folder):
        file_path = os.path.join(actual_clean_data_folder, afile)
        os.remove(file_path)

    for afile in os.listdir(actual_response_folder):
        file_path = os.path.join(actual_response_folder, afile)
        os.remove(file_path)

    ## Run the solution for each scenario and create actual responses
    for root, dirs, files in os.walk(raw_data_folder):
        raw_data_file = os.path.join(root, files[0])
        solution.the_solution(
            raw_data_file, actual_clean_data_folder, actual_response_folder
        )

        ## Compare the actual with the desired data

        ## 1.Get the file paths
        for file_name in os.listdir(actual_response_folder):
            ## Remember there are three(3) csv responses: first, second, third
            actual_response_filepath = os.path.join(actual_response_folder, file_name)
            desired_response_filepath = os.path.join(desired_response_folder, file_name)

            ## 2.Read content in pairs: actual vs desired for each of the three(3) csv responses
            with open(actual_response_filepath, "r") as actual_response_file:
                actual_response_contents = actual_response_file.readlines()

            with open(desired_response_filepath, "r") as desired_response_file:
                desired_response_contents = desired_response_file.readlines()

            ## 3.Compare actual vs desired
            result = list(
                difflib.unified_diff(
                    actual_response_contents,
                    desired_response_contents,
                    fromfile="",
                    tofile="",
                    fromfiledate="",
                    tofiledate="",
                    n=2,
                    lineterm="\n",
                )
            )

            ## result is a list of strings, that represent differences between the two files
            if result:
                print(
                    f"For the scenario {scenario}, and for file {file_name}, ",
                    "there are the following differences between actual and desired outputs",
                )
                pprint(result)
            else:
                print(
                    f"For the scenario {scenario}, and for file {file_name}, ",
                    "THERE IS A PERFECT MATCH betwen actual and desired",
                )
