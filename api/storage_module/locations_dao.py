#!/usr/bin/python3
from storage_module.psqldb import PsqlDB
from storage_module.app_exceptions import DatabaseError, MissingParameterError
from datetime import datetime


# The Locations Data Access Object handles all interactions with the locations table.
class LocationsDao:

    #constructor
    def __init__(self):
        self.db = PsqlDB()

    def normalizeLocation(self, data):
        """
        Try normalize Location parameters to allow to Store data even Location entity was incomplete.
        
        """
        normalized=False
        if 'lat' not in data:
            data['lat']=0.0
            normalized=True
        if 'lng' not in data:
            data['lng']=0.0
            normalized=True
        if 'description' not in data:
            data['description']='no description'
            normalized=True
        if 'timeref' not in data:
            data['timeref']=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            normalized=True
        if 'userid' not in data:
            data['userid']=-1
            normalized=True
        data['normalized']=normalized
        return data

    def storeLocation(self, input_values):
        """
        Start insert process to store a location into locations table

        The format to parameter input_values is a dictionary like this:
        {
            'description':string,
            'lat':double,
            'lng':double,
            'timeref':date,
            'userid': number,
            'normalized': boolean
        }
        No return value but in error raise a DatabaseError exception.
        
        Warning: This method opens connection, run the process and close connection.
        """
        id = None
        try:
            self.db.connect()
            id = self.__insert(self.normalizeLocation(input_values))
            self.db.commit()

        except BaseException as error:
            raise error
        finally:
            self.db.close()

        return id
 
    def updateLocation(self, id, url_picture):

        try:
            self.db.connect()
            self.__update(id, url_picture)
            self.db.commit()

        except BaseException as error:
            raise error
        finally:
            self.db.close()

    def __insert(self, data):
        """
        Store input data into locations table...
        """
        values = "VALUES ('{0}', {1}, {2}, {4}, {5}, to_timestamp('{3}', 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"'), ST_SetSRID(ST_MakePoint({2}, {1}), 4326))".format(data['description'],data['lat'],
        data['lng'],data['timeref'],data['userid'],data['normalized'])

        sql = "INSERT INTO public.locations( "
        sql += "description, lat, lng, userid, normalized, datetime, points) "
        sql += values
        sql += " RETURNING id"

        self.__basicExecute(sql)

        id_of_new_row = self.db.cur.fetchone()[0]
        return id_of_new_row

    def __update(self, id, url_picture):
        """
        Store url into picture field
        """
        sql = "UPDATE public.locations "
        sql += "SET picture='{0}' ".format(url_picture)
        sql += "WHERE id={0}".format(id)

        self.__basicExecute(sql)

    def __basicExecute(self, sql):
        """
        Execute a basic SQL statement.
        """
        try:
            self.db.execQuery(sql)
        except Exception as error:
            self.db.rollback()
            raise DatabaseError('Database error:', error)