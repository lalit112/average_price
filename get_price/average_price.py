"""
Module for getting the API data
"""

# Import modules
from datetime import datetime
import psycopg2
from flask import request, Blueprint, jsonify
from utils.json_output import CreateJson
from utils.queries import SqlQuery
from db.database_connection import create_connection

# Creating blueprint
avg_price = Blueprint("avg_price", __name__)


@avg_price.route("/", methods=["GET"])
def get_average_price():
    """
    API function to get the average price
    :return: jsonified message
    """
    origin_code = ""
    destination_code = ""
    date_to = request.args.get('date_to')
    date_from = request.args.get('date_from')
    try:
        # converting string date to date object
        datetime.strptime(request.args.get('date_to'), "%Y-%m-%d").date()
        datetime.strptime(request.args.get('date_from'), "%Y-%m-%d").date()
    except ValueError:
        return jsonify("Incorrect date format entered either in date_to or date_from,"
                       "both fields should be YYYY-MM-DD format.")
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        # condition to check if both origin and destination contains value
        return jsonify("Enter the origin or destination fields either in CODE format 5 "
                       "characters in uppercase or slug name")
    elif not isinstance(origin, str) or not isinstance(destination, str):
        # condition to check if origin and destination are string or not
        return jsonify("Enter the origin or destination fields in string type")
    elif not origin.isalpha() or not destination.isalpha():
        # condition to check if origin and destination contains only alphabets
        return jsonify("Enter only alphabetic characters in origin and destination.")
    if origin.isupper() and len(origin) == 5:
        # checking if all characters are upper case and of length 5 i.e. its a code else slug
        origin_code = origin
    if destination.isupper() and len(destination) == 5:
        # checking if all characters are upper case and of length 5 i.e its a code else slug
        destination_code = destination
    conn_obj = create_connection()  # creating a database connection object
    if conn_obj is not None:
        connection = conn_obj
        cursor = connection.cursor()
    else:
        return jsonify("Error occurred while connecting to database. "
                       "Please check credentials or other details")
    try:
        if origin_code and destination_code:
            # condition to validate when all the data is appropriate
            obj = SqlQuery(origin, destination, date_from, date_to)
            output = obj.query_source_destination_format_ok()
            try:
                cursor.execute(output[0], output[1])
            except psycopg2.OperationalError as error:
                return jsonify(f"Error occurred while executing sql query {error}")
            json_obj = CreateJson(cursor)
            return json_obj.create_json()
        else:
            if not origin_code and destination_code:  # check if origin code is in form of slug name
                query_origin_slug = "select code from ports where parent_slug = %(origin)s"
                try:
                    cursor.execute(query_origin_slug, {'origin': origin})
                except psycopg2.OperationalError as error:
                    return jsonify(f"Error occurred while executing sql query {error}")
                if cursor.rowcount > 0:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_origin_or_destination_as_slug_in_port(True)
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                else:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_origin_or_destination_as_slug_not_in_port(True)
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                json_obj = CreateJson(cursor)
                return json_obj.create_json()
            if not destination_code and origin_code:
                # check if destination code is in from of slug name
                query_dest_slug = "select code from ports where parent_slug = %(origin)s"
                try:
                    cursor.execute(query_dest_slug, {'origin': destination})
                except psycopg2.OperationalError as error:
                    return jsonify(f"Error occurred while executing sql query {error}")
                if cursor.rowcount > 0:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_origin_or_destination_as_slug_in_port()
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                    json_obj = CreateJson(cursor)
                    return json_obj.create_json()
                else:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_origin_or_destination_as_slug_not_in_port()
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                    json_obj = CreateJson(cursor)
                    return json_obj.create_json()
            if not destination_code and not origin_code:
                # Both destination and origin code are in slug form
                flag = False
                flag1 = False
                query_origin_slug = "select code from ports where parent_slug = %(origin)s"
                try:
                    cursor.execute(query_origin_slug, {'origin': origin})
                except psycopg2.OperationalError as error:
                    return jsonify(f"Error occurred while executing sql query {error}")
                if cursor.rowcount > 0:
                    flag = True
                query_dest_slug = "select code from ports where parent_slug = %(destination)s"
                try:
                    cursor.execute(query_dest_slug, {'destination': destination})
                except psycopg2.OperationalError as error:
                    return jsonify(f"Error occurred while executing sql query {error}")
                if cursor.rowcount > 0:
                    flag1 = True
                if flag and flag1:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_not_origin_not_destination()
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                    json_obj = CreateJson(cursor)
                    return json_obj.create_json()
                if flag:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_not_origin_not_destination_origin_slug()
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                    json_obj = CreateJson(cursor)
                    return json_obj.create_json()
                if flag1:
                    obj = SqlQuery(origin, destination, date_from, date_to)
                    output = obj.query_not_origin_not_destination_slug()
                    try:
                        cursor.execute(output[0], output[1])
                    except psycopg2.OperationalError as error:
                        return jsonify(f"Error occurred while executing sql query {error}")
                    json_obj = CreateJson(cursor)
                    return json_obj.create_json()
    except Exception as error:
        return jsonify(f"Unknown error occurred during transaction {error}")
    finally:  # Block for closing connection and cursor
        cursor.close()
        connection.close()
