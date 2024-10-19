class User:
    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role
        self.cart = Cart()
        self.payment = Payment(self)
        self.order_history = OrderHistory(self)

    def add_item_to_cart(self, item):
        self.cart.add_item(item)

    def checkout(self):
        if self.role == "admin":
            print("Admin can't make purchases.")
        else:
            if not self.cart.is_empty():
                self.payment.process_payment()
                self.order_history.add_order(self.cart)
            else:
                print("Cart is empty.")

    def view_order_history(self):
        self.order_history.show_orders()


class Cart:
    def __init__(self):
        self.items = []
        self.discount = Discount()  # High coupling with Discount class

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        total = sum(item.price for item in self.items)
        return self.discount.apply_discount(total)

    def is_empty(self):
        return len(self.items) == 0


class Payment:
    def __init__(self, user):
        self.user = user
        self.balance = 500  # High coupling with User class

    def process_payment(self):
        cart_total = self.user.cart.calculate_total()
        if cart_total > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= cart_total
            print(f"Payment successful! Remaining balance: {self.balance}")
            self.user.cart.items = []  # Clears cart after payment


class Discount:
    def __init__(self):
        self.fixed_discount = 10
        self.percentage_discount = 5

    def apply_discount(self, total):
        if total > 200:
            return total - (total * self.percentage_discount / 100)
        elif total > 100:
            return total - self.fixed_discount
        return total


class Item:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class OrderHistory:
    def __init__(self, user):
        self.user = user
        self.orders = []  # High coupling with User class

    def add_order(self, cart):
        self.orders.append(cart.items)
        print("Order added to history.")

    def show_orders(self):
        if not self.orders:
            print("No orders yet.")
        for order in self.orders:
            order_items = [f"{item.name}: {item.price}" for item in order]
            print(f"Order: {order_items}")


class Inventory:
    def __init__(self):
        self.items = [
            Item("Laptop", 800, "Electronics"),
            Item("Smartphone", 600, "Electronics"),
            Item("Desk Chair", 100, "Furniture"),
            Item("Notebook", 5, "Stationery")
        ]

    def display_items(self):
        for item in self.items:
            print(f"{item.name} - ${item.price} [{item.category}]")

    def find_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        print("Item not found.")
        return None


class Admin(User):
    def __init__(self, username, email):
        super().__init__(username, email, "admin")
        self.inventory = Inventory()  # Low modularity, Admin manages inventory and user tasks

    def add_new_item(self, name, price, category):
        new_item = Item(name, price, category)
        self.inventory.items.append(new_item)
        print(f"{new_item.name} added to inventory.")

    def remove_item(self, item_name):
        item = self.inventory.find_item(item_name)
        if item:
            self.inventory.items.remove(item)
            print(f"{item.name} removed from inventory.")


# Additional Features Leading to Increased Cyclomatic Complexity
class CouponManager:
    def __init__(self):
        self.active_coupons = {"SAVE10": 10, "DISCOUNT5": 5}

    def apply_coupon(self, cart, coupon_code):
        if coupon_code in self.active_coupons:
            discount_value = self.active_coupons[coupon_code]
            cart_total = cart.calculate_total()
            new_total = cart_total - (cart_total * discount_value / 100)
            print(f"Coupon applied! New total: ${new_total}")
            return new_total
        else:
            print("Invalid coupon.")
            return cart.calculate_total()


# Main program logic
if __name__ == "__main__":
    admin = Admin("admin1", "admin@example.com")
    admin.add_new_item("Tablet", 300, "Electronics")
    admin.inventory.display_items()

    user = User("johndoe", "johndoe@example.com", "customer")
    inventory = Inventory()

    # User browsing and purchasing items
    item = inventory.find_item("Laptop")
    if item:
        user.add_item_to_cart(item)

    item = inventory.find_item("Desk Chair")
    if item:
        user.add_item_to_cart(item)

    # Complex Checkout and Payment Process
    user.checkout()
    user.view_order_history()

    # Admin performs more inventory operations
    admin.remove_item("Tablet")
    admin.inventory.display_items()

    # Using CouponManager to apply a coupon
    coupon_manager = CouponManager()
    coupon_manager.apply_coupon(user.cart, "SAVE10")
