#!/usr/bin/python3

"""
Goal: Demonstrate some minor database concepts
from popular databases like MySQL, PostgreSQL or Oracle.

Execution: Terminal based

Contributor:
David Anthony Parham
"""

import argparse
import datetime
import hashlib
import json
import os
import sys
import time

from password_strength import PasswordPolicy

# time and date variable
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

# password rules
POLICY = PasswordPolicy.from_names(
    length=6,  # min length: 6
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


class ToyDB(object):
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        """
        Summary:
            loads the given path if it exits. Otherwise empty JSON object is created

        Arguments:
            location {[type]} -- path variable

        Returns:
            True [boolean] -- always returns True
        """

        if os.path.exists(location):
            self._load()

        else:
            self.db = {}
        return True

    def _load(self):
        """ assign a empty database file (JSON) from the location stored in self.location to self.db """
        try:
            self.db = json.load(open(self.location, "r"))
        except Exception as e:
            print(e)

        return True

    def backup(self):
        """ saves the in-memory database from self.db in a database file """
        try:
            json.dump(self.db, open(self.location, "w+"))
            return True

        except BaseException:
            return False

    def login_credentials(self):
        """ create the login credentials and check for password strength """
        username = input("Enter a username and hit 'Enter': ")

        while True:
            password = input("Enter a password and hit 'Enter': ")
            password_similarity = input(
                "Confirm your passed password and hit 'Enter': "
            )
            if password == password_similarity:
                if len(POLICY.test(password)) == 0:
                    break

                else:
                    print(
                        """
                        Your password is not strong enough.
                        Please make sure to uphold the password policy:

                        1. At least 6 characters
                        2. 1 uppercase letter
                        3. 1. digit
                        4. 1. special character
                    """
                    )
            else:
                print("\nPasswords do not match. Please try again\n")

        return username.strip(), password.strip()

    def add_user(self, username, password):
        """ add database users to the credentials list """
        try:
            if self.db.get("credentials") is not None:
                self.db["credentials"].update({username: password})
                add_user_out = "\nSuccessfully added the user: {} to table: 'credential'".format(
                    username
                )

            else:
                self.db["credentials"] = {username: password}
                add_user_out = "\nSuccessfully initialized database and created table : 'credentials' with user {}".format(
                    username
                )

            self.backup()

        except Exception as e:
            add_user_out = "[X] Error Saving Values to Database : " + str(e)

        return add_user_out

    def create_table(self, table):
        """ create a table in the database """
        try:
            if table[0].lower() in "abcdefghijklmnopqrstuvwxyz1234567890":
                self.db[table] = {}
                self.backup()
                create_table_out = "Table: '{}' has been successfully created".format(
                    table
                )
            else:
                create_table_out = "No valid table name: Please use letters or digits"

        except IndexError:
            create_table_out = "Error: Forgot something?"

        return create_table_out

    def remove_table(self, table):
        """ remove a table in the database """
        try:
            del self.db[table]
            self.backup()
            remove_table_out = "Table: '{}' has been successfully removed".format(table)

        except KeyError:
            remove_table_out = "Table: '{}' is not part of this database".format(table)

        return remove_table_out

    def insert_entity(self, table, key, value):
        """ insert a entity (key, value) into a database table"""
        try:
            if table != "credentials":
                if table in self.db:
                    self.db[table].update({key: value})
                    insert_entity_out = "Successfully inserted {} in table: {}".format(
                        key, table
                    )
                else:
                    insert_entity_out = "Table: '{}' is not part of this database".format(
                        table
                    )
            else:
                insert_entity_out = "Error: No permissions through this method. Please use the add_user method trough CLI!"

            self.backup()

        except Exception as e:
            insert_entity_out = "[X] Error Saving Values to Database : " + str(e)

        return insert_entity_out

    def get_value(self, table, key):
        """ get a entity value from a given table """
        try:
            if self.db[table].get(key) is None:
                get_value_out = "No value can be found for " + key
            else:
                get_value_out = self.db[table].get(key)

        except KeyError:
            get_value_out = "Table: '{}' is not part of this database".format(table)

        return get_value_out

    def delete_entity(self, table, key):
        """ delete existing key from database """
        if table not in self.db:
            delete_entity_out = "Table: '{}' is not part of this database".format(table)

        else:
            if key not in self.db[table]:
                delete_entity_out = "Key: '{}' is not part of this table".format(key)

            else:
                del self.db[table][key]
                self.backup()
                delete_entity_out = "Key: '{}' has been successfully removed".format(
                    table
                )

        return delete_entity_out

    def reset_db(self):
        """ reset the database """
        self.db = {}
        self.backup()
        return "Successfully resetted the database"

    def encrypt_string(self, hash_string):
        """ return a encrypted string """
        sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def delete_database(self, database):
        """ delete the current database """
        try:
            os.remove(database)
            delete_database_out = "Successfully removed database: {}".format(database)

        except Exception as e:
            delete_database_out = "Error, no such file in directory"

        return delete_database_out


def mode_db(**kwargs):
    """ Handle the database functions"""

    for k, v in kwargs.items():
        try:
            if k == "mode":
                mode = int(v)
            elif k == "db_name":
                database = v
            elif k == "table":
                table = v.lower()
            elif k == "key":
                key = v.lower()
            elif k == "value":
                value = v
            elif k == "username":
                username = v
            elif k == "password":
                password = v
            elif k == "terminal":
                terminal = v
            else:
                raise print("Something went wrong")
        except:
            pass

    # add '.db' file extension, if it's not already included in the database name
    try:
        if database[-3:] != ".db":
            database += ".db"
        else:
            pass
    except:
        database += ".db"

    db = ToyDB(database)
    output = True

    if terminal:

        if mode == 1 or mode == 7:
            username, password = db.login_credentials()
            print(db.add_user(username.lower(), db.encrypt_string(password)))

        elif mode == 2:
            print(db.insert_entity(table, key, value))

        elif mode == 3:
            print(db.get_value(table, key))

        elif mode == 4:
            print(db.delete_entity(table, key))

        elif mode == 5:
            print(db.remove_table(table))

        elif mode == 6:
            print(db.create_table(table))

        elif mode == 8:
            del_query = input(
                "Do you really want to delete the database? 'y' else 'n':   "
            ).strip()

            if del_query.lower() == "y":
                print(db.delete_database(database))
                sys.exit("Close Database Application\n")

        elif mode == 9:
            del_query = input(
                "Do you really want to reset the database? 'y' else 'n':   "
            ).strip()

            if del_query.lower() == "y":
                print(db.reset_db())

        else:
            print(
                """
                Please insert a valid number 1-9
                For help make use of the -h flag
            """
            )
    else:
        if mode == 1 or mode == 7:
            db.add_user(username.lower(), db.encrypt_string(password))

        elif mode == 2:
            output = db.insert_entity(table, key, value)

        elif mode == 3:

            output = db.get_value(table, key)

        elif mode == 4:
            output = db.delete_entity(table, key)

        elif mode == 5:
            output = db.remove_table(table)

        elif mode == 6:
            output = db.create_table(table)

        elif mode == 8:
            output = db.delete_database(database)

        elif mode == 9:
            output = db.reset_db()

        else:
            print(
                """
                Please insert a valid number 1-9
                For help make use of the -h flag
            """
            )

    return output


if __name__ == "__main__":

    # argparse arguments
    parser = argparse.ArgumentParser(description="Demo database functionality")
    parser.add_argument(
        "-m",
        "--mode",
        type=int,
        required=True,
        help="""
                Help: Choose a db mode:

                (1) Create database
                (2) Insert entity in table     (3) Get instance from table
                (4) Delete instance from table (5) Delete table
                (6) Create table               (7) Add user
                (8) Delete database            (9) Reset database
            """,
    )
    parser.add_argument(
        "-db",
        "--database",
        type=str,
        required=True,
        help="db name with path, if db in remote folder",
    )
    parser.add_argument(
        "-t", "--table", type=str, required=False, default=None, help="db table name"
    )
    parser.add_argument(
        "-k", "--key", type=str, required=False, default=None, help="db instance key"
    )
    parser.add_argument(
        "-v", "--value", required=False, default=None, help="db instance value"
    )

    args = parser.parse_args()

    mode_db(
        mode=args.mode,
        db_name=args.database,
        table=args.table,
        key=args.key,
        value=args.value,
        terminal=True,
    )

    while True:

        continue_query = input("\nTo continue press 'y' else 'n':   ").strip()
        if continue_query.lower() == "y":
            print(
                """
                Help: Choose a db mode:

                (2) Insert entity in table     (3) Get instance from table
                (4) Delete instance from table (5) Delete table
                (6) Create table               (7) Add user
                (8) Delete database            (9) Reset database
            """
            )

            mode = input("Mode: ").strip()
            if mode == "2":
                table = input("Table: ").strip()
                key = input("Key:  ").strip()
                value = input("Value: ").strip()
                mode_db(
                    mode=mode,
                    db_name=args.database,
                    table=table,
                    key=key,
                    value=value,
                    terminal=True,
                )

            elif mode in "34":
                table = input("Table: ").strip()
                key = input("Key:  ").strip()
                mode_db(
                    mode=mode,
                    db_name=args.database,
                    table=table,
                    key=key,
                    terminal=True,
                )

            elif mode in "56":
                table = input("Table: ").strip()
                mode_db(mode=mode, db_name=args.database, table=table, terminal=True)

            elif mode == "7":
                mode_db(mode=mode, db_name=args.database, terminal=True)

            elif mode in "89":
                mode_db(mode=mode, db_name=args.database, terminal=True)
                if mode == "8":
                    break
                else:
                    pass

        elif continue_query.lower() == "n":
            break

        else:
            print("Wrong entry: To continue press y else n: ")
