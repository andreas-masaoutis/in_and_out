# Project

Project Description
Analysing the employee entry - exit data from an office

<!---
TEMPLATES for STORIES and TASKS

User story
- STORY_NAME:  <br/><br/> STORY_DESCRIPTION:  <br/><br/> STATUS:  <br/><br/>  STORY_ID:
Possible STATUSes: Prospective, Running, Completed, Cancelled

Task
- TASK_NAME: <br/><br/> TASK_DESCRIPTION: <br/><br/> COMMENTS:  <br/><br/>  TASK_ID:  <br/><br/> REFERENCES_STORY: (related STORY_ID)
-->


### User Stories

- STORY_NAME: Hourly occupancy rates <br/><br/> STORY_DESCRIPTION: As a user I want to know how many people were in the office in every hourly band for each weekday<br/><br/> STATUS: Running  <br/><br/>  STORY_ID: Hourly_occupancy  
- STORY_NAME:  Logging<br/><br/> STORY_DESCRIPTION: As a user I want to have access to a report on the status and results of the solution  (pipeline and analytics) so I can be advised of successful execution or possible problems <br/><br/> STATUS: Completed  <br/><br/>  STORY_ID: Logging  
- STORY_NAME: System refactor <br/><br/> STORY_DESCRIPTION: We have answered all questions but the quality of the solution is low. There are many refactorings to be done with various aims <br/><br/> STATUS: Completed  <br/><br/>  STORY_ID: System_refactor  
- STORY_NAME: User config <br/><br/> STORY_DESCRIPTION: As a user I want to be able to have access to all the necessary parameters for the solution so that I can easily modify them <br/><br/> STATUS: Completed  <br/><br/>  STORY_ID: User_config  
- STORY_NAME: User documentation <br/><br/> STORY_DESCRIPTION: As a user I want to have easy access to all the pieces of information that are relevant to the use of the system so that I can use it with minimal effort <br/><br/> STATUS: Completed  <br/><br/>  STORY_ID: User_docs  
- STORY_NAME: Architectural spike <br/><br/> STORY_DESCRIPTION: We need to create a first iteration in order to test the viability of proposed architectures. We should deliver a response to  question 1.1 (total_time_in_office). This story has many tasks that cover the whole range of tasks from specifying requirements to deployment. <br/><br/> STATUS: Completed  <br/><br/>  STORY_ID: Arch_spike  
- STORY_NAME: Bootstrap_the_Project <br/><br/> STORY_DESCRIPTION: All the necessary first steps in order to initiate the project <br/><br/> STATUS: Completed <br/><br/>  STORY_ID: tech1  

### Tasks

- TASK_NAME: Write tests for query <br/><br/> TASK_DESCRIPTION: We should write both the unit and the acceptance tests for the task and story <br/><br/> COMMENTS: <br/><br/>  TASK_ID: test_occupancy <br/><br/> REFERENCES_STORY: Hourly_occupancy  
- TASK_NAME: Write query <br/><br/> TASK_DESCRIPTION: Write the query for the hourly occupancy rates <br/><br/> COMMENTS: <br/><br/>  TASK_ID: query_occupancy <br/><br/> REFERENCES_STORY: Hourly_occupancy  
- TASK_NAME: Integraete query <br/><br/> TASK_DESCRIPTION: Once the query and its tests are ready we want to integrate the query into the solution <br/><br/> COMMENTS: <br/><br/>  TASK_ID: integrate_query <br/><br/> REFERENCES_STORY: Hourly_occupancy  
- TASK_NAME: Update docs <br/><br/> TASK_DESCRIPTION: Once the query is tested and implemented we should update the documentation <br/><br/> COMMENTS: <br/><br/>  TASK_ID: docs_occupancy <br/><br/> REFERENCES_STORY: Hourly_occupancy  

### In Progress


### Done ✓

- TASK_NAME: Technical documentation <br/><br/> TASK_DESCRIPTION: Update the technical documentation with all the latest changes <br/><br/> COMMENTS: <br/><br/>  TASK_ID: technical_docs <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Create logs <br/><br/> TASK_DESCRIPTION: Identify the places where info has to be collected from and gather everything in one file <br/><br/> COMMENTS: <br/><br/>  TASK_ID: logs1 <br/><br/> REFERENCES_STORY: Logging  
- TASK_NAME: User documentation <br/><br/> TASK_DESCRIPTION: Write the user documentation <br/><br/> COMMENTS: Mostly how to execute the solution<br/><br/>  TASK_ID: user_docs1 <br/><br/> REFERENCES_STORY: User_docs  
- TASK_NAME: User config <br/><br/> TASK_DESCRIPTION: Get all the variables for the execution of the solution in one file <br/><br/> COMMENTS: Use the already existing solution_config file <br/><br/>  TASK_ID: user_config1 <br/><br/> REFERENCES_STORY: User_config  
- TASK_NAME: Input validation <br/><br/> TASK_DESCRIPTION: The code only covers a happy path with no exception handling - cover for all cases <br/><br/> COMMENTS: Not only the solution but the integration tests too <br/><br/>  TASK_ID: validation <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Unit testing <br/><br/> TASK_DESCRIPTION: Once the modules are done we should write the unit tests <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: unittest <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Modularise solution <br/><br/> TASK_DESCRIPTION: For both pipeline and analytics we should get some of the lower level stuff to separate modules <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: modularise <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Formatting <br/><br/> TASK_DESCRIPTION: Use black and pylint across the code base <br/><br/> COMMENTS:  This is cheating - nothing apart from pure Python, remember? <br/><br/>  TASK_ID: formatting1 <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Fix docker volumes <br/><br/> TASK_DESCRIPTION: It seems that the docker volume is not properly set up  <br/><br/> COMMENTS: We changed the structure and got all the code base on the volume instead of just the data <br/><br/>  TASK_ID: docker_volumes <br/><br/> REFERENCES_STORY: Bug_fix  
- TASK_NAME: Acceptance test 2 <br/><br/> TASK_DESCRIPTION: Now that the solution is ready we need to expand, finalise and solve any problems with the acceptance tests <br/><br/> COMMENTS:  We need them to work for the subsequent refactoring <br/><br/>  TASK_ID: acceptance_test2 <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Data journey<br/><br/> TASK_DESCRIPTION: We need to examine the data journey from end to end - the column names, the data types, etc, and verify that they conform to the specification <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: data_journey <br/><br/> REFERENCES_STORY: System_refactor  
- TASK_NAME: Analytics <br/><br/> TASK_DESCRIPTION: Here we develop the analytics infrastructure for responding to question 1.1 <br/><br/> COMMENTS: Actually we built the analysis for all the answers yet there is a lot to be done in maintainability etc <br/><br/>  TASK_ID: analytics1 <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Pipeline <br/><br/> TASK_DESCRIPTION: We develop the pipeline that produces the clean data <br/><br/> COMMENTS: THERE IS NEED FOR HEAVY REFACTORING!! Also unit tests will be added afterwards <br/><br/>  TASK_ID: pipeline1 <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Acceptance test <br/><br/> TASK_DESCRIPTION: Write the acceptance tests for this story that responds to question 1.1 <br/><br/> COMMENTS: In order to do so we have to modify the solution we have created right before <br/><br/>  TASK_ID: acceptance_test <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Docker deployment <br/><br/> TASK_DESCRIPTION: Create a set of docker containers for deployment <br/><br/> COMMENTS: We got just one container in order to avoid the trouble of communication between separate processes - at least for now <br/><br/>  TASK_ID: docker1 <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Requirements and solution <br/><br/> TASK_DESCRIPTION: The objective is to gather all the requirements and come up with a proposed architectural solution to be implemented. Capture everything in a document<br/><br/> COMMENTS:  <br/><br/>  TASK_ID: r_n_s <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Create_first_story <br/><br/> TASK_DESCRIPTION: USE the info from the problem description and write the first story  <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: first_story  <br/><br/> REFERENCES_STORY: tech1  
- TASK_NAME: Update_readme <br/><br/> TASK_DESCRIPTION: Collect all the necessary info from the problem description in the README <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: initial_readme  <br/><br/> REFERENCES_STORY: tech1  
- TASK_NAME: Setup_kanban <br/><br/> TASK_DESCRIPTION: To setup the Kanban board for the project <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: kanban1  <br/><br/> REFERENCES_STORY: tech1  

