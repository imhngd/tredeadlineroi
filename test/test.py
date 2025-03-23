from dal.OrderDAL import OrderDAL

order_dal = OrderDAL()
lo = order_dal.get_unconfirmed_order()
print(len(lo))