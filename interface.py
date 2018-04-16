# Brianna Brown Richardson
# Interface Module for VBASE project
# Last Modified Date:
# CS200 - Algorithm Analysis

from read_shapefile import ReadShapeFile
from sql_functions import InsertDatabase, IndividualGetDatabase, GetAllDatabase
from upload_requirements import UploadRequirements
from visual_setup import VisualSetup
import os
import app_screens


class Interface:
    def __init__(self):
        self._db_file = 'db.sqlite'
        self.title = None
        if not os.path.exists(os.getcwd() + '\Uploaded_Shapefiles' + chr(92)):
            os.makedirs(os.getcwd() + '\Uploaded_Shapefiles' + chr(92))
        self._main_dir = os.getcwd() + '\Uploaded_Shapefiles' + chr(92)
        self.selected_files_dir = []
        self.selected_files = []

    def sql_to_object_screen(self):
        """
        Retrieve all profiles present in database
        :return: all SQL database data
        """

        method_1 = GetAllDatabase(self._db_file)
        all_obj_list = method_1.get_all()
        return all_obj_list

    def shape_file_two_dimension(self, title):
        """
        Initialize the process to visualize shapefile to 2D
        :param title: unique title of the profile being selected
        :return: None
        """

        obj = IndividualGetDatabase(title, self._db_file)
        obj.get_object()
        temp = obj.get_files()
        r_obj = ReadShapeFile(self._main_dir, temp['ShpName'],
                              temp['DbfName'], title)
        a = r_obj.read_files(temp['FileDirectory'] + temp['ShpName'],
                             temp['FileDirectory'] + temp['DbfName'])
        v_obj = VisualSetup(a)
        app_screens.VisualScreen.plt_var = None
        app_screens.VisualScreen.plt_var = v_obj.get_plt_2d()

    def shape_file_three_dimension(self, title):
        """
        Initialize the process to visualize shapefile to 3D
        :param title: unique title of the profile being selected
        :return: None
        """
        obj = IndividualGetDatabase(title, self._db_file)
        obj.get_object()
        temp = obj.get_files()
        r_obj = ReadShapeFile(self._main_dir, temp['ShpName'],
                              temp['DbfName'], title)
        a = r_obj.read_files(temp['FileDirectory'] + temp['ShpName'],
                             temp['FileDirectory'] + temp['DbfName'])
        v_obj = VisualSetup(a)
        v_obj.setting_shapes_to_3d()
        v_obj.setup_3d_scene()
        app_screens.VisualScreen.plt_var = v_obj.get_plt_3d()

    @staticmethod
    def file_path_name(file_path):
        """
        Shorten name of filepath to just the file + extension
        :param file_path: directory of file
        :return: shorten_file name
        """
        obj = UploadRequirements(None)
        shorten_file = obj.file_separation(file_path)
        return shorten_file

    @staticmethod
    def while_selecting_files(file_path):
        """
        Check if current file path is a file or directory. If file path is a
        file, return file
        :param file_path: string of current file path being assessed
        :return: File if not none
        """
        obj = UploadRequirements(file_path)
        selected_files = obj.file_or_directory()
        if selected_files is None:
            pass
        else:
            return selected_files

    @staticmethod
    def post_select_files(selected_files):
        """
        Determine if files fit criteria
        :param selected_files: list of files
        :return: Boolean value of True or False
        """
        obj = UploadRequirements(file_path=None)
        confirmation = obj.files_checker(selected_files)
        if confirmation is True:
            return True
        elif confirmation is False:
            return False

    def selected_db_names(self, selected_files):
        """

        :param selected_files:
        :return:
        """
        obj = UploadRequirements(file_path=None)

        for i in selected_files:
            self.selected_files_dir.append(i)
            self.selected_files.append(obj.file_separation(i))

    def insert_profile_database(self, info_dict):
        """
        Insert an entire profile into the database
        :param info_dict: dictionary containing all necessary
                information to inserted the database
        :return: None
        """
        obj = InsertDatabase(info_dict['Creator'], self._db_file)

        r_obj = ReadShapeFile(self._main_dir, self.selected_files_dir[0],
                              self.selected_files_dir[1], info_dict['Title'])
        new_dir = r_obj.create_return_new_dir()

        obj.insert_profile()
        obj.insert_object(info_dict['Title'])
        obj.insert_location(info_dict['Address'], info_dict['City'],
                            info_dict['State'], info_dict['Country'],
                            info_dict['Zipcode'])

        if self.selected_files[0]['extension'] == '.shp':
            obj.insert_file(self.selected_files[0]['filename'] +
                            self.selected_files[0]['extension'],
                            self.selected_files[1]['filename'] +
                            self.selected_files[1]['extension'],
                            new_dir)

        elif self.selected_files[1]['extension'] == '.shp':
            obj.insert_file(self.selected_files[1]['filename'] +
                            self.selected_files[1]['extension'],
                            self.selected_files[0]['filename'] +
                            self.selected_files[0]['extension'],
                            new_dir)
