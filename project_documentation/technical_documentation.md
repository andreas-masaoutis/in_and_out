# in and out: Technical Documentation

### Requirements

The stated requirements are:

    - Following programming best practices (e.g., naming conventions, commenting, etc.)
    - Completeness: are all requirements met? are all tests passing?
    - Correctness: is the code written in a sensible, thought-out way?
    - Maintainability: is it written in a clean, supportable way?
    - The code should be organized, designed, tested, and documented as if it were going into production

The main objective is to transform the initial CSV file to actual answers to the 3 questions posed in the introduction. 
The solution should be modular, as a way, to be maintainable and testable - different parts of the solution perform different/independent tasks.
A test suite should be part of the solution.
Everything should be documented.

For the time being there are no other explicit requirements, like execution time or interface.

### Constraints
The main constraint for the technical stack is to only use the Python Standard Library.

### Architecture
The task at hand is to create an analytics solution. Therefore the constituent parts will be the following:
- We need an initial data pipeline for data ingestion
- and we need a 'place' to do the analytics

As we said the main technical constraint is to only use the Python Standard Library. That gives an obvious solution for the analytics engine: SQLite3. The lightweight disk-based database that doesn’t require a separate server process, and that can also load a DB file to memory and run from there, allows us to leverage SQL in order to query the data. Therefore, using a single SQLite file, we can hold and query the data.

We also need a process to ingest the data; a data pipeline. Since we are using only the Standard Library, we should let SQLite do the most part with data manipulation, so ELT is preferable. But we should still make sure that the data entered into the DB conform to the rules defined by the business process (in that case the keycard entry system ). Therefore, the pipeline will read, clean the load the data to the DB, leaving the rest of the data manipulation to the the DB.

In order to increase the modularity of the solution we will keep apart, in two separate module, the rules for cleaning the data and the queries. For every data problem we identify in the EDA phase, we will establish a data transformation that modifies the data and fixes the problem. In a similar manner, all SQL queries will be written and tested and kept separately from SQLite DB.

The core is SQLite DB, wrapped around an API that should ingest the prepared data, accept SQL queries, and return the solution CSV files requested.
|  |   |  |  |  |
|:----:|:----:|:----:|:----:|:-----:|
| Raw data &rarr;  | Data Pipeline &rarr;  | Clean Data &rarr; | Analytics Engine &rarr; | CSV results |
| | &uarr;  | | &uarr; | |
| | Data quality rules | | SQL queries | |


From the top down:
- The solution.py is the main execution point. It imports the two modules that are: 
    - The pipeline, and the analytics engine. Below them, there are the four building blocks:
        1. the readers and writers, effectively a wrapper around the csv module, that converts CSV to a list of rows and vice versa
        2. the sds, a dictionary formatted in a way to hold our specific data, and it functions as a replacement for a dataframe
        3. the implementation of the business rules for the data and some fixes for data points that are not well formatted by still fixable, like gate_in to GATE_IN
        4. the SQL queries that feed the analytics part

### Test plan

We have implemented unit tests for:
    1. The data quality rules
    2. The SQL queries
Each element is a transformation and, at least in theory, it should be easy to test. For example, replacing all lowercase event types can be directly tested. Similar for the queries.

For the two (2) modules that we have written unit tests, queries and rules_n_fixes, you can find the test suite inside the module. Execute with 

> python test_rules_n_fixes.py

or navigate to the module's folder and execute

> python -m unittest discover -v // -v for verbose with more info on the tests


- Acceptance tests for:
    1. Well, the whole solution.
Given a set of raw data, there should be a corresponding set of response CSv files.

For the acceptance test we have a script 

 > ~ / in_and_out / main / acceptance_tests_script.py

 that reads test scenarios, computes the solution for each input and compares the actual output with the desired.

 Navigate to the folder, execute the script with

 > python acceptance_tests_script.py 
 
 and you will get the results in the form:

> SCENARIO: bad_event_type, FILE: second.csv, PERFECT MATCH BETWEEN ACTUAL AND DESIRED 
> SCENARIO: bad_event_type, FILE: first.csv, PERFECT MATCH BETWEEN ACTUAL AND DESIRED 
> SCENARIO: bad_event_type, FILE: third.csv, PERFECT MATCH BETWEEN ACTUAL AND DESIRED 

 There are currently 8 scenarios. To register more, you simply have to replicate the folder structure decide what the raw should look like, and what the desired responses should be for the given raw data. Execute the script and you'll get the report, as above, indicating if there is a match, or whether and where are the differences. 


### Deployment

We use docker for deploying the solution. Although we will not have any other requirements other than Standard Library, it provides the same execution environment across machines.

A user is still able to execute the solution and get the results with their system installed Python, and it should be just fine, unless some really rare bug occurring.

In the docker-compose file found here:

 > ~ / in_and_out / docker-compose.yml

 there are two options for the execution command
>    command: ["python", "solution.py"]

or

>    command: ["/bin/bash"]

Use the second option (default) to run the solution via docker (for details see user documentation)

Use the first to create a container that you can then enter with 

>   sudo docker exec -it in_and_out_solution_1 /bin/bash

Since we use a volume to get all the code base inside the container, you can navigate around and execute all the commands for running the solution and its tests.

**Please read the user documentation for detailed instructions on how to execute the solution and its config**

### Available Data

#### Business Processes
The process that creates the data we should analyse is relatively straight forward. Employees use a keycard to enter and exit the office, and the data is being recorded. We assume, but we should also verify, that:
- employees cannot enter without the keycard, so there can be no employee that ony exits the building without having 'entered' it 
- employees do enter the building when the card is activated, and can only exit when they activate the keycard again. Therefore, for every entry, there should be an exit.

#### Data Rules
- Both of the above assumptions mean that for every employee there is an entry if an only if there is exit, while an entry always precedes an exit.
- There should be 25 unique users at most that have entered and exited the office
- There is no defined policy of office hours, although one might be evident in the data.
- For the three data fields user_id, event_type, event_time, we have that:
    - All fields are represented as strings 
    - The format for the use_id is the following: 67e4c352-bda1-4289-b0a4-0e25f67af5f2
    - The event_type can take only these two (2) values: GATE_IN and GATE_OUT
    - The format for the event_type is 2023-01-31T08:18:36.000Z, which is a valid date-time string for [SQLite](https://www.sqlite.org/lang_datefunc.html)  