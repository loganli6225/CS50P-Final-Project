from pathlib import Path
from datetime import datetime, date
import json
import re


def main():
    if not ensure_user_list_csv_exists():
        print("A file named User_IDs.csv has been created for this program to work. Please do not manually alter its contents at anytime.")
    while True:
        user_id = input("User ID (Please hit enter to create new user): ")
        if not (user_id == "" or re.search(r"^\d{3}$", user_id)):
            print("Not valid User ID format. Please enter a three-digit number or hit Enter.")
        elif not user_id:
            user_id = create_new_user_id()
            print(f"Your User_ID is: {user_id}")
            user_file_path = create_new_user_file(user_id)

            print(f"To set up your account, please answer the following questions.")

            user_first_name = input("First Name: ")
            while not user_first_name.isalpha():
                print("Not valid first name format. Please enter only alphabetic characters.")
                user_first_name = input("First Name: ")

            user_last_name = input("Last Name: ")
            while not user_last_name.isalpha():
                print("Not valid last name format. Please enter only alphabetic characters.")
                user_last_name = input("Last Name: ")

            user_birthdate_iso = input("Birthdate: ")
            while not validate_iso_format_date(user_birthdate_iso):
                print("Not valid birthdate format. Please enter in the format YYYY-MM-DD.")
                user_birthdate_iso = input("Birthdate: ")

            user_sex = input("Sex (M/F): ").upper()
            while user_sex != "M" and user_sex != "F":
                print("Please enter M for Male and F for Female.")
                user_sex = input("Sex (M/F): ").upper()

            user_personal_data_dict = store_personal_data(user_id, user_first_name, user_last_name, user_birthdate_iso, user_sex)

            user_personal_data_dict = update_CV_metrics(user_personal_data_dict)

            export_to_json_file(user_personal_data_dict, user_file_path)
            print("All data safely stored.")

            break
        else:
            if does_user_exists(user_id):
                TorF, user_personal_data_dict = is_correct_user(user_id)
                if TorF:
                    if check_date_exists(date.today().isoformat(), user_personal_data_dict)[0]:
                        print(f"Hi {user_personal_data_dict['first_name']}! Today's data has already been inputed. Please return tomorrow to input new data.")
                    else:
                        user_personal_data_dict = update_CV_metrics(user_personal_data_dict)
                        export_to_json_file(user_personal_data_dict, Path(f"{user_id}_CV_Data.json"))
                        print("All data safely stored.")

                    break
                else:
                    print("The User ID you provided is not yours. Please try again.")
            else:
                print("User does not exist. Please try again.")

    while True:
        view = input("Would you like to view your metrics from a certain date? (Y/N): ").upper()
        while view == "Y":
                print(view_data_from(user_personal_data_dict))
                view = input("Would you like to view a different date? (Y/N): ").upper()

        if view == "N":
            print("All data safely stored.")
            break
        else:
            print("Please answer Y or N.")

    print(f"Please remember your User ID: {user_id}. Thank you.")


def ensure_user_list_csv_exists():
    user_list_csv_path = Path("User_IDs.csv")
    if not user_list_csv_path.is_file():
        with open(user_list_csv_path, "w") as file:
            file.write(f"User IDs (DO NOT MANUALLY ALTER THIS FILE)")
        return False
    else:
        return True


def create_new_user_id():
    with open("User_IDs.csv", "r") as file:
        reader = file.read().splitlines()
        if len(reader) == 1:
            user_id = 100
        else:
            user_id = int(reader[-1]) + 1
    with open("User_IDs.csv", "a") as file:
        file.write(f"\n{user_id}")
    return user_id


def create_new_user_file(id):
    user_file_path = Path(f"{id}_CV_Data.json")
    user_file_path.touch()
    return user_file_path


def store_personal_data(id, first_name, last_name, birthdate_iso, sex):
    return {
        "user_id": id,
        "first_name": first_name,
        "last_name": last_name,
        "birthdate": birthdate_iso,
        "age": calculate_age(birthdate_iso),
        "sex": sex,
        "data": [
        ],
    }


def calculate_age(birthdate_iso):
    birthdate_date = date.fromisoformat(birthdate_iso)
    today = date.today()
    if (birthdate_date.month > today.month) or (birthdate_date.month == today.month and birthdate_date.day > today.day):
        age = today.year - birthdate_date.year - 1
    else:
        age = today.year - birthdate_date.year
    return age


def update_CV_metrics(personal_data_dict):
    while True:
        _ = input(f"Hi {personal_data_dict['first_name']}! Would you like to input health data for today? (Y/N): ").upper()
        if _ == "Y":
            user_rhr = input("Resting Heart Rate: ")
            while not user_rhr.isdecimal():
                print("Not valid resting heart rate input. Please enter an integer.")
                user_rhr = input("Resting Heart Rate: ")
            user_rhr = int(user_rhr)

            user_bp = input("Blood Pressure: ")
            while not re.search(r"^\d{2,3}/\d{2,3}$", user_bp):
                print("Not valid blood pressure input. Please enter in the accepted format integer/integer.")
                user_bp = input("Blood Pressure: ")

            user_hrr = input("Heart Rate Recovery: ")
            while not user_hrr.isdecimal():
                print("Not valid heart rate recovery input. Please enter an integer.")
                user_hrr = input("Heart Rate Recovery: ")
            user_hrr = int(user_hrr)

            new_CV_metrics = store_new_CV_metrics(user_rhr, user_bp, user_hrr)
            personal_data_dict["data"].append(new_CV_metrics)
            return personal_data_dict
        elif _ == "N":
            return personal_data_dict
        else:
            print("Please answer Y or N.")


def store_new_CV_metrics(rhr, bp, hrr):
    time_and_date_naive = datetime.now().isoformat(timespec = "seconds")
    (bp_systolic, bp_diastolic) = bp.split("/")
    bp_systolic = int(bp_systolic)
    bp_diastolic = int(bp_diastolic)

    return {
        "timestamp": time_and_date_naive,
        "rhr": rhr,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "hrr": hrr,
    }


def export_to_json_file(personal_data_dict, file_path):
    with open(file_path, "w") as file:
        return json.dump(personal_data_dict, file, indent = 4)


def does_user_exists(id):
    with open("User_IDs.csv", "r") as file:
        for line in file:
            if line.strip() == id:
                return True
    return False


def is_correct_user(id):
    personal_data_dict = import_from_json_file(id)
    while True:
        q1 = input(f"Is your name {personal_data_dict['first_name']} {personal_data_dict['last_name']}? (Y/N): ").upper()
        if q1 == "Y":
            while True:
                q2 = input(f"Is your birthdate {personal_data_dict['birthdate']}? (Y/N): ").upper()
                if q2 == "Y":
                    return (True, personal_data_dict)
                elif q2 == "N":
                    return (False, None)
                else:
                    print("Please answer Y or N.")
        elif q1 == "N":
            return (False, None)
        else:
            print("Please answer Y or N.")


def import_from_json_file(id):
    file_path = Path(f"{id}_CV_Data.json")
    with open(file_path, "r") as file:
        personal_data_dict = json.load(file)
        personal_data_dict["age"] = calculate_age(personal_data_dict["birthdate"])
        return personal_data_dict


def check_date_exists(date, personal_data_dict):
    for entry in personal_data_dict["data"]:
        if entry["timestamp"].startswith(date):
            return (True, entry)
    return (False, None)


def return_metrics(entry_dict):
    if matches := re.search(r"^\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", entry_dict["timestamp"]):
        return (matches.group(1), entry_dict["rhr"], entry_dict["bp_systolic"], entry_dict["bp_diastolic"], entry_dict["hrr"])


def view_data_from(personal_data_dict):
    date = input("Which date's metrics would you like to view? (Please enter date in YYYY-MM-DD format): ")
    while not validate_iso_format_date(date):
        print("Not valid date format. Please enter in the format YYYY-MM-DD.")
        date = input("Which date's metrics would you like to view? (Please enter date in YYYY-MM-DD format): ")
    does_date_exist = check_date_exists(date, personal_data_dict)
    if does_date_exist[0]:
        returned_data = return_metrics(does_date_exist[1])
        return f"On {date} at {returned_data[0]}, your resting heart rate was {returned_data[1]} BPM, your blood pressure was {returned_data[2]}/{returned_data[3]} mmHg, and your heart rate recovery was {returned_data[4]} BPM."
    else:
        return f"Metrics from this date do not exist."


def validate_iso_format_date(input_date):
    try:
        date.fromisoformat(input_date)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
