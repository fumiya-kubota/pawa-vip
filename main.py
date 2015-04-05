from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pawavip.adventure_screen import AdventureScreen


class PawaVipApp(App):
    def build(self):
        root = ScreenManager()
        return root

    def on_start(self):
        self.root.add_widget(AdventureScreen(name='adventure'))


if __name__ == '__main__':
    PawaVipApp().run()