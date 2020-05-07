import set_test_path
import unittest
from data_manager import DataManager
from data_manager import Database
import sqlite3
import os
from datetime import datetime
from unittest import mock
from testing_resources import TestingShortcuts
from io import StringIO
from app import ConsoleUI
from contextlib import redirect_stdout

class TestUserInterface(TestingShortcuts, unittest.TestCase):

    #General
    APPOINTMENT_CLASS = "1"
    CUSTOMER_CLASS = "2"
    EXIT_APP = "9"
    RETURN_SCREEN = "9"
    #Customer class
    CREATE_CUSTOMER = "1"
    READ_CUSTOMER = "2"
    UPDATE_CUSTOMER = "3"
    EXCLUDE_CUSTOMER = "4"
    #Appointment class
    CREATE_APPOINTMENT = "1"
    READ_APPOINTMENT = "2"
    UPDATE_APPOINTMENT = "3"
    EXCLUDE_APPOINTMENT = "4"

    INPUTS_SELECT_ACTION_CREATE_CUSTOMERS = [CUSTOMER_CLASS, CREATE_CUSTOMER]

    def setUp(self):
        db_file = "YourAppointment.db"
        if os.path.exists(db_file):
            os.remove(db_file)
        self.dm = DataManager()
        with redirect_stdout(StringIO()) as stdout:
            self.dm.db.create_table_customer()
        self.console_ui = ConsoleUI()

    def test_execute_customer_action_create_customer(self):
        create_customer_id_1_inputs = self.INPUTS_SELECT_ACTION_CREATE_CUSTOMERS + self.RIGHT_INPUTS_CUSTOMER_ID_1
        try:
            with redirect_stdout(StringIO()) as stdout:
                with mock.patch('builtins.input', side_effect=create_customer_id_1_inputs):
                    self.console_ui.initialize()
        except StopIteration:
            self.shortcut_console_ui_test_if_customer_in_db_by_id(self.DB_RIGHT_RETURN_CUSTOMER_ID_1)


    def test_execute_customer_action_create_2_customers(self):
        self.test_execute_customer_action_create_customer()
        create_customer_id_1_inputs = self.INPUTS_SELECT_ACTION_CREATE_CUSTOMERS + self.RIGHT_INPUTS_CUSTOMER_ID_2
        try:
            with redirect_stdout(StringIO()) as stdout:
                with mock.patch('builtins.input', side_effect=create_customer_id_1_inputs):
                    self.console_ui.initialize()
        except StopIteration:
            self.shortcut_console_ui_test_if_customer_in_db_by_id(self.DB_RIGHT_RETURN_CUSTOMER_ID_2)

if __name__ == "__main__":
    unittest.main()