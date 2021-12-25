import os, datetime
from sale import sales_writeup
from globals import *

def cart_create_dict(   cart_id,
                        cart_buyer_id,
                        cart_product_id,
                        cart_quantity,
                        cart_checkedout,
                        cart_date
                    ):
    
    new_cart_dict = {}
    new_cart_dict["cart_id"] = cart_id
    new_cart_dict["cart_buyer_id"] = cart_buyer_id
    new_cart_dict["cart_product_id"] = cart_product_id
    new_cart_dict["cart_quantity"] = cart_quantity 
    new_cart_dict["cart_checkedout"] = cart_checkedout
    new_cart_dict["cart_date"] = cart_date

    return new_cart_dict

def cart_save_dict(cart_dict):
    cart_db_handle = open("data/cart.db","a+")
    
    output_line = str(cart_dict["cart_id"]+","+
                    cart_dict["cart_buyer_id"]+","+
                    cart_dict["cart_product_id"]+","+ 
                    cart_dict["cart_quantity"]+","+ 
                    cart_dict["cart_checkedout"]+","+
                    cart_dict["cart_date"]+"\n") 

    cart_db_handle.write(output_line)
    cart_db_handle.close()

def cart_load_db():
    global carts
    cart_db_handle = open("data/cart.db","r")
    lines = cart_db_handle.readlines()
    carts.clear()
    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")
 
        carts.append(cart_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4],
                                            fields[5]
                                              ))
    cart_db_handle.close()

def cart_init():
    if not os.path.exists("data/cart.db"):
        cart_db_handle = open("data/cart.db","w")
        cart_db_handle.close()
    cart_load_db()

def cart_view_checkout():

    global carts

    loop = True
    cart_check = False
    while loop:
        response = str(input("Ender [item ID] of item: "))
        for cart in carts:
            if response == cart['cart_id'] and cart['cart_checkedout'] == '0':
                cart_check = True
                
                track = cart['cart_id']
                cp = cart['cart_product_id']
        if cart_check == False:
            print("Invalid [item ID]. Please try again.")
                
        else:
            loop = False
            date = str(datetime.datetime.now())
            input("The item will be delivered within 5 days. Please [ENTER]..")
            sales_writeup(track, cp, date)
    cart_check_db()
    cart_update_db()

def cart_update_dict(   cart_id,
                        cart_buyer_id,
                        cart_product_id,
                        cart_quantity,
                        cart_checkedout,
                        cart_date
                    ):
    global sales

    new_cart_dict = {}
    new_cart_dict["cart_id"] = cart_id
    new_cart_dict["cart_buyer_id"] = cart_buyer_id
    new_cart_dict["cart_product_id"] = cart_product_id
    new_cart_dict["cart_quantity"] = cart_quantity
    for sale in sales:
        if sale['sale_product_id'] == cart_product_id:
            new_cart_dict["cart_checkedout"] = "1"
        else:
            new_cart_dict["cart_checkedout"] = cart_checkedout	
    new_cart_dict["cart_date"] = cart_date

    return new_cart_dict

def cart_check_db():
    global carts
    cart_db_handle = open("data/cart.db","r")
    lines = cart_db_handle.readlines()
    carts.clear()
    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")

        carts.append(cart_update_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4],
                                            fields[5]
                                              ))

    cart_db_handle.close()

def cart_update_db():
    global carts
    f = open("data/cart.db", "w+")
    f.close()
    for i in carts:
        cart_save_dict(i)
    cart_load_db()