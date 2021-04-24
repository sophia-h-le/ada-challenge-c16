class Customer:
    def __init__(self, customer_id, delivery_num, rush_num, meal_num, bundle_delivery_size):
        self.customer_id = customer_id
        self.delivery_num = delivery_num
        self.rush_num = rush_num
        self.meal_num = meal_num
        self.bundle_delivery_size = bundle_delivery_size
        (self.bundle_delivery_num, self.single_delivery_num) = divmod(delivery_num, bundle_delivery_size)
    def __str__(self):
        customer_str = f'custome_id: {self.customer_id}, delivery_num: {self.delivery_num}, bundle_delivery_num: {self.bundle_delivery_num}, single_delivery_num: {self.single_delivery_num}, rush_num: {self.rush_num}, meal_num: {self.meal_num}'
        return customer_str
        
class Pricelist:
    def __init__(self, single_delivery_price = 7.25, bundle_delivery_price = 60.00, rush_price = 2.00, meal_price = 12.50):
        self.single_delivery_price = single_delivery_price
        self.bundle_delivery_price = bundle_delivery_price
        self.rush_price = rush_price
        self.meal_price = meal_price
        
    def __str__(self):
        pricelist_str = f'single_delivery_price: {self.single_delivery_price}, bundle_delivery_price: {self.bundle_delivery_price}, rush_price: {self.rush_price}, meal_price: {self.meal_price}'
        return pricelist_str
        
class Receipt:
    def __init__(self, customer, pricelist):
        self.customer_id = customer.customer_id
        self.delivery_fees = (customer.single_delivery_num * pricelist.single_delivery_price) + (customer.bundle_delivery_num * pricelist.bundle_delivery_price)
        self.rush_fees = customer.rush_num * pricelist.rush_price
        self.meal_fees = customer.meal_num * pricelist.meal_price
        self.total_fees = self.delivery_fees + self.rush_fees + self.meal_fees
        
    def __str__(self):
        receipt_str = f'''Customer {self.customer_id} paid ${self.total_fees:.2f} total
>>> ${self.delivery_fees:.2f} in delivery fees
>>> ${self.rush_fees:.2f} in rush delivery fees
>>> ${self.meal_fees:.2f} in meal fees
'''
        return receipt_str

class Summary:
    def __init__(self, receipt_list):
        self.receipt_list = receipt_list
        self.combined_total_fees = sum(receipt.total_fees for receipt in receipt_list)
        self.combined_delivery_fees = sum(receipt.delivery_fees for receipt in receipt_list) + sum(receipt.rush_fees for receipt in receipt_list)
        self.highest_total_fees = max(receipt.total_fees for receipt in receipt_list)
    
    def get_highest_paid_customers(self):
        highest_paid_customers = []
        for receipt in self.receipt_list:
            if receipt.total_fees == self.highest_total_fees:
                highest_paid_customers.append(receipt.customer_id)
        self.highest_paid_customers = highest_paid_customers
        
    def __str__(self):
        summary_str = f'''Combined all customers paid ${self.combined_total_fees:.2f} total
Delivery fees (standard and Rush Delivery) were ${self.combined_delivery_fees:.2f} total

${self.highest_total_fees:.2f} was the most paid by any single customer
The customer(s) that paid the most were: #{', #'.join(str(customer_id) for customer_id in self.highest_paid_customers)}'''
        return summary_str
        
def delivery_summary(deliveries_ordered, rush_deliveries, meals_purchased):
    # print("Welcome to the Ada Meal Delivery Dashboard")
    # print()
    # debugged - non-breaking space
    
    print('''Welcome to the Ada Meal Delivery Dashboard
    ''')
    bundle_delivery_size = 10
    customer_list = []
    for i in range(len(deliveries_ordered)):
        customer_id = i + 1
        delivery_num = deliveries_ordered[i]
        rush_num = rush_deliveries[i]
        meal_num = meals_purchased[i]
        customer = Customer(customer_id, delivery_num, rush_num, meal_num, bundle_delivery_size)
        customer_list.append(customer)
        # print(customer.__str__())
        # to check instantiating correctly
    
    pricelist = Pricelist()
    # print(pricelist.__str__())
    # to check instantiating correctly
    receipt_list = []
    for customer in customer_list:
        receipt = Receipt(customer, pricelist)
        receipt_list.append(receipt)
        print(receipt.__str__())
    
    summary = Summary(receipt_list)
    summary.get_highest_paid_customers()
    print(summary.__str__())
    
