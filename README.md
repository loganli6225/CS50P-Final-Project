# Cardiovascular Health Data Storer
### Video Demo: [https://youtu.be/xQcuDKOgMaE](https://youtu.be/xQcuDKOgMaE)
## Description:
This project is an interactive program for users to store daily cardiovascular health metrics and to view past metrics. The current version supports use by multiple users and the storage of a user's daily resting heart rate, blood pressure, and heart rate recovery. The program's code is written in the file `project.py` and unit tests for the program's functions are written in the file `test_project.py`. Required third-party python libraries to install are listed in the file `requirements.txt`. Each user's personal data and daily cardiovascular health metrics are stored and updated in a personally unique json file, created when a new user is created. These json files are in the format `id_CV_Data.json`, where _id_ is the specific user's User ID number. For the program to correctly function, it requires a csv file named `User_IDs.csv` to store existing User IDs. This file is created the first time the program is used and should never be manually altered in any way.

Further improvements include supporting the storing of additional health metrics, improving the security of user's data, and supporting analysis and visualization of health data to detect abnormalities. Eventually, this program would be integrated into an user-friendly medical device that can measure a wide range of cardiovascular health metrics, safely store personal and health data, and accurately detect abnormalities and alert users to seek medical help if needed.

## Libraries:
This project currently uses six libraries: `pathlib`, `datetime`, `json`, `re`, `pytest`, and `freezegun`. The main program, `project.py`, uses `pathlib` for filesystem paths and file I/O operations; `datetime` for handling date and time operations; `json` for serializing and deserializing json files; and `re` for regular expression support during input validation. The unit test program uses `pytest` to run unit testing and `freezegun` to mock dates and times for unit testing. To install all necessary third-party libraries not part of the Python Standard Library, please use the command line command:

```pip install -r requirements.txt```

## Functionality:
The program currently uses a main function and 15 additional helper functions. Each function and its description is included below.

### `main` Function
The main function is the core of the program, as it calls many of the helper functions to perform the program's role. It also handles printing messages for the user, handling various user answers to questions, and asking for personal information inputs with input validation support. Its current structure is composed of two sections: 1) for storing new cardiovascular health data of a user, 2) for viewing past cardiovascular health data of a user. Furthermore, the first section is composed of two different possible sub-scenarios: 1) for creating a new user and storing both personal information and new cardiovascular health data, 2) for accessing an old user and storing new cardiovascular health data.

### `ensure_user_list_csv_exists` Function
This function is used to ensure the file `User_IDs.csv` exists. This file is necessary for the program's functionality as existing User IDs are stored in this file. The function returns True if the file `User_IDs.csv` exists. If the file does not exist, the function creates the file with a header and returns False.

### `create_new_user_id` Function
This function reads the file `User_IDs.csv` to determine the new user's User ID. If the file is empty (besides the header), the new user's User ID is set to 100. If the file already stores other User IDs, the new user's User ID is set to one more than the last stored User ID. The function returns the new user's User ID and writes it in the file to be safely stored.

### `create_new_user_file` Function
This function takes a new user's User ID as input and creates a json file for the new user to store their data. The json file created is named in the format `id_CV_Data.json`, where _id_ is the new user's id number.

### `store_personal_data` Function
This function creates and returns a personal dictionary storing a new user's User ID, first name, last name, birthdate in isoformat, age, sex, and an empty data list. The function's inputs are the new user's User ID, first name, last name, birthdate in isoformat, and sex. The function calls on the function `calculate_age` to calculate the user's most-up-to-date age.

### `calculate_age` Function
This function accurately calculates a user's age using the user's birthdate in isoformat as input. The function uses the local time's current date of when the function is called to calculate the user's age.

### `update_CV_metrics` Function
This function, takes as input a user's personal dictionary containing their personal information and health data, and is used for acquiring a user's cardiovascular health data for the day and safely storing the inputted data into the user's personal dictionary. The function asks the user if they want to input their cardiovascular health data for the day. If the user answers `Y` or `y` for _Yes_, the function prompts the user to input their various health data one at a time, with input validification. The function will then call the function `store_new_CV_metrics` to store the inputted data into a new dictionary, which is appended to the data list within the user's personal dictionary for storage. Finally, the updated user personal dictionary is returned. If the user answers `N` or `n` for _No_, the function ends and returns the current up-to-date user personal dictionary. If the user answers with anything else, the function prompts the user to answer again until a valid answer is inputted.

### `store_new_CV_metrics` Function
This function takes a user's inputted health data and returns it neatly formatted in a dictionary along with the timestamp of when the function was called, down to the current second. The current version supports inputs of resting heart rate, blood pressure, and heart rate recovery, and returns the timestamp, resting heart rate, systolic blood pressure, diastolic blood pressure, and heart rate recovery in a dictionary.

### `export_to_json_file` Function
This function updates and stores a user's personal json file with their up-to-date personal information and cardiovascular health metrics data. It takes as input the user's up-to-date personal dictionary and their personal json file's file path, in the format `id_CV_Data.json` where _id_ is the user's id number. It then exports and safely stores the dictionary's information into the json file in a neat json format.

### `does_user_exists` Function
This function reads the file `User_IDs.csv` to determine if the inputted User ID exists and is stored within the file. It returns True if the User ID exists and is stored, and returns False if the User ID does not exist and is not stored.

### `is_correct_user` Function
This function asks the user two clarifying questions to ensure they are accessing the correct user information. Using the inputted User ID, the function calls the `import_from_json_file` function to access the corresponding user's personal json file, in the format `id_CV_Data.json` where _id_ is the User ID number, to deserialized and return its contents in the format of a python dictionary. The function then asks the user if their name and birthdate are as stored in the json file, by accessing the deserialized dictionary. If the user answers `Y` or `y` for _Yes_ to both questions, the function returns True and the user's personal dictionary (deserialized from the json file) in the form of a tuple. If the user answers `N` or `n` for _No_ to either question, the function returns False and None in the form of a tuple. If the user answers with anything else to either question, the function prompts the user to answer again until a valid answer is inputted.

### `import_from_json_file` Function
This function takes a user's User ID as input, and deserializes the ID's corresponding json file, in the format `id_CV_Data.json` where _id_ is the User ID number, into the user's personal dictionary containing their information and data. The function then updates the user's age stored in the dictionary by calling the `calculate_age` function, and returns this updated deserialized dictionary.

### `check_date_exists` Function
This function takes as input a date in isoformat and a user's personal dictionary containing their information and data. The function then accesses the dictionary's data list, which stores all the user's daily cardiovascular health data in separate entry dictionaries, and scans each entry dictionary within the data list. If an entry dictionary is found with a timestamp of the inputted date, the function returns True and the entry dictionary in the form of a tuple. If no entry dictionary is found with a timestamp of the inputted date, the function returns False and None in the form of a tuple.

### `return_metrics` Function
This function takes as input an entry dictionary containing a user's cardiovascular data for a single day, and returns the time-portion of the timestamp and each stored cardiovascular data from the dictionary in the form of a tuple. The current version supports returning the time, the resting heart rate, the systolic blood pressure, the diastolic blood pressure, and the heart rate recovery in the form of a tuple.

### `view_data_from` Function
This function aims to return a user's cardiovascular health data from a certain date in a user-friendly message by taking as input a user's personal dictionary containing their information and data. The function asks the user for a date they would like to view their data from, and validates it is in isoformat. If the inputted date is not in isoformat, the function reprompts the user to input a date until it is in isoformat. The function then calls the `check_date_exists` function to validate an entry containing health data exists from that date and is stored within the user's personal dictionary. If an entry does exist from that date, the function calls the `return_metrics` function to effectively access the time and cardiovascular data of that entry. The function finally returns a user-friendly message stating the user's various cardiovascular health metrics on that date and time. If the `check_date_exists` function determines an entry from the inputted date does not exist within the user's personal dictionary, the function returns a message stating no metrics exist from that date.

### `validate_iso_format_date` Function
This function returns True if the input date is in isoformat and returns False if the input date is not in isoformat.

## Unit Tests:
The program currently has 6 unit tests to test the 6 functions: `store_personal_data`, `calculate_age`, `store_new_CV_metrics`, `check_date_exists`, `return_metrics`, and `validate_iso_format_date`. A description of each current unit test is below. A further improvement to this project is writing additional unit tests for the other functions.

### `test_store_personal_data` Unit Test
This unit test tests if the function `store_personal_data` works as expected in returning a dictionary containing a user's personal information. All inputs are assumed to have passed prior validation and to be in the correct format. Furthermore, as the `store_personal_data` function calls the `calculate_age` function, this unit test assumes the `calculate_age` function is working properly.

### `test_calculate_age` Unit Test
This unit test tests if the function `calculate_age` works as expected in calculating and returning a user's current age from their birthdate in isoformat. This unit test utilizes the `freeze_time` decorator from the `freezegun` library to mock the date of `date.today()`.

### `test_store_new_CV_metrics` Unit Test
This unit test tests if the function `store_new_CV_metrics` works as expected in returning a dictionary containing a user's inputted cardiovascular health data and a timestamp from the certain moment the function is called, regardless of the user's local time zone. All inputs are assumed to have passed prior validation and to be in the correct format. The unit test utilizes the `freeze_time` context manager from the `freezegun` library to mock the date and time of `datetime.now()`.

### `test_check_date_exists` Unit Test
This unit test tests if the function `check_date_exists` works as expected in returning a tuple based on whether the inputted user's personal dictionary contains a data dictionary from the inputted date (in isoformat) within its nested "data" list. More specifically, when the user's personal dictionary does contain a data dictionary from the specified date within its nested "data" list, the unit test tests whether the function `check_date_exists` returns a tuple containing True and the specified data dictionary from that date. On the other hand, when the user's personal dictionary does not contain a data dictionary from the specified date within its nested "data' list, the unit test tests whether the function `check_date_exists` returns a tuple containing False and None. To mock the input of an expected dictionary, fake dictionaries with valid possible key-value pairs were created and used within the unit test.

### `test_return_metrics` Unit Test
This unit test tests if the function `return_metrics` works as expected in returning a tuple containing the time of a timestamp and each individual cardiovascular health metric from the input of a dictionary containing a user's cardiovascular data for an individual day. To mock the input of an expected dictionary, fake dictionaries with valid possible key-value pairs were created and used within the unit test.

### `test_validate_iso_format_date` Unit Test
This unit test tests if the function `validate_iso_format_date` works as expected in returning True when an input date is in isoformat and in returning False when an input date is not in isoformat.

### Functions Without A Unit Test
A unit test for `ensure_user_list_csv_exists` requires mocking file I/O operations.

A unit test for `create_new_user_id` requires mocking file I/O operations.

A unit test for `create_new_user_file` requires mocking file I/O operations.

A unit test for `update_CV_metrics` requires mocking user input and helper functions (store_new_CV_metrics).

A unit test for `export_to_json_file` requires mocking file I/O operations.

A unit test for `does_user_exists` requires mocking file I/O operations.

A unit test for `is_correct_user` requires mocking user input and helper functions (import_from_json_file).

A unit test for `import_from_json_file` requires mocking file I/O operations and helper functions (calculate_age).

A unit test for `view_data_from` requires mocking user input and helper functions (validate_iso_format_date, check_date_exists, return_metrics).

## Author:
Logan Li, a current undergraduate bioengineering student at the University of California, San Diego (UCSD). LinkedIn: [www.linkedin.com/in/logan-li-ucsd](www.linkedin.com/in/logan-li-ucsd). This project was completed to improve my python coding skills and as an assignment for Harvard's free online course, [CS50P Introduction to Programming with Python](https://cs50.harvard.edu/python/2022/).
