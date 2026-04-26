# Store items as (name, price)
cart = []

while True:# Keeps asking the user to input their option
    print("\n1. Add item")
    print("2. Remove item")
    print("3. View cart")
    print("4. Checkout")
    
    choice = input("Choose an option: ")

    if choice == "1":
        item = input("Enter item name: ")
        
        try:
            price = float(input("Enter price: "))  # Convert price to number
            cart.append((item, price))  # Store item + price
        except ValueError:
            print("Invalid price")

    elif choice == "2":
        item = input("Enter item to remove: ")
        
        # Remove item by name
        for i in cart:
            if i[0] == item:
                cart.remove(i)
                print(f"{item} removed.")
                break
        else:
            print("Item not in cart")

    elif choice == "3":
        if cart:
            for item, price in cart:
                print(f"{item} - MWK{price}")
        else:
            print("Cart is empty")

    elif choice == "4":
        break  # Go to checkout

    else:
        print("Invalid choice")


#  Calculate and print total at the end
total = 0
for item, price in cart:
    total += price

print("\n--- Checkout ---")
print(f"Total: MWK{total}")
