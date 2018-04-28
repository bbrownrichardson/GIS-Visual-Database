# Brianna Brown Richardson
# Read Shapefile Module for VBASE project
# Last Modified Date: 28 April 2018
# CS200 - Algorithm Analysis

import shapefile
import os
from shutil import copy


class ReadShapeFile:
    def __init__(self, shapefile_dir, shp_dir, dbf_dir, title):
        self.shp_dir = shp_dir
        self.dbf_dir = dbf_dir
        self._title = title + chr(92)
        self._main_shp_dir = shapefile_dir

    def create_return_new_dir(self):
        """
        Upload selected shapefile files to main upload shapefile directory
        in a folder under the same title as profile
        :return: directory of main upload folder + title
        """
        new_dir = self._main_shp_dir + self._title
        os.makedirs(new_dir)
        with open(self.shp_dir, "rb"):
            copy(self.shp_dir, new_dir)
        with open(self.dbf_dir, "rb"):
            copy(self.dbf_dir, new_dir)

        return new_dir

    @staticmethod
    def read_files(shp_file, dbf_file):
        """
        Apply shapefile reader to main and dBASE files
        :param shp_file: main file selected
        :param dbf_file: dBASE file selected
        :return: reference to reader of selected files
        """
        myshp = open(shp_file, "rb")
        mydbf = open(dbf_file, "rb")
        sf = shapefile.Reader(shp=myshp, dbf=mydbf)
        return sf
