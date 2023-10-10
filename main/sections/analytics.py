""" 
The analytics
"""



def analytics(clean_data_folder, output_folder):

    with open( clean_data_folder + "clean_data.csv", "r") as clean_data:
        print('Analytics says: I read the clean data') 

    with open( output_folder + "first.csv", "w") as first_answer:
        print('Analytics says: This is answer1') 

    with open( output_folder + "second.csv", "w") as second_answer:
        print('Analytics says: This is answer2')  

    with open( output_folder + "third.csv", "w") as third_answer:
        print('Analytics says: This is answer3') 

