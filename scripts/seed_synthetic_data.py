"""Seed script to insert synthetic customers, items, guarantors, and payments.

Usage:
    python scripts/seed_synthetic_data.py --count 50

This script uses the project's model helpers so it will work with the project's DB config.
"""
import os
import sys

# Ensure project root is on sys.path so imports like `models.*` resolve when run as a script
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import random
import argparse
from datetime import date, timedelta
from models.address_model import add_address, get_all_addresses
from models.village_model import add_village, get_all_villages
from models.customer_model import add_customer
from models.guarantor_model import add_guarantor
from models.item_model import add_item
from models.payment_model import add_payment

FIRST_NAMES = ["Raju","Sita","Amit","Neha","Rahul","Kavita","Vijay","Meera","Sunil","Pooja","Sameer","Anjali","Raj","Deepa","Suresh","Sonia","Aakash","Priya"]
LAST_NAMES = ["Sharma","Singh","Gupta","Patel","Kumar","Verma","Chaudhary","Joshi","Reddy","Nair"]
BRANDS = ["Samsung","LG","Sony","Panasonic","Whirlpool","Haier"]
MODELS = ["X100","A200","Pro","S-lite","V3","M7"]

phone_prefixes = ["98","97","96","95","94"]

random.seed(42)


def random_phone():
    return ''.join(random.choice('0123456789') for _ in range(10))


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_address(i):
    return f"{i} Main Road, Area {random.choice(['A','B','C','D'])}"


def seed(count=50):
    # Ensure a few villages and addresses exist
    villages = get_all_villages()
    if not villages:
        for v in ["Greenfield","Lakshmi Nagar","Riverside","Hillview","Sunset"]:
            add_village(v)
        villages = get_all_villages()

    addresses = get_all_addresses()
    if not addresses:
        for i in range(10):
            add_address(random_address(i+1))
        addresses = get_all_addresses()

    village_ids = [v['village_id'] for v in villages]
    address_ids = [a['address_id'] for a in addresses]

    created = {
        'customers': [],
        'items': [],
        'payments': []
    }

    for i in range(1, count+1):
        name = random_name()
        phone = random_phone()
        addr_choice = random.choice(address_ids)
        village_choice = random.choice(village_ids)
        remarks = random.choice([None, 'Good customer', 'Late payer'])
        entry_dt = date.today() - timedelta(days=random.randint(0, 365))

        customer_id = add_customer(name=name, phone=phone, address=random_address(i), remarks=remarks, address_id=addr_choice, village_id=village_choice, entry_date=entry_dt)
        created['customers'].append(customer_id)

        # Add 1 or 2 items per customer
        for j in range(random.choice([1, 1, 2])):
            brand = random.choice(BRANDS)
            model = random.choice(MODELS)
            item_amount = round(random.uniform(2000, 50000), 2)
            advance = round(item_amount * random.choice([0.05, 0.1, 0.15, 0.2]), 2)
            finance_amount = round(item_amount - advance, 2)

            # Randomly choose percent or amount interest
            if random.random() < 0.8:
                interest_type = 'PERCENT'
                interest_rate = round(random.uniform(1, 20), 2)
            else:
                interest_type = 'AMOUNT'
                interest_rate = round(random.uniform(100, 2000), 2)

            installments = random.choice([6, 12, 24, 36])
            installment_amount = round((finance_amount + (finance_amount * (interest_rate/100) if interest_type=='PERCENT' else float(interest_rate))) / installments, 2)
            start_date = date.today() - timedelta(days=random.randint(0, 90))

            item_id = add_item(
                customer_id=customer_id,
                brand=brand,
                model=model,
                serial_no=None,
                invoice_no=None,
                item_amount=item_amount,
                advance_amount=advance,
                finance_amount=finance_amount,
                interest_rate=interest_rate,
                installment_mode=random.choice(["MONTHLY","WEEKLY","DAILY","ONE-TIME"]),
                total_installments=installments,
                installment_amount=installment_amount,
                start_date=start_date,
                interest_type=interest_type
            )
            created['items'].append(item_id)

            # Add a guarantor sometimes
            if random.random() < 0.6:
                add_guarantor(customer_id, random_name(), random_phone(), random_address(i+100))

            # Add 0-N payments to create history (but not exceed payable)
            total_payable = finance_amount + (finance_amount * (interest_rate/100) if interest_type=='PERCENT' else float(interest_rate))
            paid_so_far = 0.0
            num_payments = random.choice([0, 0, 1, 2, 3])
            for p in range(num_payments):
                remaining = round(total_payable - paid_so_far, 2)
                pay = round(min(remaining, installment_amount + random.uniform(-10, 20)), 2)
                pay = max(pay, 0.01)
                pay_date = start_date + timedelta(days=30*(p+1))
                try:
                    remaining_after = add_payment(item_id, pay_date, pay, total_payable)
                    created['payments'].append((item_id, pay_date, float(pay), float(remaining_after)))
                    paid_so_far += pay
                except Exception:
                    # ignore payment errors
                    pass

    print(f"Inserted {len(created['customers'])} customers, {len(created['items'])} items, {len(created['payments'])} payments")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=50, help='Number of customers to create')
    args = parser.parse_args()
    seed(count=args.count)
