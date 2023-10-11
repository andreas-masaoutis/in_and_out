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

- STORY_NAME: Architectural spike <br/><br/> STORY_DESCRIPTION: We need to create a first iteration in order to test the viability of proposed architectures. We should deliver a response to  question 1.1 (total_time_in_office). This story has many tasks that cover the whole range of tasks from specifying requirements to deployment. <br/><br/> STATUS: Running  <br/><br/>  STORY_ID: Arch_spike  
- STORY_NAME: Bootstrap_the_Project <br/><br/> STORY_DESCRIPTION: All the necessary first steps in order to initiate the project <br/><br/> STATUS: Completed <br/><br/>  STORY_ID: tech1  

### Tasks

- TASK_NAME: Guards <br/><br/> TASK_DESCRIPTION: The code only covers a happy path with no exception handling - cover for all cases <br/><br/> COMMENTS: Not only the solution but the integration tests too <br/><br/>  TASK_ID: guards <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Logging <br/><br/> TASK_DESCRIPTION: Until now necessary info for the user is just printed on screen - Redirect everything to a log <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: logging <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Pipeline refactoring <br/><br/> TASK_DESCRIPTION: We need to move ahead in order to answer all questions otherwise the refactoring should be part of the Pipeline task <br/><br/> COMMENTS: Consider creating a Class that will handle both data and logic <br/><br/>  TASK_ID: pipeline_refactor <br/><br/> REFERENCES_STORY: Arch_spike  

### In Progress

- TASK_NAME: Analytics <br/><br/> TASK_DESCRIPTION: Here we develop the analytics infrastrucure for responding to question 1.1 <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: analytics1 <br/><br/> REFERENCES_STORY: Arch_spike  

### Done ✓

- TASK_NAME: Pipeline <br/><br/> TASK_DESCRIPTION: We develop the pipeline that produces the clean data <br/><br/> COMMENTS: THERE IS NEED FOR HEAVY REFACTORING!! Also unit tests will be added afterwards <br/><br/>  TASK_ID: pipeline1 <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Acceptance test <br/><br/> TASK_DESCRIPTION: Write the acceptance tests for this story that responds to question 1.1 <br/><br/> COMMENTS: In order to do so we have to modify the solution we have created right before <br/><br/>  TASK_ID: acceptance_test <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Docker deployment <br/><br/> TASK_DESCRIPTION: Create a set of docker containers for deployment <br/><br/> COMMENTS: We got just one container in order to avoid the trouble of communication between separate processes - at least for now <br/><br/>  TASK_ID: docker1 <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Requirements and solution <br/><br/> TASK_DESCRIPTION: The objective is to gather all the requirements and come up with a proposed architectural solution to be implemented. Capture everything in a document<br/><br/> COMMENTS:  <br/><br/>  TASK_ID: r_n_s <br/><br/> REFERENCES_STORY: Arch_spike  
- TASK_NAME: Create_first_story <br/><br/> TASK_DESCRIPTION: USE the info from the problem description and write the first story  <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: first_story  <br/><br/> REFERENCES_STORY: tech1  
- TASK_NAME: Update_readme <br/><br/> TASK_DESCRIPTION: Collect all the necessary info from the problem description in the README <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: initial_readme  <br/><br/> REFERENCES_STORY: tech1  
- TASK_NAME: Setup_kanban <br/><br/> TASK_DESCRIPTION: To setup the Kanban board for the project <br/><br/> COMMENTS:  <br/><br/>  TASK_ID: kanban1  <br/><br/> REFERENCES_STORY: tech1  

