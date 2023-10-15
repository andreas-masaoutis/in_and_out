"""The complete solution

Here we connect together the two main parts, the pipeline and the analytics engine.

The pipeline reads raw data, runs quality checks, fixes problems, and writes clean/bad data.
The analytics reads and loads the clean data, perform SQL queries, and writes final CSV files.
The clean_data csv file is like a port between the two.
"""
import tracemalloc


from sections import pipeline, analytics

from solution_config import (
    raw_data_file,
    clean_data_folder,
    bad_data_folder,
    output_folder,
)


def the_solution(raw_data_file, clean_data_folder, bad_data_folder, output_folder):
    """Piecing together the pipeline and the analytics"""

    pipeline.pipeline(raw_data_file, clean_data_folder, bad_data_folder)

    analytics.analytics(clean_data_folder, output_folder)


if __name__ == "__main__":
    tracemalloc.start()
    
    print("Solution says: I am in")
    the_solution(raw_data_file, clean_data_folder, bad_data_folder, output_folder)
    print("Solution says: I am done")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory usage - Current: {current / 1000000} MB, Peak {peak / 1000000} MB" )
