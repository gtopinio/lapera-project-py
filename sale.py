import os
from globals import *

def sales_create_dict( sale_id,
                        sale_buyer_id,
                        sale_product_id,
                        sale_quantity,
                        sale_total_amount,
                        date
                    ):

    new_sale_dict = {}

    new_sale_dict["sale_id"] = sale_id
    new_sale_dict["sale_buyer_id"] = sale_buyer_id
    new_sale_dict["sale_product_id"] = sale_product_id
    new_sale_dict["sale_quantity"] = sale_quantity 
    new_sale_dict["sale_total_amount"] = sale_total_amount
    new_sale_dict["date"] = date

    return new_sale_dict

def sales_load_db():

    global sales

    sales_db_handle = open("data/sale.db","r")

    lines = sales_db_handle.readlines()
    
    sales.clear()

    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")

        sales.append(sales_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4],
                                            fields[5]
                                              ))
 
    sales_db_handle.close()

def sale_init():

    if not os.path.exists("data/sale.db"):
        sales_db_handle = open("data/sale.db","w")
        sales_db_handle.close()
    sales_load_db()

def sales_save_dict(sale_dict):
    sale_db_handle = open("data/sale.db","a+")
    
    output_line = str(sale_dict["sale_id"]+","+
                    sale_dict["sale_buyer_id"]+","+
                    sale_dict["sale_product_id"]+","+
                    sale_dict["sale_quantity"]+","+
                    sale_dict["sale_total_amount"]+","+ 
                    sale_dict["date"]+"\n")

    sale_db_handle.write(output_line)
    sale_db_handle.close()

def sales_writeup(track, cp, date):
    global carts
    new_sales_dict = {}

    for cart in carts:
        if track == cart['cart_id'] and cart['cart_checkedout'] == "0":
            cart['cart_checkedout'] = "1"

    for product in products:
        if product['product_id']== cp:
            price = int(product['product_unit_price'])

    for cart in carts:
        if track == cart['cart_id'] and cart['cart_checkedout'] == "1":
            quantity = int(cart['cart_quantity'])

            new_sales_dict['sale_id'] = str(len(sales))
            new_sales_dict['sale_buyer_id'] = str(cart['cart_buyer_id'])
            new_sales_dict['sale_product_id'] = str(cart['cart_product_id'])
            new_sales_dict['sale_quantity'] = str(cart['cart_quantity'])
            new_sales_dict['sale_total_amount'] = str(price*quantity)
            new_sales_dict['date'] = date
    sales_save_dict(new_sales_dict)
    sales_load_db()