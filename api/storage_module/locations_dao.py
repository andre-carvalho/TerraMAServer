#!/usr/bin/python3
from storage_module.psqldb import PsqlDB
from storage_module.app_exceptions import DatabaseError, MissingParameterError


# The Locations Data Access Object handles all interactions with the locations table.
class LocationsDao:

    #constructor
    def __init__(self):
        self.db = PsqlDB()

    """
        Start insert process to store a location into locations table

        The format to parameter input_values is a dictionary like this: {'scene_id':value,path':value,'row':value,'date':value}
        
        No return value but in error raise a DatabaseError exception.
        
        Warning: This method opens connection, run the process and close connection.
    """
    def storeLocation(self, input_values):
        id = None
        try:
            self.db.connect()
            id = self.__insert(input_values)
            self.db.commit()

        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return id
 
    """
        Store input data into locations table...
    """
    def __insert(self, data):

        values = "VALUES ('{0}', {1}, {2}, '{3}', '{4}')".format(data['description'],data['lat'],data['lng'],data['datetime'],data['photo'])

        sql = "INSERT INTO public.locations( "
        sql += "description, lat, lng, datetime, photo) "
        sql += values
        sql += " RETURNING id"

        self.__basicExecute(sql)

        id_of_new_row = self.db.cur.fetchone()[0]
        return id_of_new_row
    

 
    """
        Execute a basic SQL statement.
    """
    def __basicExecute(self, sql):
        try:
            self.db.execQuery(sql)
        except Exception as error:
            self.db.rollback()
            raise DatabaseError('Database error:', error)