"""
The solution
"""
print("Solution says: I am in")

from sections import pipeline, analytics

from solution_config import raw_data_file, clean_data_folder, bad_data_folder, output_folder

import os
print( "Solution says: my cwd is: ", os.getcwd() )


def the_solution(raw_data_file, clean_data_folder, bad_data_folder, output_folder):

    pipeline.pipeline(raw_data_file, clean_data_folder, bad_data_folder)
    
    analytics.analytics(clean_data_folder, output_folder)    


if __name__ == "__main__":

    the_solution(raw_data_file, clean_data_folder, bad_data_folder, output_folder)