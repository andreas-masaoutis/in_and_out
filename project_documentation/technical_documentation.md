# in and out

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

The core will be the SQLite DB, wrapped around an API that should ingest the prepared data, accept SQL queries, and return the solution CSV files requested.
|  |   |  |  |  |
|:----:|:----:|:----:|:----:|:-----:|
| Raw data &rarr;  | Data Pipeline &rarr;  | Clean Data &rarr; | Analytics Engine &rarr; | CSV results |
| | &uarr;  | | &uarr; | |
| | Data quality rules | | SQL queries | |


### Test plan

Once we have a general architectural model, we can decide how to test the solution:

- Unit tests for:
    1. The data quality rules
    2. The SQL queries
    3. The analytics engine API
Each element is a transformation and, at least in theory, it should be easy to test. For example, replacing all lowercase event types can be directly tested. Similar for the queries

- Integration test for:
    1. The whole pipeline
    2. The whole analytics engine
Here we want to make sure that all the pieces of each section work together without problems. The data pipeline should transform the raw data into cleaned data, and the analytics engine should transform the cleaned data into correct results. Here we assume that the unit tests make sure that all the individual parts work as expected.

- Acceptance tests for:
    1. Well, the whole solution.
Given a set of raw data, there should be a corresponding set of response CSv files.

Testing will be implemented with the unittest library.

### Deployment

We use docker for deploying the analytics solution. Although we will not have any other requirements other than Standard Library, it provides the same execution environment across machines.

A user is still able to execute the solution and get the results with their system installed Python, and it should be just fine, unless some really rare bug occurring.

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