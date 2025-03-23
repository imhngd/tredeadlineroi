from PyQt6.QtWidgets import QApplication, QMainWindow

from backend.OrderComfirmExt import OrderConfirmExt

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = QMainWindow()
    mp = OrderConfirmExt()
    mp.setupUi(MainWindow)
    mp.show()
    app.exec()




