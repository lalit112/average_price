"""
Module for getting json data
"""

# import modules
import collections
import json


class CreateJson:
    """
    Class for creating json from sql rows
    """
    def __init__(self, cursor):
        """
        Instance variable initializer for class
        :param cursor: cursor object
        """
        self.cursor = cursor

    def create_json(self):
        """
        Function for creating json data from cursor object
        :return: json data
        """
        data = self.cursor.fetchall()
        output_list = []
        for row in data:  # creating a list of dictionary for getting proper output format
            dict_row = collections.OrderedDict()
            dict_row["day"] = row[0]
            dict_row["average_price"] = row[1]
            output_list.append(dict_row)
        return json.dumps(output_list, default=str)
