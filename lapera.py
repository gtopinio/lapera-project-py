from cart import cart_init
from seller import *
from product import *
from sale import *
from buyer import *

def main():
    while True:
        print("Welcome to LAPERA Online Shopping!")
        print("\tOptions:")
        print("\t[1] Register Seller")
        print("\t[2] Register Buyer")
        print("\t[3] Login Seller")
        print("\t[4] Login Buyer")
        print("\t[5] View 5 random products")
        print("\t[q] Exit")
        choice = str(input("Please enter your choice: "))
        #Register Seller
        if choice == '1':
            seller_view_register()

        #Register Buyer
        elif choice == '2':
            buyer_view_register()
        
        #Login Seller
        elif choice == '3':
            seller_view_login()

        #Login Buyer
        elif choice == '4':
            buyer_view_login()

        #Five Random Products
        elif choice == '5':
            product_random()
        #Exit
        elif choice == 'q':
            print("Thank you for using LAPERA! Please come back again :D")
            exit()
        else:
            print("Invalid choice! Please Try again.")
#Everything init-related first
seller_init()
product_init()
sale_init()
buyer_init()
cart_init()
main()

#   CMSC-12 (CD) Project by Mark Genesis C. Topinio