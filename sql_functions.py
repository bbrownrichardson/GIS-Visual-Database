# Brianna Brown Richardson
# SQL Functions Module for VBASE project
# Last Modified Date: 28 April 2018
# CS200 - Algorithm Analysis

import sqlite3
import datetime


class InsertDatabase:

    def __init__(self, creator, db_file):
        self.creator = creator
        self._db_file = db_file
        self._pid = None
        self._oid = None

    def insert_profile(self):
        """
        Insert data about creator and title into profile table
        :return: None
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""INSERT OR IGNORE INTO Profile(Creator)
                                        VALUES(?)""",
                    (self.creator,))
        conn.commit()

        cur.execute("""SELECT ProfileId FROM Profile
                                        WHERE Creator = ?""",
                    (self.creator,))

        self._pid = cur.fetchone()[0]
        conn.commit()

    def insert_object(self, title):
        """
        Insert data pertaining to shapefile object
        :param title: title of shapefile object
        :return: None
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""INSERT OR IGNORE INTO Object(Title, Date, ProfileId) 
        VALUES(?, ?, ?);""",
                    (title, datetime.datetime.now(), self._pid))
        conn.commit()

        cur.execute("""SELECT ObjectId FROM Object 
        WHERE Title = ? AND ProfileId = ?""",
                    (title, self._pid))

        self._oid = cur.fetchone()[0]
        conn.commit()

    def insert_location(self, address, city, state, country, zipcode):
        """
        Insert data pertaining to location of shape file into location table

        :param address: address of shape_file, can be null
        :param city: city of shape_file, can be null
        :param state: state of shape_file, can be null
        :param country: country of shape_file, CANNOT be null
        :param zipcode: zipcode of shape_file, can be null
        :return: None
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""INSERT OR IGNORE INTO Location(Address, City, 
                    State, Country, Zipcode, ObjectId) 
                    VALUES(?, ?, ?, ?, ?, ?)""",
                    (address, city, state, country, zipcode,
                     self._oid))
        conn.commit()

    def insert_file(self, shp_name, dbf_name, file_directory):
        """
        Insert data about files of given shape_file into file table
        :param shp_name: main file of shape_file
        :param dbf_name: DBASE file of shape_file
        :param file_directory: directory of shape_files
        :return: NONE
        """
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()

        cur.execute("""INSERT OR IGNORE INTO Files(ShpName, DbfName, 
                            FileDirectory, ObjectId) VALUES(?, ?, ?, ?)""",
                    (shp_name, dbf_name, file_directory, self._oid))
        conn.commit()


class IndividualGetDatabase:
    def __init__(self, title, db_file):
        self.title = title
        self._db_file = db_file
        self._pid = None
        self._oid = None

    def exist_or_not(self):
        """
        Check if entry is currently in database
        :return: True if in database and False if not in database
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""SELECT COUNT(TITLE) FROM Object
                    WHERE Title = ? """, (self.title,))

        info = cur.fetchone()

        if info[0] > 0:
            return True
        else:
            return False

    def get_object(self):
        """
        Get all data in for an object in the Object table
        :return: object_data - dictionary contain data for an object
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""SELECT ObjectId, Title, Date, ProfileId FROM Object 
                        WHERE Title = ?""",
                    (self.title, ))

        info = cur.fetchall()

        self._oid = info[0][0]
        self._pid = info[0][3]

        object_data = {
            'ObjectId': info[0][0],
            'Title': info[0][1],
            'Date': info[0][2],
            'ProfileId': info[0][3]
        }

        return object_data

    def get_profile(self):
        """
        Get all data in for a profile in the Profile table
        :return: creator - creator of the profile
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""SELECT Creator FROM Profile
        WHERE ProfileId = ?""", (self._pid, ))

        creator = cur.fetchall()
        return creator

    def get_location(self):
        """
        Get all data in of the shapefile's location in the Location table
        :return: location_data - dictionary contain location data
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""SELECT LocationId, Address, City, Country, State, 
        Zipcode, ObjectId FROM Location 
        WHERE ObjectId = ?""", (self._oid,))

        info = cur.fetchall()

        location_data = {
            'LocationId': info[0][0],
            'Address': info[0][1],
            'City': info[0][2],
            'State': info[0][3],
            'Country': info[0][4],
            'Zipcode': info[0][5],
            'ObjectId': info[0][6]
        }

        return location_data

    def get_files(self):
        """
        Get all data about the files for shapefile in the Files table
        :return: files_data - dictionary contain files data
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute("""SELECT FilesId, ShpName, DbfName, FileDirectory, 
        ObjectId FROM Files WHERE ObjectId = ?""", (self._oid,))

        info = cur.fetchall()

        files_data = {
            'FilesId': info[0][0],
            'ShpName': info[0][1],
            'DbfName': info[0][2],
            'FileDirectory': info[0][3],
            'ObjectId': info[0][4],
        }

        return files_data


class GetAllDatabase:
    def __init__(self, db_file):
        self._db_file = db_file

    def get_all(self):
        """
        Get all complete entries from all the tables
        :return: info - list of tuples with each entries data
        """
        conn = sqlite3.connect(self._db_file)

        cur = conn.cursor()

        cur.execute(""" SELECT Profile.ProfileId, Profile.Creator, 
        Object.ObjectId, Object.Title, Object.Date, Object.ProfileId, 
        Location.LocationId, Location.Address, Location.City, 
        Location.State, Location.Country, Location.Zipcode, 
        Location.ObjectId, Files.FilesId, Files.ShpName, Files.DbfName, 
        Files.FileDirectory, Files.ObjectId 
        FROM Profile, Object, Location, Files 
        WHERE Profile.ProfileId = Object.ProfileId 
        AND Object.ObjectId = Location.ObjectId
        AND Object.ObjectId = Files.ObjectId
        """)

        info = cur.fetchall()

        all_data_list = list()

        for i in info:
            all_data_list.append({
                'Profile': i[0],
                'Creator': i[1],
                'ObjectId': i[2],
                'Title': i[3],
                'Date': i[4],
                'ProfileId': i[5],
                'LocationId': i[6],
                'Address': i[7],
                'City': i[8],
                'State': i[9],
                'Country': i[10],
                'Zipcode': i[11],
                'LObjectId': i[12],
                'FilesId': i[13],
                'ShpName': i[14],
                'DbfName': i[15],
                'FileDirectory': i[16],
                'FObjectId': i[17]
            })

        return all_data_list
