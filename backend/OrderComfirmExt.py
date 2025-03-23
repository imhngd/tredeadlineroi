import traceback

from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from dal.OrderDAL import OrderDAL
from dal.ProductDAL import ProductDAL
from model.Order import Order
from ui.Order_Confirm import Ui_MainWindow


class OrderConfirmExt(Ui_MainWindow):
    def __init__(self):
        self.product_dal = ProductDAL()
        self.order_dal = OrderDAL()
        self.list_product = []
        self.list_product_confirm = []
        self.count_row = 0
        self.current_order_id = None
        self.change_successfully = False
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.display_confirmed_order()
        self.display_unconfirmed_order()
        self.setupSignalAndSlots()
    def setupSignalAndSlots(self):
        self.tabWidget.currentChanged.connect(self.on_change_tab_main)
        self.tabWidgetConfirm.currentChanged.connect(self.on_change_tab_confirm)
        self.but_them.clicked.connect(self.add_new_product)
        self.but_xoa.clicked.connect(self.clear_product)
        self.but_tinhtien.clicked.connect(self.total)
        self.but_taodon.clicked.connect(self.generate_order)
        self.but_lammoi.clicked.connect(self.reset_all)
        self.listWidgetConfirmedOrder.itemClicked.connect(self.on_item_clicked)
        self.listWidgetUncomfirmedOrder.itemClicked.connect(
            self.on_item_clicked_un
        )
        self.but_xacnhan.clicked.connect(self.change_status_order)
        self.but_lammoitrang.clicked.connect(self.reset_confirm_tab)
    def change_status_order(self):
        isChecked = True
        for product in self.list_product_confirm:
            need_product = self.product_dal.get_product_by_id(product["id"])
            if need_product.quantity < product["minimum_stock"]:
                isChecked = False
                break
        if isChecked == True:
            id = self.current_order_id
            self.order_dal.change_status(id)
            self.change_successfully = True
            msg = QMessageBox()
            msg.setText("Đổi trạng thái thành công")
            msg.setWindowTitle("Thông báo")
            msg.exec()
        else:
            msg = QMessageBox()
            self.change_successfully = False
            msg.setText("Đơn hàng không hợp lệ")
            msg.setWindowTitle("Thông báo")
            msg.exec()
    def reset_confirm_tab(self):
        self.tbl_confirm.setRowCount(0)
        self.list_product_confirm = []
        if self.change_successfully == True:
            self.listWidgetConfirmedOrder.addItem(self.current_order_id)
            current_item = self.listWidgetUncomfirmedOrder.currentItem()
            self.listWidgetUncomfirmedOrder.takeItem(self.listWidgetUncomfirmedOrder.row(current_item))
    def on_item_clicked_un(self, item):
        order_id = item.text()
        self.list_product_confirm = []
        self.current_order_id = order_id
        searched_order = self.order_dal.get_order_by_id(order_id)
        if searched_order == None:
            msg = QMessageBox()
            msg.setText("Không tìm thấy")
            msg.setWindowTitle("thông báo")
        else:
            self.tbl_confirm.setRowCount(0)
            list_product = searched_order.list_product
            for i in range(len(list_product)):
                self.tbl_confirm.insertRow(i)
                current_product = list_product[i]
                self.list_product_confirm.append(current_product[0])
                column_name = QTableWidgetItem(current_product[0]["name"])
                column_unit_price = QTableWidgetItem(str(current_product[0]["unit_price"]))
                column_quantity = QTableWidgetItem(str(current_product[1]))
                column_amount = QTableWidgetItem(str(current_product[0]["unit_price"] * current_product[1]))
                self.tbl_confirm.setItem(i, 0, column_name)
                self.tbl_confirm.setItem(i, 1, column_quantity)
                self.tbl_confirm.setItem(i, 2, column_unit_price)
                self.tbl_confirm.setItem(i, 3, column_amount)
    def on_item_clicked(self, item):
        order_id = item.text()
        self.list_product_confirm = []
        self.current_order_id = order_id
        searched_order = self.order_dal.get_order_by_id(order_id)
        if searched_order == None:
            msg = QMessageBox()
            msg.setText("Không tìm thấy")
            msg.setWindowTitle("thông báo")
        else:
            self.tbl_confirm.setRowCount(0)
            list_product = searched_order.list_product
            for i in range(len(list_product)):
                self.tbl_confirm.insertRow(i)
                current_product = list_product[i]
                self.list_product_confirm.append(current_product[0])
                column_name = QTableWidgetItem(current_product[0]["name"])
                column_unit_price = QTableWidgetItem(str(current_product[0]["unit_price"]))
                column_quantity = QTableWidgetItem(str(current_product[1]))
                column_amount = QTableWidgetItem(str(current_product[0]["unit_price"]*current_product[1]))
                self.tbl_confirm.setItem(i, 0, column_name)
                self.tbl_confirm.setItem(i, 1, column_quantity)
                self.tbl_confirm.setItem(i, 2, column_unit_price)
                self.tbl_confirm.setItem(i, 3, column_amount)
    def reset_all(self):
        self.clear_product()
        self.list_product = []
        self.count_row = 0
        self.tbl_donhang.setRowCount(self.count_row)
        self.txt_tenkh.setText("")
        self.txt_sdt.setText("")
        self.txt_phaithu.setText("")
    def generate_order(self):
        order_id = f"order{len(self.order_dal.get_list_order()) + 1}"
        date_order = self.dateEdit.date().toString("dd/MM/yyyy")
        list_product = []
        for product in self.list_product:
            list_product.append([product[0].__dict__, product[1]])
        status = "Chưa xác nhận"
        customer_name = self.txt_tenkh.text()
        contact_no = self.txt_sdt.text()
        total = int(self.txt_phaithu.text())
        if customer_name == "" and contact_no == "":
            msg = QMessageBox()
            msg.setText("Điền thiếu thông tin!")
            msg.setWindowTitle("Thông báo")
            msg.exec()
            return
        new_order = Order(order_id, date_order, list_product, status, customer_name, contact_no, total)
        self.order_dal.store_order(new_order)
        msg = QMessageBox()
        msg.setText("Đã tạo đơn hàng")
        msg.setWindowTitle("Thông báo")
        msg.exec()
    def total(self):
        total = 0
        for i in range(len(self.list_product)):
            total += self.list_product[i][0].unit_price * self.list_product[i][1]
        self.txt_phaithu.setText(str(total))
    def clear_product(self):
        self.txt_PName.setText("")
        self.txt_PQuantity.setText("")
    def add_new_product(self):
        product_name = self.txt_PName.text()
        quantity = int(self.txt_PQuantity.text())
        needed_product = self.product_dal.get_product_by_name(product_name)
        if needed_product == None:
            msg = QMessageBox()
            msg.setText("Không tìm thấy sản phẩm!!!")
            msg.setWindowTitle("Thông báo")
            msg.exec()
        else:
            self.product_dal.update_quantity_product(needed_product.id, quantity)
            self.list_product.append([needed_product, quantity])
            self.tbl_donhang.setRowCount(self.count_row)
            self.tbl_donhang.insertRow(self.count_row)
            column_name = QTableWidgetItem(needed_product.name)
            column_quantity = QTableWidgetItem(str(quantity))
            column_unit_price = QTableWidgetItem(str(needed_product.unit_price))
            column_total = QTableWidgetItem(str(quantity*needed_product.unit_price))
            self.tbl_donhang.setItem(self.count_row, 0, column_name)
            self.tbl_donhang.setItem(self.count_row, 1, column_quantity)
            self.tbl_donhang.setItem(self.count_row, 2, column_unit_price)
            self.tbl_donhang.setItem(self.count_row, 3, column_total)
            self.count_row += 1
    def on_change_tab_confirm(self, index):
        self.tabWidgetConfirm.setCurrentIndex(index)
    def on_change_tab_main(self, index):
        self.tabWidget.setCurrentIndex(index)
    def display_confirmed_order(self):
        list_confirmed_order = self.order_dal.get_confirmed_order()
        list_confirmed_order = [order.order_id for order in list_confirmed_order]
        print(list_confirmed_order)
        self.listWidgetConfirmedOrder.addItems(list_confirmed_order)
    def display_unconfirmed_order(self):
        try:
            list_unconfirmed_order = self.order_dal.get_unconfirmed_order()
            list_unconfirmed_order = [order.order_id for order in list_unconfirmed_order]
            list_unconfirmed_order = list_unconfirmed_order[:int(len(list_unconfirmed_order)/2)]
            print(list_unconfirmed_order)
            self.listWidgetUncomfirmedOrder.addItems(list_unconfirmed_order)
        except:
            traceback.print_exc()
    def show(self):
        self.MainWindow.show()