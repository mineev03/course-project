from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import models
from gui.windows import main_window


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, database, config_py, utils, excel):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.database = database
        self.config_py = config_py
        self.utils = utils
        self.excel = excel

        self.add_table.clicked.connect(self.show_add_page)
        self.open_table.clicked.connect(self.show_table)
        self.change_table.clicked.connect(self.show_choice_page)

        self.back_button.clicked.connect(self.to_back_page)
        self.back_button_2.clicked.connect(self.to_back_page)
        self.back_button_3.clicked.connect(self.to_back_page)
        self.back_button_4.clicked.connect(self.to_back_page)
        self.back_button_5.clicked.connect(self.to_back_page)
        self.back_button_6.clicked.connect(self.to_back_page)
        self.back_button_7.clicked.connect(self.to_back_page)

        self.select_table.clear()
        self.select_table.addItems(self.database.get_tables_name())

        self.add_hall_button.clicked.connect(self.add_elements)
        self.add_movie_button.clicked.connect(self.add_elements)
        self.add_sale_button.clicked.connect(self.add_elements)

        self.delete_table.clicked.connect(self.fill_list)
        self.delete_button.clicked.connect(self.delete_by_id)

        self.open_change.clicked.connect(self.show_change_page)
        self.change_button.clicked.connect(self.change_elements)

        self.save_table.clicked.connect(self.show_output_page)
        self.output_button.clicked.connect(self.output_to_file)

    def to_back_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_output_page(self):
        self.stackedWidget.setCurrentIndex(7)

    def output_to_file(self):
        select_extension = self.select_extension.currentText()
        select_output_type = self.select_output_type.currentText()
        select_table = self.select_table.currentText()
        stmt = select(self.config_py.get_table_model(select_table))

        output_templates = {
            'JSON': {
                'Процент наполнения зала по сеансам': (self.database.get_hall_workload(),
                                                       self.config_py.get_field_by_output('hall_workload')),

                'Самый популярный жанр': (self.database.get_popular_genre(),
                                          self.config_py.get_field_by_output('popular_genre')),

                'Таблица': (self.database.select_query(stmt, 3), self.config_py.get_table_fields(select_table)),
            },
            'EXCEL': {
                'Процент наполнения зала по сеансам': (self.database.get_hall_workload(),
                                                       'Процент наполнения',
                                                       self.config_py.get_field_by_output('hall_workload')),

                'Самый популярный жанр': (self.database.get_popular_genre(),
                                          'Популярный жанр',
                                          self.config_py.get_field_by_output('popular_genre')),

                'Таблица': (self.database.select_query(stmt, 3),
                            f'Таблица {select_table}',
                            self.config_py.get_table_fields(select_table))
            }
        }

        if select_extension == 'EXCEL':
            self.output_to_excel(*output_templates[select_extension][select_output_type])
        elif select_extension == 'JSON':
            self.output_to_json(*output_templates[select_extension][select_output_type])

    def output_to_json(self, data_from_database, fields):
        data = []

        for row in data_from_database:
            data.append({key: value for key, value in zip(tuple(fields), row)})

        file_path = QFileDialog.getOpenFileName(self, 'Выбор JSON-файла', './', 'Image(*.json)')[0]

        if file_path:
            self.utils.save_to_json(file_path, data)
            self.stackedWidget.setCurrentIndex(0)

    def output_to_excel(self, data_from_database, header, fields):
        self.excel.create_workbook()
        file_path = QFileDialog.getOpenFileName(self, 'Выбор EXCEL-файла', './', 'Image(*.xlsx)')[0]

        if file_path:
            self.excel.sheet.title = header
            self.excel.sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(data_from_database[0]))

            self.excel.sheet['A1'] = header
            for cell in self.excel.sheet[1]:
                cell.border = self.excel.full_border
                cell.alignment = self.excel.alignment_center
                cell.font = self.excel.bold_font

            self.excel.sheet.append(fields)
            for cell in self.excel.sheet[2]:
                cell.border = self.excel.full_border
                cell.alignment = self.excel.alignment_center
                cell.font = self.excel.bold_font

            for index, value in enumerate(data_from_database, 3):
                self.excel.sheet.append(tuple(map(str, value)))

                for cell in self.excel.sheet[index]:
                    cell.border = self.excel.full_border
                    cell.alignment = self.excel.alignment_center

            try:
                self.excel.workbook.save(filename=file_path)
                self.stackedWidget.setCurrentIndex(0)
            except PermissionError:
                QMessageBox.warning(self, 'ОШИБКА', 'Закройте выбранный файл')

    def change_elements(self):
        table = self.config_py.get_table_field_models(self.select_table.currentText())
        type_change = table[self.type_change.currentText()]
        id_change = int(self.id_change.currentText())
        new_change = self.new_change.toPlainText()

        with Session(self.database.engine) as session:
            session.query(table['default']).filter(table['default'].id == id_change).update({type_change: new_change})
            session.commit()
        self.stackedWidget.setCurrentIndex(0)

        self.stackedWidget.setCurrentIndex(0)

    def show_change_page(self):
        self.id_select_change.clear()
        self.type_select_change.clear()
        self.new_change.clear()

        id_change = self.id_change.currentText()
        select_table = self.select_table.currentText()
        type_change = self.type_change.currentText()
        current_table = self.config_py.get_table_field_models(select_table)
        new_change_text = self.database.select_query(select(current_table[type_change]
                                                            ).where(current_table['default'].id == id_change), 2)

        self.new_change.setText(str(new_change_text))
        self.id_select_change.setText(f'ID: {id_change}')
        self.type_select_change.setText(f'Изменяемое поле: {type_change}')

        self.stackedWidget.setCurrentIndex(6)

    def show_choice_page(self):
        self.id_change.clear()
        self.type_change.clear()

        select_table = self.select_table.currentText()
        current_table = self.config_py.get_table_model(select_table)

        ids = [str(index) for index in self.database.select_query(select(current_table.id), 1)]
        types = [column.key for column in current_table.__table__.columns if column.key.find('id') == -1]

        self.id_change.addItems(ids)
        self.type_change.addItems(types)

        self.stackedWidget.setCurrentIndex(5)

    def delete_by_id(self):
        select_table = self.select_table.currentText()
        table = self.config_py.get_table_field_models(select_table)
        id_input_delete = self.id_input_delete.text()

        self.database.engine_connect(delete(table['default']).where(table['default'].id == id_input_delete))
        self.stackedWidget.setCurrentIndex(0)

    def fill_list(self):
        self.id_list_delete.clear()

        select_table = self.select_table.currentText()
        current_table = self.config_py.get_table_model(select_table)

        self.id_list_delete.addItems([str(index) for index in self.database.select_query(select(current_table.id), 1)])
        self.stackedWidget.setCurrentIndex(4)

    def show_table(self):
        if self.select_table.currentText() == 'halls':
            self.table.clear()

            id_hall = self.database.select_query(select(models.Hall.id), 1)
            capacity = self.database.select_query(select(models.Hall.capacity), 1)

            self.table.setColumnCount(2)
            self.table.setRowCount(len(id_hall))

            for index, value in enumerate(id_hall):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 0, item)

            for index, value in enumerate(capacity):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 1, item)

        elif self.select_table.currentText() == 'movies':
            self.table.clear()

            id_movie = self.database.select_query(select(models.Movie.id), 1)
            title = self.database.select_query(select(models.Movie.title), 1)
            genre = self.database.select_query(select(models.Movie.genre), 1)

            self.table.setColumnCount(3)
            self.table.setRowCount(len(id_movie))

            for index, value in enumerate(id_movie):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 0, item)

            for index, value in enumerate(title):
                item = QTableWidgetItem(value)
                self.table.setItem(index, 1, item)

            for index, value in enumerate(genre):
                item = QTableWidgetItem(value)
                self.table.setItem(index, 2, item)

        elif self.select_table.currentText() == 'sales':
            self.table.clear()

            id_sale = self.database.select_query(select(models.Sale.id), 1)
            id_movie = self.database.select_query(select(models.Sale.id_movie), 1)
            id_hall = self.database.select_query(select(models.Sale.id_hall), 1)
            time = self.database.select_query(select(models.Sale.time), 1)
            place_number = self.database.select_query(select(models.Sale.place_number), 1)

            self.table.setColumnCount(5)
            self.table.setRowCount(len(id_sale))

            for index, value in enumerate(id_sale):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 0, item)

            for index, value in enumerate(id_movie):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 1, item)

            for index, value in enumerate(id_hall):
                item = QTableWidgetItem(str(value))
                self.table.setItem(index, 2, item)

            for index, value in enumerate(time):
                item = QTableWidgetItem(value)
                self.table.setItem(index, 3, item)

            for index, value in enumerate(place_number):
                item = QTableWidgetItem(value)
                self.table.setItem(index, 4, item)

    def show_add_page(self):
        if self.select_table.currentText() == 'halls':
            self.id_hall.clear()
            self.capacity_hall.clear()

            self.id_hall.setText(self.database.get_last_index(models.Hall.id))

            self.stackedWidget.setCurrentIndex(1)

        elif self.select_table.currentText() == 'movies':
            self.id_movie.clear()
            self.title_movie.clear()
            self.genre_movie.clear()

            self.id_movie.setText(self.database.get_last_index(models.Movie.id))

            self.stackedWidget.setCurrentIndex(2)

        elif self.select_table.currentText() == 'sales':
            self.id_sale.clear()
            self.id_movie_sale.clear()
            self.id_hall_sale.clear()
            self.time_sale.clear()
            self.place_number_sale.clear()

            self.id_sale.setText(self.database.get_last_index(models.Sale.id))
            self.id_movie_sale.addItems(self.database.select_query(select(models.Movie.title), 1))
            self.id_hall_sale.addItems(self.database.select_query(select(models.Hall.capacity), 1))

            self.stackedWidget.setCurrentIndex(3)

    def add_elements(self):
        try:
            if self.select_table.currentText() == 'halls':
                id_halls = self.id_hall.text()

                capacity = self.capacity_hall.text()

                self.database.insert_query(models.Hall, id_halls, capacity)

                self.stackedWidget.setCurrentIndex(0)
                self.show_table()

            elif self.select_table.currentText() == 'movies':
                id_movie = self.id_movie.text()
                title = self.title_movie.text()
                genre = self.genre_movie.text()

                self.database.insert_query(models.Movie, id_movie, title, genre)
                self.stackedWidget.setCurrentIndex(0)
                self.show_table()

            elif self.select_table.currentText() == 'sales':
                id_sale = self.id_sale.text()
                id_movie = int(self.database.select_query(
                    select(models.Movie.id).where(
                        models.Movie.title == self.id_movie_sale.currentText()),
                    2))
                id_hall = int(self.database.select_query(
                    select(models.Hall.id).where(
                        models.Hall.capacity == self.id_hall_sale.currentText()),
                    2))
                time = self.time_sale.text()
                place_number = self.place_number_sale.text()

                self.database.insert_query(models.Sale, id_sale, id_movie, id_hall, time, place_number)
                self.stackedWidget.setCurrentIndex(0)
                self.show_table()
        except TypeError:
            QMessageBox.warning(self, 'ОШИБКА', 'Заполните все поля')
