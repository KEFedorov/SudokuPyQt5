import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QFileDialog, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from Field import *
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QStyle, QMessageBox


DISABLED_CELL = 'border: 2px solid #00103D; background: "#EDC997"; color: "#00103D";'
ENABLED_CELL = 'border: 2px solid #00103D; background: "#B7D7F6"; color: "#00103D";'
SELECTED_CELL = 'border: 2px solid #00103D; background: "#C383C2"; color: "#00103D";'
HARD_LEVELS = ("1 - Знакомлюсь с правилами", "2 - Начинающий",
               "3 - Ученик", "4 - Любитель",
               "5 - Специалист", "6 - Профессионал",
               "7 - Одаренный", "8 - Талант",
               "9 - Гений", "10 - Искусственный интеллект")


class Button(QPushButton):
    def __init__(self, parent=None, row=None, col=None, basic_style=None, selected_style=None):
        super(Button, self).__init__(parent)
        self.blocked = False
        self.basic_style = basic_style
        self.selected_style = selected_style
        self.row = row
        self.col = col
        if basic_style is not None:
            self.setStyleSheet(self.basic_style)

    def enterEvent(self, q_event):
        if self.blocked:
            return
        if not self.isEnabled():
            return
        if self.selected_style is not None:
            self.setStyleSheet(self.selected_style)

    def leaveEvent(self, q_event):
        if self.blocked:
            return
        if not self.isEnabled():
            return
        if self.basic_style is not None:
            self.setStyleSheet(self.basic_style)


class ChoiceNumberWindow(QDialog):
    def __init__(self):
        super(ChoiceNumberWindow, self).__init__()
        self.result = None
        self.setFixedSize(220, 280)
        self.setWindowTitle("Выбор цифры")
        self.main_layout = QVBoxLayout(self)
        number = 0
        for i in range(3):
            line_layout = QHBoxLayout(self)
            for j in range(3):
                button = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
                number += 1
                button.setFont(QFont("Times", 20, QFont.Bold))
                button.clicked.connect(self.choice)
                button.setFixedSize(60, 60)
                button.setText(str(number))
                line_layout.addWidget(button)
            self.main_layout.addLayout(line_layout)
        clear_button = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
        clear_button.setFont(QFont("Times", 12, QFont.Bold))
        clear_button.setFixedSize(195, 60)
        clear_button.setText("Очистить поле")
        clear_button.clicked.connect(self.choice)
        line_layout = QHBoxLayout(self)
        line_layout.addWidget(clear_button)
        self.main_layout.addLayout(line_layout)
        self.exec()

    def choice(self):
        sender = self.sender()
        if sender.text().isdigit():
            self.result = sender.text()
        else:
            self.result = 0
        self.close()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Судоку')
        self.main_layout = QVBoxLayout(self)

        text_font = QFont("Times", 12, QFont.Bold)
        numbers_font = QFont("Times", 20, QFont.Bold)

        button_new_game = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
        button_new_game.setText("Новая игра")
        button_new_game.setFont(text_font)
        button_new_game.setFixedHeight(60)
        button_new_game.clicked.connect(self.create_new_game)

        button_open_game = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
        button_open_game.setText("Открыть игру")
        button_open_game.setFont(text_font)
        button_open_game.setFixedHeight(60)
        button_open_game.clicked.connect(self.open_game_from_file)

        button_save_game = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
        button_save_game.setText("Сохранить игру")
        button_save_game.setFont(text_font)
        button_save_game.setFixedHeight(60)
        button_save_game.clicked.connect(self.save_game_to_file)

        first_line = QHBoxLayout(self)
        first_line.addWidget(button_new_game)
        first_line.addWidget(button_open_game)
        first_line.addWidget(button_save_game)
        self.main_layout.addLayout(first_line)

        self.FG = Field()
        self.field_buttons = []
        for i in range(9):
            line_layout = QHBoxLayout(self)
            line_buttons = []
            for j in range(9):
                button = Button(self, row=i, col=j, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
                button.setFont(numbers_font)
                button.setFixedSize(60, 60)
                button.clicked.connect(self.choice_number)
                line_buttons.append(button)
                line_layout.addWidget(button)
            self.field_buttons.append(line_buttons)
            self.main_layout.addLayout(line_layout)
        self.clear_field()
        self.setFixedSize(621, 691)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor("#00103D"))
        qp.drawRect(209, 80, 2, 595)
        qp.drawRect(410, 80, 2, 595)
        qp.drawRect(13, 276, 595, 2)
        qp.drawRect(13, 477, 595, 2)
        qp.end()

    def clear_field(self):
        for i in range(9):
            for j in range(9):
                self.field_buttons[i][j].setText("")
                self.field_buttons[i][j].setEnabled(False)
                self.field_buttons[i][j].setStyleSheet(DISABLED_CELL)
        self.repaint()

    def create_new_game(self):
        hard_level, ok_pressed = QInputDialog.getItem(
            self, "Выбор уровня сложности", "Выберите уровень сложности", HARD_LEVELS, 4, False)
        if not ok_pressed:
            return
        self.setWindowTitle('Судоку')
        self.clear_field()
        self.FG = FieldsGenerator(int(hard_level.split(" - ")[0]))
        self.download_game_to_window()

    def save_game_to_file(self):
        if self.FG.hard_level is None:
            message = "Поле игры пустое!\nНет смысла его сохранять!"
            InformationWindow("Ошибка сохранения", message)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Выбор файла для сохранения игры', '', 'Text files (*.txt)')[0]
            if file_name != "":
                self.FG.save_game(file_name)
                message = "Игра успешно сохранена!"
                InformationWindow("Успешное сохранение", message)

    def open_game_from_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выбор файла с игрой', '', 'Text files (*.txt)')[0]
        if file_name != "":
            self.FG = Field()
            if not self.FG.open_game(file_name):
                self.FG = Field()
                self.clear_field()
                message = "Загрузка игры невозможна!\nФайл повреждён!"
                InformationWindow("Ошибка загрузки", message)
            else:
                self.download_game_to_window()
                message = "Игра успешно загружена из файла!"
                InformationWindow("Успешная загрузка", message)

    def download_game_to_window(self):
        for i in range(9):
            for j in range(9):
                if self.FG.start_field[i][j] is not None:
                    self.field_buttons[i][j].setText(str(self.FG.start_field[i][j]))
                    self.field_buttons[i][j].setEnabled(False)
                    self.field_buttons[i][j].setStyleSheet(DISABLED_CELL)
                else:
                    if self.FG.field[i][j] is not None:
                        self.field_buttons[i][j].setText(str(self.FG.field[i][j]))
                    else:
                        self.field_buttons[i][j].setText("")
                    self.field_buttons[i][j].setEnabled(True)
                    self.field_buttons[i][j].setStyleSheet(ENABLED_CELL)
        self.setWindowTitle('Судоку - Уровень #' + HARD_LEVELS[self.FG.hard_level - 1])

    def choice_number(self):
        self.sender().blocked = True
        self.sender().setStyleSheet(self.sender().selected_style)
        cnw = ChoiceNumberWindow()
        row = self.sender().row
        col = self.sender().col
        res = cnw.result
        if res is not None:
            if res == 0:
                self.FG.field[row][col] = None
                self.field_buttons[row][col].setText("")
            else:
                self.FG.field[row][col] = int(res)
                self.field_buttons[row][col].setText(str(res))
        self.sender().setStyleSheet(self.sender().basic_style)
        self.sender().blocked = False
        if self.FG.is_game_over():
            lvl = self.FG.hard_level
            message = "Вы успешно решили судоку!\nВами был покорен уровень " + str(lvl) + "!\n"
            message += "Ваш титул: " + HARD_LEVELS[lvl - 1][len(str(lvl)) + 3:] + "!"
            InformationWindow("Победа", message)


class InformationWindow(QDialog):
    def __init__(self, title, text):
        super(InformationWindow, self).__init__()
        self.setFixedSize(450, 200)
        self.setWindowTitle(title)
        # self.setStyleSheet("background-color: #EDC997")
        main_layout = QVBoxLayout(self)
        text_label = QLabel()
        text_label.setStyleSheet("color: #00103D")
        text_label.setText(text)
        text_label.setFont(QFont("Times", 12, QFont.Bold))
        text_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        ok_button = Button(self, basic_style=ENABLED_CELL, selected_style=SELECTED_CELL)
        ok_button.setFont(QFont("Times", 12, QFont.Bold))
        ok_button.setFixedSize(150, 50)
        ok_button.setText("ОК")
        ok_button.clicked.connect(self.close)
        button_layout = QHBoxLayout(self)
        button_layout.addWidget(ok_button)
        button_layout.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(text_label)
        main_layout.addLayout(button_layout)
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())
