""" 
The configuration file for computing the solution
The raw_data_file is the input, while the rest of the folders
hold the various final and intermediate outputs
The start and end date control the time frame for the computations
The minimal break (in seconds) is for now at two (2) hours
"""

raw_data_file = "../data/raw_data/in_out_data.csv"

clean_data_folder = "../data/clean_data/"

bad_data_folder = "../data/bad_data/"

output_folder = "../data/output/"

START_DATE = "2023-02-01"

END_DATE = "2023-02-29"

MINIMAL_BREAK_IN_SEC = 7200