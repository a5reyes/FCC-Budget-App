import math
class Category:
    instances = []
    def __init__(self, category, ledger=None, total=None):
        self.category = category
        self.ledger = []
        self.total = 0
        Category.instances.append(self)

    def __repr__(self):
        return str(self.category)

    def __str__(self):
        res = ""
        total_amount = 0
        centered_text = str(self.category).center(30, "*")
        for transaction in self.ledger:
            trans_description = transaction["description"]
            trans_amount = transaction["amount"]
            total_amount += trans_amount
            width = 30 - (len(trans_description) + len(f"{trans_amount:.2f}")) - 1
            max_width = 30 - max(len(repr(payment["amount"])) for payment in self.ledger) - 1
            res += f"{trans_description[:max_width]}" + " " * width + " " + f"{trans_amount:.2f}" + "\n"
        return centered_text + "\n" + res + f"Total: {total_amount:.2f}"


    def deposit(self, amount, description=None):
        self.total += amount
        if description is None:
            description = ""
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=None, transfer_category=None):
        if self.total > amount:
            self.total -= amount
            if description is None:
                description = ""     
            if transfer_category:
                self.ledger.append({"amount": -abs(amount), "description": "Transfer to " + transfer_category})
            else:
                self.ledger.append({"amount": -abs(amount), "description": description})
            return True
        else:
            return False
    
    def get_balance(self):
        return self.total

    def transfer(self, amount, description):
        withdrawal = self.withdraw(amount, self.category, repr(description))
        if (withdrawal):
            description.total += amount
            description.ledger.append({"amount": amount, "description": "Transfer from " + self.category})
            return True
        else:
            return False
    
    def check_funds(self, amount):
        if self.total < amount:
            return False
        return True

def create_spend_chart(categories):
    res = "Percentage spent by category\n"
    all_total = 0
    totals_arr = []

    for category in categories:
        category_total = 0
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                category_total += abs(transaction["amount"])
        totals_arr.append(round(category_total, 2))
        all_total += category_total

    for val in reversed(range(0, 101, 10)):
        res += str(val).rjust(3) + '|'
        for item_total in totals_arr:
            total_percent = item_total / round(all_total, 2) * 100
            rounded_percent = math.floor(total_percent / 10) * 10
            if val <= rounded_percent:
                res += " o "
            else:
                res += "   "
        res += " \n"

    bar_line = "    " + "-" * (3 * len(categories) + 1)
    res += bar_line
    max_len = max(len(repr(category)) for category in categories)
    for i in range(max_len):
        res += "\n     " + "  ".join(repr(category)[i] if i < len(repr(category)) else " " for category in categories) + "  "

    return res
 
