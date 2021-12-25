import getpass, os, hashlib, datetime
from globals import *
from product import *
from cart import *

def buyer_init():

    if not os.path.exists("data/buyer.db"):
        buyer_db_handle = open("data/buyer.db","w")
        buyer_db_handle.close()
    buyer_load_db()

def buyer_load_db():

    global buyers

    buyer_db_handle = open("data/buyer.db","r")

    lines = buyer_db_handle.readlines()

    buyers.clear()

    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")
        
        buyers.append(buyer_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4]
                                              ))

    buyer_db_handle.close()

def buyer_create_dict( buyer_id,
                        buyer_email,
                        buyer_first_name,
                        buyer_last_name,
                        buyer_password_hash
                    ):

    new_buyer_dict = {}

    new_buyer_dict["buyer_id"] = buyer_id
    new_buyer_dict["buyer_email"] = buyer_email
    new_buyer_dict["buyer_first_name"] = buyer_first_name
    new_buyer_dict["buyer_last_name"] = buyer_last_name 
    new_buyer_dict["buyer_password_hash"] = buyer_password_hash

    return new_buyer_dict

def buyer_view_register():

    global buyers 

    print(">>[Register Buyer]<<")
    
    new_buyer_dict = {}

    new_buyer_dict['buyer_id'] = str(len(buyers))

    email=str(input("Email: "))
    while buyer_email_exists(email):
        print(email + " already exists! Please use another email")
        email=str(input("Email: "))
  
    new_buyer_dict["buyer_email"] = email

    new_buyer_dict["buyer_first_name"] = str(input("First Name: "))
    new_buyer_dict["buyer_last_name"] = str(input("Last Name: "))
    
    matched = False
    while not matched:
        password_hash_1 = hashlib.sha256(getpass.getpass("Password: ").encode('utf-8')).hexdigest()
        password_hash_2 = hashlib.sha256(getpass.getpass("Retype Password: ").encode('utf-8')).hexdigest()
        #TODO: Make sure the password is not empty
        if password_hash_1 != password_hash_2:
            print("Password did not match! ")
        else:
            matched = True

    new_buyer_dict["buyer_password_hash"] = password_hash_1

    buyer_save_dict(new_buyer_dict)

    buyer_load_db()

def buyer_email_exists(email_to_check):

    global buyers

    for buyer in buyers:
        if buyer["buyer_email"] == email_to_check:
            return True
    return False

def buyer_save_dict(buyer_dict):

    buyer_db_handle = open("data/buyer.db","a+")
    
    output_line = str(buyer_dict["buyer_id"]+","+
                    buyer_dict["buyer_email"]+","+
                    buyer_dict["buyer_first_name"]+","+ 
                    buyer_dict["buyer_last_name"]+","+ 
                    buyer_dict["buyer_password_hash"]+"\n") 

    buyer_db_handle.write(output_line)
    buyer_db_handle.close()

def buyer_view_login():

    global user_session

    input_email = str(input("Email: "))

    input_password_hash = hashlib.sha256(getpass.getpass("Password: ").encode('utf-8')).hexdigest()

    login_valid = False

    for buyer in buyers:
        if buyer["buyer_email"] == input_email:
            if buyer["buyer_password_hash"] == input_password_hash:
                login_valid = True
                break  

    if login_valid == True:
        print("\nWelcome " + buyer["buyer_first_name"] + "!" )

        session_id = buyer["buyer_id"]
        
        user_session = {"session_id":session_id,"session_details":buyer}

        buyer_view_menu()
    else:
        input("Unknown buyer! Press [ENTER] to continue.")

def buyer_view_add_to_cart():
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

    loop = True
    id_valid = False

    while loop:
        choice = str(input("Add to cart? [y/n]: "))
        
        if choice == 'n':
            loop = False
            return None
            
        elif choice =='y':
            loop = False
            id_check = str(input("Enter product id of item: "))
            for product in matches:
                if id_check == product['product_id']: #checks if product id exists
                    id_valid = True
        else:
            print("Invalid response. Please try again.")

    if id_valid == True:
        buyer_flush_cart(id_check)
    elif id_valid == False and choice == 'n':
        return None
    else:
        print("Product ID is invalid. Please try again.")
        input("Press [ENTER] to continue..")
        return None

def buyer_flush_cart(id_check):

    global products
    global carts
    global user_session

    new_cart_dict = {}
    cart =[]

    cart_quantity = int(input("How many units of the product? "))
    for i in products:
            if i['product_id'] == id_check and cart_quantity > int(i['product_quantity']) or cart_quantity <= 0:
               print("Number of units is invalid. Please try again.")
               input("Press [ENTER] to continue..")
               return buyer_view_menu()
            else:
                new_cart_dict['cart_id'] = str(len(carts))
                new_cart_dict['cart_buyer_id'] = str(user_session['session_id'])
                new_cart_dict['cart_product_id'] = str(id_check)
                new_cart_dict['cart_quantity'] = str(cart_quantity)
                new_cart_dict['cart_checkedout'] = "0"
                new_cart_dict['cart_date'] = str(datetime.datetime.now())

    for i in new_cart_dict.values():
        cart.append(i)
    
    print(','.join(cart) )

    cart_save_dict(new_cart_dict)
    cart_load_db() 
    

def buyer_view_total_expenses():

    global sales
    global user_session

    expenses = 0
    for sale in sales:
        if sale['sale_buyer_id'] == user_session["session_id"]:
            expenses += int(sale['sale_total_amount'])
    
    print("Your total expenses:", expenses)
    input("Press [ENTER] to continue..")

    return None

def buyer_view_carts_display():

    global carts
    global user_session
    
    count = 0

    print("Below are the contents of your cart")
    for cart in carts:
        for product in products:
            if cart['cart_buyer_id']==user_session["session_id"] and cart['cart_product_id'] == product['product_id'] and cart['cart_checkedout'] == "0":
                print("[{0}] - {1} - {2}".format(cart['cart_id'], product['product_name'], cart['cart_quantity']))
                count += 1
    
    print("There are", count,"item(s)")

    loop = True

    while loop:
        response = str(input("Checkout an item?[y/n] "))
        
        if response == 'n':
            loop = False
            return None
        elif response =='y' and count>0:
            loop = False
            cart_view_checkout()
        elif response =='y' and count<=0:
            loop = False
            print("Invalid. There's nothing in your cart.")
            input("Press [ENTER] to continue..")
            return None
        else:
            print("Invalid response. Please try again.")
            input("Press [ENTER] to continue..")
            return None

def buyer_view_menu():

    choice = '8'
    while choice != 'q':
        print(">>[Buyer Menu]<<")
        print("[1] Search/Add to cart ")
        print("[2] View Cart ")
        print("[3] View total expenses amount ")
        print("[q] Exit ")
        choice = str(input("Enter choice: "))
        if choice == "1":
            buyer_view_add_to_cart()
        
        elif choice == "2":
            buyer_view_carts_display()

        elif choice == "3":
            buyer_view_total_expenses()