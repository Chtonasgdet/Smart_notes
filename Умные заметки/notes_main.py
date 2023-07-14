from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox
import json

app = QApplication([])
window = QWidget()

#Создание интерфейса приложения
window.setWindowTitle('Умные заметки')
window.resize(800, 700)

view_note = QTextEdit()
notes_list = QLabel('Список заметок')
make_note = QListWidget()
create_note_btn = QPushButton('Создать заметку')
del_note_btn = QPushButton('Удалить заметку')
save_note_btn = QPushButton('Сохранить заметку')
tegs_list = QLabel('Список тегов')
make_teg = QListWidget()
create_teg = QLineEdit()
create_teg.setPlaceholderText('Введите тег...')
add_teg_btn = QPushButton('Добавить к заметке')
detach_teg_btn = QPushButton('Открепить от заметки')
search_note_btn = QPushButton('Искать заметки по тегу')

v1_line = QVBoxLayout()
v2_line = QVBoxLayout()
main_hline = QHBoxLayout()
h1_line = QHBoxLayout()
h2_line = QHBoxLayout()
h3_line = QHBoxLayout()
h4_line = QHBoxLayout()

v1_line.addWidget(view_note)
v2_line.addWidget(notes_list, alignment = Qt.AlignLeft)
v2_line.addWidget(make_note)
h1_line.addWidget(create_note_btn, alignment = Qt.AlignCenter)
h1_line.addWidget(del_note_btn, alignment = Qt.AlignCenter)
v2_line.addLayout(h1_line)
h3_line.addWidget(save_note_btn, alignment = Qt.AlignCenter)
v2_line.addLayout(h3_line)
v2_line.addWidget(tegs_list, alignment = Qt.AlignLeft)
v2_line.addWidget(make_teg)
v2_line.addWidget(create_teg)
h2_line.addWidget(add_teg_btn, alignment = Qt.AlignCenter)
h2_line.addWidget(detach_teg_btn, alignment = Qt.AlignCenter)
v2_line.addLayout(h2_line)
h4_line.addWidget(search_note_btn, alignment = Qt.AlignCenter)
v2_line.addLayout(h4_line)
main_hline.addLayout(v1_line, stretch = 2)
main_hline.addLayout(v2_line, stretch = 1)
window.setLayout(main_hline)

#Создание json файла
notes = {
    'Добро пожаловать!': {
        'текст': 'В этом приложении можно создавать заметки с тегами...',
        'теги': ['умные заметки', 'инструкция']
    }
}

with open('notes_data.json', 'w', encoding = 'utf-8') as file:
    json.dump(notes, file, sort_keys = True)

with open('notes_data.json', 'r', encoding = 'utf-8') as file:
    notes = json.load(file)

#Отображение заметок на экране
make_note.addItems(notes)

def show_note():
    name = make_note.selectedItems()[0].text()
    print(name)
    view_note.setText(notes[name]['текст'])
    make_teg.clear()
    make_teg.addItems(notes[name]['теги']) 

make_note.itemClicked.connect(show_note)

#Функционал: заметки
def add_note():
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '' and note_name not in notes:
        notes[note_name] = {'текст': '', 'теги': []}
        make_note.addItem(note_name)
        make_teg.addItems(notes[note_name]['теги'])
    elif note_name in notes:
        error = QMessageBox()
        error.setWindowTitle('Ошибка!')
        error.setText('Заметка с подобным именем уже существует!')
        error.exec_()
create_note_btn.clicked.connect(add_note)

def del_note():
    if make_note.selectedItems():
        name = make_note.selectedItems()[0].text()
        del notes[name]
        make_note.clear()
        view_note.clear()
        make_teg.clear()
        make_note.addItems(notes)
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        error = QMessageBox()
        error.setWindowTitle('Ошибка!')
        error.setText('Пожалуйста выберите заметку,\nкоторую хотите удалить!')
        error.exec_()
del_note_btn.clicked.connect(del_note)

def save_note():
    if make_note.selectedItems():
        name = make_note.selectedItems()[0].text()
        notes[name]['текст'] = view_note.toPlainText()
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        error = QMessageBox()
        error.setWindowTitle('Ошибка!')
        error.setText('Пожалуйста выберите заметку,\nкоторую хотите сохранить!')
        error.exec_()
save_note_btn.clicked.connect(save_note)

#Функционал: теги
def add_teg():
    if make_note.selectedItems():
        name = make_note.selectedItems()[0].text()
        teg_name = create_teg.text()
        create_teg.clear()
        if teg_name != '' and teg_name not in notes[name]['теги']:
            notes[name]['теги'].append(teg_name)
            with open('notes_data.json', 'w', encoding = 'utf-8') as file:
                json.dump(notes, file, sort_keys = True)
            print(notes)
        elif teg_name in notes[name]['теги']:
            error = QMessageBox()
            error.setWindowTitle('Ошибка!')
            error.setText('Такой тег уже есть в заметке!')
            error.exec_()
    else:
        error = QMessageBox()
        error.setWindowTitle('Ошибка!')
        error.setText('Пожалуйста выберите заметку,\nв которую хотите добавить тег!')
        error.exec_()
add_teg_btn.clicked.connect(add_teg)

def del_teg():
    if make_note.selectedItems():
        name = make_note.selectedItems()[0].text()
        teg_name = create_teg.text()
        create_teg.clear()
        if teg_name in notes[name]['теги']:
            notes[name]['теги'].remove(teg_name)
            with open('notes_data.json', 'w', encoding = 'utf-8') as file:
                json.dump(notes, file, sort_keys = True)
            print(notes)
        elif teg_name not in notes[name]['теги']:
            error = QMessageBox()
            error.setWindowTitle('Ошибка!')
            error.setText('Такого тега нет в заметке!')
            error.exec_()
    else:
        error = QMessageBox()
        error.setWindowTitle('Ошибка!')
        error.setText('Пожалуйста выберите заметку,\nв которую хотите добавить тег!')
        error.exec_()
detach_teg_btn.clicked.connect(del_teg)

def search_teg():
    if search_note_btn.text() == 'Искать заметки по тегу':
        teg = create_teg.text()
        notes_filtered = {}
        for note in notes:
            if teg in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes_filtered, file, sort_keys = True)
        print(notes)
        make_note.clear()
        view_note.clear()
        make_teg.clear()
        make_note.addItems(notes_filtered)
        search_note_btn.setText('Сбросить результаты поиска')
    else:
        make_note.clear()
        view_note.clear()
        make_teg.clear()
        make_note.addItems(notes)
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
        search_note_btn.setText('Искать заметки по тегу')
search_note_btn.clicked.connect(search_teg)

window.show()
app.exec_()