# coding:utf-8
from kivy.uix.floatlayout import FloatLayout
import kivy
from kivy.uix.widget import Widget

kivy.require('1.8.0')
from kivy.app import App


class Test(FloatLayout):
    pass


class TestApp(App):
    def build(self):
        root = Test()
        return root


if __name__ == '__main__':
    TestApp().run()