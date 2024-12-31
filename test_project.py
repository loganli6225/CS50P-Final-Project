from project import store_personal_data, calculate_age, store_new_CV_metrics, check_date_exists, return_metrics, validate_iso_format_date
from freezegun import freeze_time

def test_store_personal_data():
    ### Assume calculate_age function is working correctly
    birthdate = "1999-12-31"
    expected_correct_age = calculate_age(birthdate)

    assert store_personal_data(100, "John", "Williams", "1999-12-31", "M") == {
        "user_id": 100,
        "first_name": "John",
        "last_name": "Williams",
        "birthdate": "1999-12-31",
        "age": expected_correct_age,
        "sex": "M",
        "data": [
        ],
    }


@freeze_time("2024-08-30")
def test_calculate_age():
    assert calculate_age("1995-01-01") == 29
    assert calculate_age("2000-08-30") == 24
    assert calculate_age("2000-08-31") == 23
    assert calculate_age("2000-09-01") == 23
    assert calculate_age("2000-02-29") == 24
    assert calculate_age("2024-08-30") == 0
    assert calculate_age("2024-01-01") == 0
    assert calculate_age("1800-01-01") == 224


def test_store_new_CV_metrics():
    with freeze_time("2024-08-31 3:59:59"):
        assert store_new_CV_metrics(40, "120/80", 20) == {
        "timestamp": "2024-08-31T03:59:59",
        "rhr": 40,
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "hrr": 20,
    }

    with freeze_time("2024-08-31 3:59:59", tz_offset = -4):
        assert store_new_CV_metrics(60, "125/88", 15) == {
        "timestamp": "2024-08-30T23:59:59",
        "rhr": 60,
        "bp_systolic": 125,
        "bp_diastolic": 88,
        "hrr": 15,
    }


def test_check_date_exists():
    test_data_dict = {
        "user_id": 129,
        "first_name": "John",
        "last_name": "Williams",
        "birthdate": "2000-01-01",
        "age": 24,
        "sex": "M",
        "data": [
            {
                "timestamp": "2024-08-29T21:37:23",
                "rhr": 40,
                "bp_systolic": 120,
                "bp_diastolic": 80,
                "hrr": 12
            },
            {
                "timestamp": "2024-08-30T23:59:59",
                "rhr": 60,
                "bp_systolic": 125,
                "bp_diastolic": 85,
                "hrr": 20
            }
        ]
    }
    assert check_date_exists("2024-08-29", test_data_dict) == (True, {
        "timestamp": "2024-08-29T21:37:23",
        "rhr": 40,
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "hrr": 12
    })
    assert check_date_exists("2024-08-30", test_data_dict) == (True, {
        "timestamp": "2024-08-30T23:59:59",
        "rhr": 60,
        "bp_systolic": 125,
        "bp_diastolic": 85,
        "hrr": 20
    })
    assert check_date_exists("2024-08-31", test_data_dict) == (False, None)

    empty_test_data_dict = {
        "user_id": 129,
        "first_name": "John",
        "last_name": "Williams",
        "birthdate": "2000-01-01",
        "age": 24,
        "sex": "M",
        "data": []
    }
    assert check_date_exists("2024-08-29", empty_test_data_dict) == (False, None)


def test_return_metrics():
    test_entry_1 = {
        "timestamp": "2024-08-29T21:37:23",
        "rhr": 40,
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "hrr": 12
    }
    assert return_metrics(test_entry_1) == ("21:37:23", 40, 120, 80, 12)

    test_entry_2 = {
        "timestamp": "2024-08-30T23:59:59",
        "rhr": 60,
        "bp_systolic": 125,
        "bp_diastolic": 85,
        "hrr": 20
    }
    assert return_metrics(test_entry_2) == ("23:59:59", 60, 125, 85, 20)


def test_validate_iso_format_date():
    assert validate_iso_format_date("2024-08-29") == True
    assert validate_iso_format_date("08-29-2024") == False
    assert validate_iso_format_date("2024-08-32") == False
    assert validate_iso_format_date("2024/08/29") == False
    assert validate_iso_format_date("2024-02-29") == True
    assert validate_iso_format_date("not-valid-date") == False
    assert validate_iso_format_date("") == False
