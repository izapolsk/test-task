# test-task

This repo contains an implementation of test task.
It has the following structure:
- lib/views - widgetastic views covering login/board/card pages and modals
- lib/widgets - widgetastic widgets
- tests - tests itself
- tests/smoke_test.py - the file with tests for given automation task
- utils - utilities needed for testing like set up logging and etc
- requirements.txt - list of essential python packages for running tests
- Dockerfile - dockerfile for building container with all essential stuff for running tests


There many ways to run existing smoke tests. 
The smoothest one is to use pre-built docker container or build it from scratch.
The way with pre-built container is
```shell script
docker pull docker.io/ez999/test-task:latest
docker run -it --shm-size=512m docker.io/ez999/test-task:latest
``` 
or image can be built and run locally
```shell script
git clone https://github.com/izapolsk/test-task.git ~/test-task
cd ~/test-task
docker build -f Dockerfile -t test-task:latest .
docker run -it --shm-size=512m test-task:latest
```

Expected output is 
```
[root@e5767ded22f0 sprintboards]# pytest -m smoke -s tests/
============================================================================================================ test session starts =============================================================================================================
platform linux -- Python 3.7.6, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /sprintboards, inifile: pytest.ini
collected 2 items

tests/smoke_test.py 2020-03-31 14:35:42.072 | INFO     | tests.smoke_test:browser:24 - openning chrome browser
2020-03-31 14:35:43.252 | INFO     | tests.smoke_test:browser:31 - step 1. Go to https://sprintboards.io/auth/login
2020-03-31 14:35:44.168 | INFO     | tests.smoke_test:login:42 - Step 2. Type "***@gmail.com" in “Email Address” field
2020-03-31 14:35:44.168 | INFO     | tests.smoke_test:login:43 - Step 3. Type “***” as password in “Password” field
2020-03-31 14:35:44.168 | INFO     | tests.smoke_test:login:44 - Step 4. Click “Login”
2020-03-31 14:35:47.803 | INFO     | tests.smoke_test:board:57 - Step 5. Click “CREATE BOARD”
2020-03-31 14:35:50.018 | INFO     | tests.smoke_test:board:61 - Verifying Expected Result 5.1. User is taken to https://sprintboards.io/boards/create
2020-03-31 14:35:50.025 | INFO     | tests.smoke_test:board:66 - Verifying Expected Result 5.2. “Create a Board” title is displayed
2020-03-31 14:35:50.031 | INFO     | tests.smoke_test:board:71 - Step 6. Type “My first board” in “Session Name” field
2020-03-31 14:35:57.194 | INFO     | tests.smoke_test:board:73 - Step 7. Click “Create Board” button
2020-03-31 14:35:58.136 | INFO     | tests.smoke_test:board:77 - Verifying Expected Result 7.1. User gets a confirmation pop-up saying “Created”
2020-03-31 14:35:58.187 | INFO     | tests.smoke_test:board:81 - Verifying Expected Result 7.2. URL contains “https://sprintboards.io/boards”
2020-03-31 14:35:58.190 | INFO     | tests.smoke_test:test_create_green_card:97 - Step 8. Click green “+” button
2020-03-31 14:36:02.741 | INFO     | tests.smoke_test:test_create_green_card:101 - Verifying Expected Result 8.1. A modal with title “Add a Card” is displayed
2020-03-31 14:36:02.764 | INFO     | tests.smoke_test:test_create_green_card:104 - Step 9. Type “Goal was achieved” as title
2020-03-31 14:36:02.764 | INFO     | tests.smoke_test:test_create_green_card:105 - Step 10. Type “Sprint was well planned” as description
2020-03-31 14:36:04.775 | INFO     | tests.smoke_test:test_create_green_card:107 - Step 11. Click “Add Card” button
2020-03-31 14:36:06.743 | INFO     | tests.smoke_test:test_create_green_card:112 - Verifying Expected Result 11. Card is added with the title and description specified in steps 9 and 10
.2020-03-31 14:36:06.882 | INFO     | tests.smoke_test:test_create_delete_red_card:128 - Step 12. Click red “+” button
2020-03-31 14:36:08.643 | INFO     | tests.smoke_test:test_create_delete_red_card:132 - Verifying Expected Result 12.1. A modal with title “Add a Card” is displayed
2020-03-31 14:36:08.670 | INFO     | tests.smoke_test:test_create_delete_red_card:135 - Step 13. Type “Goal was not achieved” as title
2020-03-31 14:36:09.754 | INFO     | tests.smoke_test:test_create_delete_red_card:137 - Step 14. Click “Add Card” button
2020-03-31 14:36:12.010 | INFO     | tests.smoke_test:test_create_delete_red_card:142 - Verifying Expected Result 14.1 Card is added with the title specified in step 13
2020-03-31 14:36:12.010 | INFO     | tests.smoke_test:test_create_delete_red_card:143 - Verifying Expected Result 14.2 Card’s description is set to “No description provided.”
2020-03-31 14:36:12.278 | INFO     | tests.smoke_test:test_create_delete_red_card:152 - Step 15. Click thumbs up icon for the card in the first column
2020-03-31 14:36:12.740 | INFO     | tests.smoke_test:test_create_delete_red_card:154 - Expected Result 15. “Likes” count goes from 0 to 1
2020-03-31 14:36:14.303 | INFO     | tests.smoke_test:test_create_delete_red_card:156 - Step 16. Click “x Delete” button from the card in the second column
2020-03-31 14:36:15.042 | INFO     | tests.smoke_test:test_create_delete_red_card:158 - Verifying Expected Result 16. Modal appears with the following text: • “Delete Card” • “Are you sure you want to continue?”
2020-03-31 14:36:15.464 | INFO     | tests.smoke_test:test_create_delete_red_card:168 - Step 17. Click “Confirm” button
2020-03-31 14:36:16.186 | INFO     | tests.smoke_test:test_create_delete_red_card:170 - Expected Result 17. Card with title “Goal was not achieved” is removed from the board
.

============================================================================================================= 2 passed in 34.71s =============================================================================================================
```

NB: login and password are hardcoded in test as a temporary solution. Those have to be saved to vault/encrypted file or passed via env variables in future.
