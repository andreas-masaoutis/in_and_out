"""
The solution
"""
print("I am in solution.py")

from sections import pipeline, analytics

import os
print( "This is the cwd for solution.py: ", os.getcwd() )

if __name__ == "__main__":

    pipeline.pipeline()

    analytics.analytics()