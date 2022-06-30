import sys

from PyQt5 import QtWidgets

from config.config import Config
from database.database import DataBase
from gui.connection.main_connection import MainWindow
from utils.excel import Excel
from utils.utils import Utils


def main():
    config_py = Config()
    utils = Utils()
    excel = Excel()

    database = DataBase("cinema")
    database.create_all_tables()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(database, config_py, utils, excel)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
