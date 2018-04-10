# Brianna Brown Richardson
# Application Driver (Main) Module for VBASE project
# Last Modified Date:
# CS200 - Algorithm Analysis

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FallOutTransition
from kivy.lang import Builder
from app_screens import UploadScreen, IntroScreen, ObjectListScreen, \
    VisualScreen, DataEntryScreen


kv = Builder.load_file('my.kv')


class VBASEApp(App):

    def build(self):
        # self.manager = ScreenManager(transition=FallOutTransition())
        # self.manager.add_widget(MainScreen(name='MainScreen'))
        # self.manager.add_widget(ObjectListScreen(name='ObjectListScreen'))
        # self.manager.add_widget(UploadScreen(name='UploadScreen'))
        # self.manager.add_widget(DataEntryScreen(name='DataEntryScreen'))
        # self.manager.add_widget(VisualScreen(name='VisualScreen'))
        sm = ScreenManager(transition=FallOutTransition())

        sm.add_widget(IntroScreen())
        sm.add_widget(ObjectListScreen())
        sm.add_widget(UploadScreen())
        sm.add_widget(DataEntryScreen())
        sm.add_widget(VisualScreen())

        return sm


def main():
    pass


if __name__ == '__main__':
    VBASEApp().run()