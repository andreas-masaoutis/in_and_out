"""Testing the SQL queries
We have implemented tests for two (2) of the queries
"""

import unittest
from rules_n_fixes import *


class RulesNFixesTests(unittest.TestCase):
    """Testing the rules and fixes for the pipeline"""
    
    def test_valid_check_user_id_format(self):
        """The valid user_id case"""

        VALID_USER_ID = 'p3b4e81f-79de-4937-ba87-aec8e7e731af'
        self.valid_id = check_user_id_format(VALID_USER_ID)

        self.assertTrue(self.valid_id)


    def test_short_check_user_id_format(self):
        """An invalid user_id case: shorter"""

        SHORT_USER_ID = 'p3b4e81f-79de-4937-ba87-aec8e7e71af'
        self.short_id = check_user_id_format(SHORT_USER_ID)

        self.assertFalse(self.short_id)


    def test_empty_check_user_id_format(self):
        """An invalid user_id case: empty"""

        EMPTY_USER_ID = ''
        self.empty_id = check_user_id_format(EMPTY_USER_ID)

        self.assertFalse(self.empty_id)


    def test_valid1_check_event_type(self):
        """A valid event type: GATE_IN"""

        VALID_EVENT_TYPE = "GATE_IN"
        self.valid_event_type = check_event_type(VALID_EVENT_TYPE, ["GATE_IN","GATE_OUT"] )

        self.assertTrue(self.valid_event_type)
    
    def test_invalid_check_event_type(self):
        """A valid event type: GATE_OUT"""

        INVALID_EVENT_TYPE = "GATE_OUt"
        self.invalid_event_type = check_event_type(INVALID_EVENT_TYPE, ["GATE_IN","GATE_OUT"] )

        self.assertFalse(self.invalid_event_type)

    def test_empty_check_event_type(self):
        """An invalid event type: empty """

        EMPTY_EVENT_TYPE = ""
        self.empty_event_type = check_event_type(EMPTY_EVENT_TYPE, ["GATE_IN","GATE_OUT"] )

        self.assertFalse(self.empty_event_type)


    def test_missing_event_in_sds(self):
        """Missing events (eg exit without entry) in the Special Data Structure"""

        sds = {
            'good_user' : {
                'GATE_IN' : [
                    datetime.strptime('2023-01-31T08:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ],
                'GATE_OUT' : [
                    datetime.strptime('2023-01-31T09:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ], 
            },
            'bad_user' : {
                'GATE_IN' : [
                    datetime.strptime('2023-01-31T08:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ],
                'GATE_OUT' : [
                    datetime.strptime('2023-01-31T09:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ"),
                    datetime.strptime('2023-01-31T15:12:52.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ], 
            }
        }
        
        self.missing_event = check_entry_exit_sequence_and_no_duplicates(sds)

        self.assertEqual(self.missing_event, (['good_user'], ['bad_user']) )


    def test_duplicates_in_sds(self):
        """Duplicate rows in CSV -> duplicates in the Special Data Structure"""

        sds = {
            'good_user' : {
                'GATE_IN' : [
                    datetime.strptime('2023-01-31T08:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ],
                'GATE_OUT' : [
                    datetime.strptime('2023-01-31T09:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ], 
            },
            'bad_user' : {
                'GATE_IN' : [
                    datetime.strptime('2023-01-31T08:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ"),
                    datetime.strptime('2023-01-31T08:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ],
                'GATE_OUT' : [
                    datetime.strptime('2023-01-31T09:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ"),
                    datetime.strptime('2023-01-31T09:18:36.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")
                ], 
            }
        }
        
        self.duplicate_rows = check_entry_exit_sequence_and_no_duplicates(sds)

        self.assertEqual(self.duplicate_rows, (['good_user'], ['bad_user']) )



if __name__ == "__main__":
    unittest.main()
