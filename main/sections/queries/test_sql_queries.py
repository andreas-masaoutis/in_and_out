"""Testing the SQL queries
We have implemented tests for two (2) of the queries
"""

import unittest
import csv
import sqlite3
from sql_queries import NET_OFFICE_HOURS, DAYS_IN_OFFICE


class QueriesTest(unittest.TestCase):
    """Testing individual SQL queries"""

    def setUp(self):
        """The DB
        Setup the DB
        Load the initial data
        Execute the queries we want to test (they create two tables)
        """
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS in_out(user_id, event_type, event_time)"
        )

        self.insert_records = (
            "INSERT INTO in_out (user_id, event_type, event_time) VALUES(?, ?, ?)"
        )

        with open("test_data_sql_queries.csv", "r", encoding="UTF8") as self.query_data:
            self.query_data_reader = csv.reader(self.query_data)
            ## get rid of header
            next(self.query_data_reader)
            self.cur.executemany(self.insert_records, self.query_data_reader)
            self.con.commit()

        self.cur.execute(NET_OFFICE_HOURS)
        self.cur.execute(DAYS_IN_OFFICE)

    def test_net_office_hours(self):
        """Correct execution for net hours spent in the office by each employee"""

        self.actual_results = self.cur.execute(
            "SELECT * FROM net_office_hours"
        ).fetchall()

        self.desired_results = [
            ("user1g90-49ff-4512-b1c1-ee92ec9680ab", 144000),
            ("user281f-79de-4937-ba87-aec8e7e731af", 25200),
        ]

        self.assertEqual(self.actual_results, self.desired_results)

    def test_days_in_office(self):
        """Correct execution for days present in office for each employee"""

        self.actual_results = self.cur.execute(
            "SELECT * FROM days_in_office"
        ).fetchall()

        self.desired_results = [
            ("user1g90-49ff-4512-b1c1-ee92ec9680ab", 5),
            ("user281f-79de-4937-ba87-aec8e7e731af", 1),
        ]

        self.assertEqual(self.actual_results, self.desired_results)

    def tearDown(self):
        self.con.close()


if __name__ == "__main__":
    unittest.main()
