# Brianna Brown Richardson
# Frontend (App Screens) Module for VBASE project
# Last Modified Date: 28 April 2018
# CS200 - Algorithm Analysis

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.bubble import BubbleButton
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, \
    NavigationToolbar2Kivy
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import threading
import interface


class IntroScreen(Screen):
    """
    First Screen User is introduced to. Constructed in .kv file
    """
    @staticmethod
    def update_obj_screen():
        obj = ObjectListScreen()
        obj.show_objects()


class ObjectListScreen(Screen):
    """
    Screen containing all profiles presented in database
    """
    title_returned = None
    interface_call = interface.Interface()
    v_coords = list()

    def __init__(self):
        super(ObjectListScreen, self).__init__()
        self.frame = GridLayout(cols=1)
        box_1 = BoxLayout(size_hint=(1, .10))

        btn_1 = Button(text='+')
        btn_1.bind(on_press=lambda x: self.delay_upload_screen())

        lbl_1 = Label(size_hint=(9, 1), text='OBJECTS')

        btn_2 = Button(id='refresh', text='REFRESH')
        btn_2.bind(on_press=lambda x: self.show_objects())

        box_1.add_widget(btn_1)
        box_1.add_widget(lbl_1)
        box_1.add_widget(btn_2)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.objects_holder = BoxLayout(orientation='vertical',
                                        id='objects_holder',
                                        size_hint=(1, self.scroll.size_hint_y*3
                                                   ))
        self.scroll.add_widget(self.objects_holder)

        self.frame.add_widget(box_1)
        self.frame.add_widget(self.scroll)
        self.add_widget(self.frame)
        self.show_objects()
        self.v_coords = list()

    def get_title(self, instance):
        """
        Function to get button's id via an instance which is the unique
        title of every profile
        :param instance: the occurrence of an object
        :return: None
        """
        self.title_returned = instance.id

    def return_title(self):
        """
        Purpose: To parse data from data using unique title as a identifier.

        Return the class variable, self.title_return which contains the data
        from get_title(). Created as work around to not being able to return
        a object's instance.
        :return: self.title_return
        """
        return self.title_returned

    def delay_upload_screen(self):
        """
        One time scheduled call to the function transition_upload()
        :return: None
        """
        Clock.schedule_once(lambda x: self.transition_upload(), .0000001)

    def transition_upload(self):
        """
        Transition to UploadScreen Screen
        :return: None
        """
        self.manager.current = 'UploadScreen'

    def visual_screen_instance_2d(self, instance):
        """
        Take the id of an instance and call the method to visual shapefiles
        in 2D while initiating thread loading popup and schedule a call for
        transition_visual function
        :param instance: button instance
        :return: None
        """
        ThreadPopup(self.interface_call.shape_file_two_dimension(
            instance.id))
        Clock.schedule_once(lambda x: self.transition_visual(), .000001)

    def visual_screen_instance_3d(self, instance):
        """
        Take the id of an instance and call the method to visual shapefiles
        in 3D while initiating thread loading popup and schedule a call for
        transition_visual function
        :param instance: button instance
        :return: None
        """
        ThreadPopup(self.interface_call.shape_file_three_dimension(
                instance.id))
        Clock.schedule_once(lambda x: self.transition_visual(), .000001)

    def transition_visual(self):
        """
        Initiate a transition to visual screen after setting the map widget
        on the visualscreen
        :return: None
        """
        v_obj = VisualScreen()
        Clock.schedule_once(lambda x: v_obj.set_map(), .00001)
        self.manager.current = 'VisualScreen'

    def show_objects(self):
        """
        Create the entire layout for all profiles present in the database
        :return: None
        """
        list_of_objects = self.interface_call.sql_to_object_screen()
        parent_widget = self.objects_holder

        parent_widget.clear_widgets()

        for item in list_of_objects:
            layout = GridLayout(cols=1, size_hint=(1,
                                                   parent_widget.size_hint_y
                                                   * 10), id=item['Title'])

            widg_1 = Label(text=item['Title'], size_hint=(1, .5))

            widg_2 = BoxLayout()
            widg_2_1 = Label(text='Creator: ' + item['Creator'])
            widg_2_2 = GridLayout(cols=1)
            shp_2_2 = Label(text='Shp Name: ' + item['ShpName'])
            dbf_2_2 = Label(text='Dbf Name: ' + item['DbfName'])
            widg_2_2.add_widget(shp_2_2)
            widg_2_2.add_widget(dbf_2_2)
            widg_2_3 = Label(text='Date: ' + item['Date'])

            widg_2.add_widget(widg_2_1)
            widg_2.add_widget(widg_2_2)
            widg_2.add_widget(widg_2_3)

            widg_3 = BoxLayout()

            widg_3_1 = BubbleButton(id=item['Title'], text='2D',
                                    color=[0, 0, 0, 1],
                                    size_hint=(1.0, .5),
                                    background_normal='',
                                    background_color=[1, 1, 1, 1])
            widg_3_1.bind(on_press=self.visual_screen_instance_2d)

            widg_3_2 = BubbleButton(id=item['Title'], text='3D',
                                    color=[0, 0, 0, 1],
                                    size_hint=(1.0, .5),
                                    background_normal='',
                                    background_color=[1, 1, 1, 1])
            widg_3_2.bind(on_press=self.visual_screen_instance_3d)

            widg_3_3 = BubbleButton(text='VR',
                                    color=[0, 0, 0, 1],
                                    size_hint=(1.0, .5),
                                    background_normal='',
                                    background_color=[1, 1, 1, 1])

            widg_3.add_widget(widg_3_1)
            widg_3.add_widget(widg_3_2)
            widg_3.add_widget(widg_3_3)

            layout.add_widget(widg_1)
            layout.add_widget(widg_2)
            layout.add_widget(widg_3)

            parent_widget.add_widget(layout)


class UploadScreen(Screen):
    """
    Screen containing an embedded file explorer where users are able to select
    shape files to upload
    """
    files = list()

    def __init__(self):
        super(UploadScreen, self).__init__()

    def selected(self, filename):
        """
        Add all selected files to temporary list to be later evaluated
        :param filename: selected file
        :return: None
        """
        interface_obj = interface.Interface()
        select = interface_obj.while_selecting_files(filename)
        if len(self.files) < 5:
            if select is None:
                pass
            elif select is not None:
                self.files.append(select)
        elif len(self.files) == 5 and select is not None:
            PopupMessage('You Only Need Two files\n'
                         'Remove Some to Proceed')

    def selected_files_popup(self):
        """
        Popup containing all files presented in a selected files list where
        user is able to add files or removes to given list prior to
        confirmation
        :return: None
        """
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Current Selected Files -- Click Button of '
                            'Files to Remove',
                      content=layout,
                      size_hint=(.75, .75))

        scroll_view = ScrollView(size_hint=(1, 10))
        file_layout = GridLayout(cols=1)
        scroll_view.add_widget(file_layout)

        for i in UploadScreen.files:
            obj = interface.Interface()
            cur_file = obj.file_path_name(i)
            if i is None:
                pass
            elif i is not None:
                a = Button(id=i, text=(cur_file['filename']+cur_file[
                    'extension']))
                a.bind(on_press=self.file_instance)
                file_layout.add_widget(a)

        button_layout = BoxLayout(orientation='horizontal')
        dismiss_button = Button(text='Add More Files')
        dismiss_button.bind(on_press=popup.dismiss)
        upload_button = Button(text='Upload')
        upload_button.bind(on_press=lambda x: self.confirm_files(
            UploadScreen.files, popup))

        button_layout.add_widget(dismiss_button)
        button_layout.add_widget(upload_button)

        layout.add_widget(scroll_view)
        layout.add_widget(button_layout)

        popup.open()

    @staticmethod
    def file_instance(instance):
        """
        On press function that removes file from selected files list
        and disables button that represents given file to indicate that file
        that been removed
        :param instance: instance of button being selected
        :return: None
        """
        UploadScreen.files.remove(instance.id)
        instance.disabled = True

    def confirm_files(self, files, popup_widget):
        """
        On confirmation of selected file, determine whether or not the given
        files fit the criteria to be uploaded and transition to Data Entry
        Screen if criteria is fulfilled
        :param files: final list of selected files to be upload
        :param popup_widget: parent widget object to be dismissed
        :return: list containing two dictionaries of filenames and
        extensions if criteria to be uploaded is fulfilled
        """
        obj = interface.Interface()
        if obj.post_select_files(files):
            self.manager.current = 'DataEntryScreen'
            popup_widget.dismiss()
            DataEntryScreen.files = self.files
        else:
            PopupMessage('Incorrect Files \nSelected!!')

    def return_to_obj_screen(self):
        """
        Reset class attributes
        :return: None
        """
        self.files = list()


class DataEntryScreen(Screen):
    files = None

    def __init__(self):
        super(DataEntryScreen, self).__init__()

    def submitting_data(self):
        """
        Function to handle data submissions
        :return: None
        """
        creator = self.ids.creator_id.text
        title = self.ids.title_id.text
        address = self.ids.address_id.text
        city = self.ids.city_id.text
        state = self.ids.state_id.text
        country = self.ids.country_id.text
        zipcode = self.ids.zipcode_id.text

        if creator == '' or title == '' or country == '':
            PopupMessage('Creator, Title, and Country \n'
                         'fields must have an entry')

        elif zipcode.strip() != '' and zipcode.strip().isdigit() is False:
            PopupMessage('Zipcode must be \nan integer value')

        elif zipcode.strip() == '':
            temp_dict = {
                'Creator': creator.strip().title(),
                'Title': title.strip().title(),
                'Address': address.strip().title(),
                'City': city.strip().title(),
                'State': state.strip().title(),
                'Country': country.strip().title(),
                'Zipcode': None
            }
            int_obj = interface.Interface()
            int_obj.selected_db_names(self.files)

            response = int_obj.check_existence_database(temp_dict['Title'])

            if response is False:
                PopupMessage('Lets be Unique. \nChoose a Different Title')

            elif response is True:
                int_obj.insert_profile_database(temp_dict)
                self.manager.current = 'ObjectListScreen'
                self.clear_entries()
                objscrn = ObjectListScreen()
                objscrn.show_objects()

        else:
            temp_dict = {
                'Creator': creator.strip().title(),
                'Title': title.strip().title(),
                'Address': address.strip().title(),
                'City': city.strip().title(),
                'State': state.strip().title(),
                'Country': country.strip().title(),
                'Zipcode': int(zipcode.strip())
            }
            int_obj = interface.Interface()
            int_obj.selected_db_names(self.files)

            response = int_obj.check_existence_database(temp_dict['Title'])

            if response is False:
                PopupMessage('Lets be Unique. \nChoose a Different Title')

            elif response is True:
                int_obj.insert_profile_database(temp_dict)
                self.manager.current = 'ObjectListScreen'
                self.clear_entries()
                objscrn = ObjectListScreen()
                objscrn.show_objects()

    def clear_entries(self):
        """
        Clear data fields
        :return: None
        """
        UploadScreen.files = list()
        self.ids.creator_id.text = ''
        self.ids.title_id.text = ''
        self.ids.address_id.text = ''
        self.ids.city_id.text = ''
        self.ids.state_id.text = ''
        self.ids.country_id.text = ''
        self.ids.zipcode_id.text = ''


class VisualScreen(Screen):
    plt_var = plt.gcf()

    def __init__(self):
        super(VisualScreen, self).__init__()

    def set_map(self):
        """
        Assign appropriate figure map to screen
        :return: None
        """
        box = self.ids.visual_box
        temp = FigureCanvasKivyAgg(self.plt_var)
        box.add_widget(temp)
        navigation = NavigationToolbar2Kivy(temp)
        box.add_widget(navigation.actionbar)
        map_button = self.ids.map_button
        map_button.disabled = True

    def screen_delay(self):
        """
        One time call to transition_obj_screen function
        :return: None
        """
        Clock.schedule_once(lambda x: self.transition_obj_screen(), .0000001)

    def transition_obj_screen(self):
        """
        Transition to ObjectListScreen, clear map widgets, reset
        display map button
        :return: None
        """
        self.manager.current = 'ObjectListScreen'
        box = self.ids.visual_box
        box.clear_widgets()
        self.plt_var.clf()
        map_button = self.ids.map_button
        map_button.disabled = False


class PopupError:
    """
    Popup with error messages
    """
    def __init__(self, e_mssg):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=str(e_mssg))
        dismiss_button = Button(text='OK')
        content.add_widget(message_label)
        content.add_widget(dismiss_button)
        popup = Popup(title='Error', content=content,
                      size_hint=(0.3, 0.25))
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()


class PopupMessage:
    """
    Popup with message
    """
    def __init__(self, mssg):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=str(mssg))
        dismiss_button = Button(text='OK')
        content.add_widget(message_label)
        content.add_widget(dismiss_button)
        popup = Popup(title='UH OH', content=content,
                      size_hint=(0.3, 0.25))
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()


class ThreadPopup:
    def __init__(self, running_func):
        self.pop_up = Popup()
        self.process(running_func)

    def pop_initate(self):
        """
        Initiate popup inform users background tasks are occurring
        :return: None
        """
        content = BoxLayout(orientation='vertical')
        message_label = Label(text='Running some awesome \nbackground '
                                   'tasks...', halign="center",
                              valign="middle")
        content.add_widget(message_label)
        self.pop_up = Popup(title='', content=content,
                            size_hint=(0.3, 0.25), separator_height=0)
        self.pop_up.open()

    def process(self, running_func):
        """
        Process the thread of the function being ran and call popup_initate()
        while the thread is alive then close popup when thread dies
        :param running_func: current function being ran
        :return: None
        """
        mythread = threading.Thread(target=running_func)
        mythread.start()
        while mythread.isAlive():
            self.pop_initate()
        self.pop_up.dismiss()
