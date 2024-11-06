# Vending Machine

# assumptions:
# machine will only accept $5, $2, $1, $0.25 and $0.10 denominations
# only one item can be purchased at a time
# money is inserted before item can be purchased
# on transaction cancelled, money inserted is refunded

# To run this program, just invovke using the python CLI
# > python vending-machine.py

from enum import Enum


class VendingItem:
    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count

    def print(self):
        print(f"Name {self.name}, price {self.price}")


class MoneyValue(Enum):
    FIVE_DOLLARS = 5.00
    TWO_DOLLARS = 2.00
    ONE_DOLLAR = 1.00
    QUARTER = 0.25
    DIME = 0.10


class Money:
    def __init__(
        self,
        five_dollar_count,
        two_dollar_count,
        one_dollar_count,
        quarter_count,
        dime_count,
    ):
        self.five_dollar_count = five_dollar_count
        self.two_dollar_count = two_dollar_count
        self.one_dollar_count = one_dollar_count
        self.quarter_count = quarter_count
        self.dime_count = dime_count

    def increment_value(self, money: MoneyValue):
        if money == MoneyValue.FIVE_DOLLARS:
            self.five_dollar_count += 1
        elif money == MoneyValue.TWO_DOLLARS:
            self.two_dollar_count += 1
        elif money == MoneyValue.ONE_DOLLAR:
            self.one_dollar_count += 1
        elif money == MoneyValue.QUARTER:
            self.quarter_count += 1
        elif money == MoneyValue.DIME:
            self.dime_count += 1

    def get_total_value(self):
        return (
            self.five_dollar_count * MoneyValue.FIVE_DOLLARS.value
            + self.two_dollar_count * MoneyValue.TWO_DOLLARS.value
            + self.one_dollar_count * MoneyValue.ONE_DOLLAR.value
            + self.quarter_count * MoneyValue.QUARTER.value
            + self.dime_count * MoneyValue.DIME.value
        )

    def print_quantity_values(self):
        print(
            f"Denominations: $5 x {self.five_dollar_count}, $2 x {self.two_dollar_count}, $1 x {self.one_dollar_count}, $0.25 x {self.quarter_count}, $0.10 x {self.dime_count}"
        )

    def calculate_change(amount):

        remainder = amount
        five_dollar_count = 0
        two_dollar_count = 0
        one_dollar_count = 0
        quarter_count = 0
        dime_count = 0

        print("Calculating amount of change")

        while remainder > 0:
            if remainder >= MoneyValue.FIVE_DOLLARS.value:
                remainder = round(remainder - MoneyValue.FIVE_DOLLARS.value, 2)
                five_dollar_count += 1
            elif remainder >= MoneyValue.TWO_DOLLARS.value:
                remainder = round(remainder - MoneyValue.TWO_DOLLARS.value, 2)
                two_dollar_count += 1
            elif remainder >= MoneyValue.ONE_DOLLAR.value:
                remainder = round(remainder - MoneyValue.ONE_DOLLAR.value, 2)
                one_dollar_count += 1
            elif remainder >= MoneyValue.QUARTER.value:
                remainder = round(remainder - MoneyValue.QUARTER.value, 2)
                quarter_count += 1
            else:
                remainder = round(remainder - MoneyValue.DIME.value, 2)
                dime_count += 1

        change = Money(
            five_dollar_count,
            two_dollar_count,
            one_dollar_count,
            quarter_count,
            dime_count,
        )

        return change


class VendingMachine:

    def __init__(self, name, money_inserted, item_selected, items):
        self.name = name
        self.item_selected = item_selected
        self.money_inserted = money_inserted
        self.items = items

    def get_item(self, name):
        return self.items[name]

    def select_item(self, name):
        if name not in self.items.keys():
            print("Invalid item selected")
            return

        self.item_selected = name

    def print_inventory(self):
        print("Displaying inventory")
        for k, v in self.items.items():
            print(f"Name: {k}, price: {v.price}, count: {v.count}")

    def add_items(self, name, price, count):
        self.items[name] = VendingItem(name, price, count)

    def update_items(self, name, item):
        self.items[name] = item

    def get_item_price(self, name):
        return self.items[name].price

    def purchase_item(self):
        if not self.item_selected:
            print("No item selected.")
            return

        print(f"Purchasing {self.item_selected}")

        item_to_purchase = self.items[self.item_selected]

        if item_to_purchase.count > 0:
            item_total = item_to_purchase.price

            if self.money_inserted.get_total_value() > item_total:
                change = Money.calculate_change(
                    self.money_inserted.get_total_value() - item_total
                )
                print(f"Dispensing change value of ${change.get_total_value():.2f}")
            else:
                print(
                    f"Payment insufficient. Funds available: ${self.money_inserted.get_total_value():.2f} "
                )
                return

            item_to_purchase.count -= 1
            self.update_items(self.item_selected, item_to_purchase)
            self.reset_transaction()

        else:
            print("Not enough items available to purchase")

        return (item_to_purchase, change)

    def cancel_transaction(self):
        print("Cancelling transaction")
        change = Money.calculate_change(self.money_inserted.get_total_value())

        print(f"Refunding amount ${self.money_inserted.get_total_value():.2f} ")
        change.print_quantity_values()
        self.reset_transaction()

        return change

    def insert_money(self, money: MoneyValue):
        self.money_inserted.increment_value(money)

    def display_money_inserted(self):
        print(f"Total amount inserted: ${self.money_inserted.get_total_value():.2f}")

    def reset_transaction(self):
        self.money_inserted = Money(0, 0, 0, 0, 0)
        self.item_selected = ""


vending_machine = VendingMachine("Unit 1", Money(0, 0, 0, 0, 0), "", {})

# the below logic runs through various test scenarios with the VendingMachine class
# insert items into the machine
vending_machine.add_items("Snickers", 1.25, 10)
vending_machine.add_items("Mars", 1.00, 15)
vending_machine.add_items("Starburst", 0.50, 20)

vending_machine.print_inventory()

vending_machine.get_item("Snickers").print()

vending_machine.insert_money(MoneyValue.FIVE_DOLLARS)
vending_machine.display_money_inserted()

# test a purchase
vending_machine.select_item("Snickers")
vending_machine.purchase_item()
vending_machine.print_inventory()

# test cancelling the current transaction
vending_machine.insert_money(MoneyValue.FIVE_DOLLARS)
vending_machine.cancel_transaction()
vending_machine.display_money_inserted()

# test attempting to buy an item when no money is inserted
vending_machine.select_item("Mars")
vending_machine.purchase_item()  # -> should be insufficient funds in the machine to purchase
vending_machine.insert_money(MoneyValue.TWO_DOLLARS)
vending_machine.insert_money(MoneyValue.QUARTER)

vending_machine.display_money_inserted()
vending_machine.select_item("Mars")
vending_machine.purchase_item()

vending_machine.print_inventory()
