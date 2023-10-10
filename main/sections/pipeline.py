""" 
The pipeline
"""



def pipeline(raw_data_file, clean_data_folder):

    with open( raw_data_file, "r") as first_answer:
        print('Pipeline says: I read the raw data')

    with open( clean_data_folder + "clean_data.csv", "w") as first_answer:
        print('Pipeline says: I created the clean data') 

