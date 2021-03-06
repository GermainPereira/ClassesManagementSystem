import set_test_path
import unittest
from unittest import mock
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime
from data_manager import DataManager as Dm


class TestingShortcuts():

    customer_register_day = datetime.now().strftime("%Y-%m-%d")
    customer_register_time = datetime.now().strftime("%H:%M")


    #RightInputs
    INDEX_OF_FORENAME = 0
    INDEX_OF_SURNAME = 1
    INDEX_OF_BIRTHDATE = 2
    INDEX_OF_PERSONAL_ID = 3
    INDEX_OF_ADDRESS_STREET_AND_NUMBER = 4
    INDEX_OF_ADDRESS_OTHER = 5
    INDEX_OF_ADDRESS_CITY = 6
    INDEX_OF_ADDRESS_STATE = 7


    RIGHT_INPUTS_CUSTOMER_ID_1 = ["João", "da Silva", "23-05-1978",
                                  "297.586.890-10", "Rua Bom Sucesso, 487",
                                  "Casa", "São Paulo", "SP"]

    RIGHT_RETURN_CUSTOMER_ID_1 = ["João", "da Silva", "João da Silva", "1978-05-23",
                                  "297.586.890-10", "Rua Bom Sucesso, 487",
                                  "Casa", "São Paulo", "SP",
                                  customer_register_day, customer_register_time, "Active"]

    DB_RIGHT_RETURN_CUSTOMER_ID_1 = (1, "João", "da Silva", "João da Silva", "1978-05-23", "297.586.890-10",
                                  "Rua Bom Sucesso, 487", "Casa", "São Paulo", "SP",
                                     customer_register_day, customer_register_time, "Active")


    RIGHT_INPUTS_CUSTOMER_ID_2 = ["Joana", "Silveira", "17-02-1972",
                                  "434.763.780-20", "Felicidade, 14", "Ap. 201",
                                 "Rio de Janeiro", "RJ"]


    RIGHT_RETURN_CUSTOMER_ID_2 = ["Joana", "Silveira", "Joana Silveira", "1972-02-17",
                                  "434.763.780-20", "Felicidade, 14", "Ap. 201",
                                 "Rio de Janeiro", "RJ",
                                  customer_register_day, customer_register_time, "Active"]

    DB_RIGHT_RETURN_CUSTOMER_ID_2 = (2, "Joana", "Silveira", "Joana Silveira", "1972-02-17", "434.763.780-20",
                                     "Felicidade, 14", "Ap. 201", "Rio de Janeiro", "RJ",
                                     customer_register_day, customer_register_time, "Active")

    ##Appointments

    RIGHT_INPUTS_APPOINTMENT_ID_1_OF_CUSTOMER_ID_1 = ["1", "07-05-2020", "15:00-16:00"]

    DB_RIGHT_RETURN_APPOINTMENT_ID_1_OF_CUSTOMER_ID_1 = (
        1, 1, "2020-05-07", "15:00-16:00", customer_register_day, customer_register_time, "Active"
    )

    def shortcut_test_add_customer_to_registry(self, inputs, expected_return):
        actual_return = self.dm_instance.customers_registry
        INDEX_LAST_ADDED_COSTUMER = -1
        expected_final_num_of_customers = self.shortcut_get_number_of_customers_in_registry() + 1
        with mock.patch('builtins.input', side_effect=inputs):
            self.dm_instance.add_customer_to_registry()
        self.assertEqual(expected_return, actual_return[INDEX_LAST_ADDED_COSTUMER])
        self.shortcut_test_if_num_of_customers_in_registry_equals(expected_final_num_of_customers)

    def shortcut_test_add_customer_handles_value_error(
            self, right_inputs, expected_return,
            index_to_insert_the_wrong_input, wrong_input, expected_exception
    ):
        inputed_inputs = right_inputs[:]
        inputed_inputs.insert(index_to_insert_the_wrong_input, wrong_input)
        with redirect_stdout(StringIO()) as stdout:
            self.shortcut_test_add_customer_to_registry(
                inputs = inputed_inputs, expected_return=expected_return
            )
        printed_messages = stdout.getvalue()
        self.assertIn(expected_exception, printed_messages)


    def shortcut_get_number_of_customers_in_registry(self):
        actual_num_of_customers = len(self.dm_instance.customers_registry)
        return actual_num_of_customers

    def shortcut_test_if_num_of_customers_in_registry_equals(self, expected_num_of_customers):
        actual_num_of_customers = self.shortcut_get_number_of_customers_in_registry()
        self.assertEqual(expected_num_of_customers, actual_num_of_customers)

    def shortcut_test_if_registry_contain_customers_list(self, list_with_expected_customers):
        self.assertEqual(list_with_expected_customers,
                         self.dm_instance.customers_registry)


    def shortcut_test_add_customer_raises_type_error(
            self, right_inputs, index_to_insert_the_wrong_input, wrong_input
    ):
        inputed_inputs = right_inputs[:]
        inputed_inputs.insert(index_to_insert_the_wrong_input, wrong_input)
        with self.assertRaises(TypeError):
            with mock.patch('builtins.input', side_effect=inputed_inputs):
                self.dm_instance.add_customer_to_registry()

    def shortcut_test_remove_customer_list_by_index(
            self, id_of_customer_to_be_removed, customer_to_be_removed
    ):
        expected_customers_num = self.shortcut_get_number_of_customers_in_registry() - 1
        with mock.patch('builtins.input', side_effect=id_of_customer_to_be_removed):
            self.dm_instance.remove_customer_by_index()
        self.assertEqual(expected_customers_num, self.shortcut_get_number_of_customers_in_registry())
        self.assertNotIn(customer_to_be_removed, self.dm_instance.customers_registry)

    def shortcut_test_remove_customer_handles_value_error(
            self, customer_to_be_removed,
            right_inputs_customer_id, index_to_insert_the_wrong_input,
            wrong_input, expected_exception
    ):
        inputed_inputs = right_inputs_customer_id[:]
        inputed_inputs.insert(index_to_insert_the_wrong_input, wrong_input)
        with redirect_stdout(StringIO()) as stdout:
            self.shortcut_test_remove_customer_list_by_index(
                inputed_inputs, customer_to_be_removed
            )
        printed_messages = stdout.getvalue()
        self.assertIn(expected_exception, printed_messages)

    def shortcut_test_remove_customer_raises_type_error(
            self, wrong_input
    ):
        customer_number_start = self.shortcut_get_number_of_customers_in_registry()
        with self.assertRaises(TypeError):
            with mock.patch('builtins.input', side_effect=wrong_input):
                self.dm_instance.remove_customer_by_index()
        self.shortcut_test_if_num_of_customers_in_registry_equals(customer_number_start)
        self.shortcut_test_if_registry_contain_customers_list(
            [self.RIGHT_RETURN_CUSTOMER_ID_1, self.RIGHT_RETURN_CUSTOMER_ID_2]
        )


    def shortcut_add_customer_to_datebase(self, right_customer_inputs, db_right_return_customer):
        with mock.patch('builtins.input', side_effect=right_customer_inputs):
            with redirect_stdout(StringIO()) as stdout:
                self.dm.add_new_customer_to_database()
        self.shortcut_test_if_customer_in_db_by_id(db_right_return_customer)

    def shortcut_test_if_customer_in_db_by_fullname(self, db_right_return_customer):
        fullname = db_right_return_customer[3]
        self.assertEqual([db_right_return_customer],
            self.dm.db.select_by_fullname(table="customers", fullname=fullname))


    def shortcut_test_if_customer_in_db_by_id(self, db_right_return_customer):
        customer_id = db_right_return_customer[0]
        self.assertEqual([db_right_return_customer],
            self.dm.db.select_by_customer_id(table="customers", customer_id=customer_id))


    def shortcut_console_ui_test_if_customer_in_db_by_id(self, db_right_return_customer):
        customer_id = db_right_return_customer[0]
        self.assertEqual([db_right_return_customer],
            self.console_ui.dm.db.select_by_customer_id(table="customers", customer_id=customer_id))


    def shortcut_test_console_ui_inputs(self, inputs, testing_function, parameter, use_printed_messages=False):
        try:
            with redirect_stdout(StringIO()) as stdout:
                with mock.patch('builtins.input', side_effect=inputs):
                    self.console_ui.initialize()
        except StopIteration:
            if use_printed_messages == False:
                testing_function(parameter)
            else:
                printed_messages = stdout.getvalue()
                testing_function(parameter, printed_messages)

    def shortcut_test_if_expected_message_in_console_stdoutput(self, expected_message, printed_messages):
        self.assertIn(expected_message, printed_messages)


    def shortcut_set_customer_to_inactive(self, db_customer):
        toList = list(db_customer)
        toList[-1] = "Inactive"
        tuple_inactived_customer = tuple(toList)
        return tuple_inactived_customer






