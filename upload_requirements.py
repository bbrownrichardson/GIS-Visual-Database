# Brianna Brown Richardson
# Upload Requirements Module for VBASE project
# Last Modified Date: 28 April 2018
# CS200 - Algorithm Analysis

import os


class UploadRequirements:
    def __init__(self, file_path):
        """
        Constructor
        :param file_path: path to check for file or directory function
        """
        self._file_path = file_path

    def file_or_directory(self):
        """
        Determine whether a file path from Upload object is a file or directory
        :return: file paths with a file and not directory
        """
        if len(self._file_path) is not 0:
            if os.path.isfile(self._file_path[0]) is True \
                    and self._file_path[0] is not None:
                return self._file_path[0]
        else:
            pass

    @staticmethod
    def file_separation(file_path):
        """
        Separate file name and extension from file path
        :param file_path:
        :return: dictionary contain filename and extension of given file path
        """
        filename_w_ext = os.path.basename(file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        file_combo = {
            'filename': filename,
            'extension': file_extension
        }
        return file_combo

    def files_checker(self, files_list):
        """
        Determine if desired files fulfill file requirement of being two files
        (.shp and .dbf) with same prefix
        :param files_list: list of files to check
        :return: boolean to determine if fulfilled or not
        """

        if len(files_list) is 2:
            first_file = self.file_separation(files_list[0])
            second_file = self.file_separation(files_list[1])
            if first_file['filename'] == second_file['filename']:
                if first_file['extension'] == '.shp' and \
                        second_file['extension'] == '.dbf':
                    return True
                elif first_file['extension'] == '.dbf' and \
                        second_file['extension'] == '.shp':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
