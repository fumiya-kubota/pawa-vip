import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen.adventure_screen import AdventureScreen


class PawaVipApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(AdventureScreen(name='adventure'))
        return root

if __name__ == '__main__':
    PawaVipApp().run()