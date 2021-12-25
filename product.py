import os
import random
from globals import *
def product_create_dict( product_id,
                        product_seller_id,
                        product_category,
                        product_name,
                        product_description,
                        product_quantity,
                        product_unit_price
                    ):

    new_product_dict = {}

    new_product_dict["product_id"] = product_id
    new_product_dict["product_seller_id"] = product_seller_id
    new_product_dict["product_category"] = product_category
    new_product_dict["product_name"] = product_name
    new_product_dict["product_description"] = product_description 
    new_product_dict["product_quantity"] = product_quantity
    new_product_dict["product_unit_price"] = product_unit_price
    
    return new_product_dict

def product_load_db():

    global products

    product_db_handle = open("data/product.db","r")

    lines = product_db_handle.readlines()

    products.clear()

    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")
        
        products.append(product_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4],
                                            fields[5],
                                            fields[6]
                                              ))

    product_db_handle.close()

def product_init():

    if not os.path.exists("data/product.db"):
        product_db_handle = open("data/product.db","w")
        product_db_handle.close()
    product_load_db()

def product_save_dict(product_dict):

    product_db_handle = open("data/product.db","a+")

    output_line = str(product_dict["product_id"]+","+
                    product_dict["product_seller_id"]+","+
                    product_dict["product_category"]+","+ 
                    product_dict["product_name"]+","+ 
                    product_dict["product_description"]+","+ 
                    product_dict["product_quantity"]+","+ 
                    product_dict["product_unit_price"]+"\n")

    product_db_handle.write(output_line)
    product_db_handle.close()

def product_view_search():

    global products
    matches = []
    keyword = str(input("Keyword: "))
    
    for product in products:
       if keyword.lower() in str(product['product_name']).lower() or keyword.lower() in str(product['product_category']).lower() or keyword.lower() in str(product['product_description']).lower():
           matches.append(product)
           
    print(len(matches),"match(es) found:")
    for i in matches:
        sub =[]
        sub.append(i['product_id'])
        sub.append(i['product_name'])
        sub.append(i['product_description'])
        sub.append(i['product_unit_price'])
        sub.append(i['product_quantity'])
        print("[{0}]- {1}, {2}, {3} per unit,{4} unit(s) available" .format(sub[0],sub[1], sub[2],sub[3], sub[4]))

    input("Press [ENTER] to continue..")

def product_random():

    global products

    if len(products) < 5:
        print("No five products available yet! Please be patient :D")
        input("Press [ENTER] to continue..")
        return None

    else:

        baggage = []
        for i in products:
            sub =[]
            sub.append(i['product_id'])
            sub.append(i['product_name'])
            sub.append(i['product_description'])
            sub.append(i['product_unit_price'])
            sub.append(i['product_quantity'])
            baggage.append(sub)
        loop = 0
        finalRandom = []
        while loop<5:
            randomProduct = random.choice(baggage)
            finalRandom.append(randomProduct)
            if randomProduct in baggage:
                baggage.remove(randomProduct)
                loop+=1

        print("Five (5) Random Products in LAPERA!")

        for i in finalRandom:
            sub = []
            sub.append(i[0])
            sub.append(i[1])
            sub.append(i[2])
            sub.append(i[3])
            sub.append(i[4])
            print("[{0}]- {1}, {2}, {3} per unit,{4} unit(s) available" .format(sub[0], sub[1],sub[2], sub[3], sub[4]))

        input("Press [ENTER] to continue..")