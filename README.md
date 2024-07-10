## Overview

### Application
Implement a team project planner tool. The tool consists of API's for
* Managing users
* Manging teams
* Managing a team board and tasks within a board 


The directory consists of base abstract classes. The goal is to implement the API methods defined in these classes
Create a module for concrete implementation of these base classes extending the base classes.
* The input and output will be JSON strings. Structure of which is mentioned in the method doc string.
* Every API needs to adhere to the constraints and raise exceptions for invalid inputs.
* The method doc, will include some additional requirements specific to the method.
### SUMMARY

The functions included in managing a team board and tasks within a board 
   * Create_board - creating the dashboard
   * Close_board - Closing the dashboard
   * add_task - Adding the tasks to the dashboard
   * Update_task - Upadating the tasks in the dashboard
   * List_boards - listing the dashboards.
   * Export_board - To provide the results


The functions included in managing users and tasks within a board 
   * Create_user - creating a new user who are not present in the list.
   * List_users - listing the all existing users.
   * Describe_user - providing an info about the user.
   * Update_user - updating the user.
   * get_user_teams - Getting the info about the teams where the users present.


The functions included in managing  and tasks within a board 
   * Create_team-Creating the teams (group of users).
   * list_teams- Listing the teams present.
   * describe_team- Providing the info about the team and users present in the team.
   * update_team - Updating the team.
   * add_users_to_team- Adding the users to the team.
   * remove_users_from_team- Removing the users from the team.
   * list_team_users- Listing the users present in the team.
