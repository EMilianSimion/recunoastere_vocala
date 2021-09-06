import json


class Color:
    def __init__(self):
        self.data = None
        self.init_data("../resources/color.json")

    def init_data(self, path):
        f = open(path, 'r')
        self.data = json.load(f)

    def add_color(self, button, background, navbar, centralwidget, intention):
        for b in button:
            b.setStyleSheet('QPushButton {{background-color: {}; color: {} }};'.format(self.data["secondary"],
                                                                                       self.data[
                                                                                           "on background color"]))
        for f in background:
            f.setStyleSheet('QGroupBox {{background-color: {}}};'.format(self.data["primary"]))
        navbar.setStyleSheet(
            'QMenuBar {{background-color: {}; color: {} }};'.format(self.data["navbar"], self.data["on primary color"]))
        centralwidget.setStyleSheet('QWidget {{color: {}}};'.format(self.data["primary"]))
        # intention.setStyleSheet('QPushButton {{background-color: {}; color: {} }};'.format(self.data["intention"],
        #                                                                                    self.data[
        #                                                                                        "on background color"]))
