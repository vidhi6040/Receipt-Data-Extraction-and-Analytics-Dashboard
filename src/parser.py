import os
import json
import re
from datetime import datetime

RAW_FOLDER = "../raw_receipts"
JSON_FOLDER = "../json_receipts"

os.makedirs(JSON_FOLDER, exist_ok=True)

def receipt_parser(data):
    res = {}

    #Shop Name
    shop_name = re.search(r"\s*(.*?)\s*\n\s*ABN", data)
    res["shop_name"] = shop_name.group(1).strip() if shop_name else None

    #ABN Num
    abn_num = re.search(r"\s*ABN\s(\d+\s\d+\s\d+)\s*\n", data)
    res["abn_num"] = abn_num.group(1).replace(" ", "") if abn_num else None

    #Date
    date_block = re.search(r"\n\s*(\d{2}/\d{2}/\d{4})\s*\n", data)
    if date_block:
        date = datetime.strptime(date_block.group(1), "%d/%m/%Y")
        res["date"] = date.strftime("%Y-%m-%d")
        res["month"] = date.month
        res["year"] = date.year
    else:
        res["date"] = None
        res["month"] = None
        res["year"] = None

    #Terminal Num
    terminal_num = re.search(r"\nTerminal\s(\d+)\s*\n", data)
    res["terminal_num"] = terminal_num.group(1) if terminal_num else None

    #Cashier Name
    cashier_name = re.search(r"\nCashier\s(.+?)\s*\n", data)
    res["cashier_name"] = cashier_name.group(1) if cashier_name else None

    #Customer Name
    customer_name = re.search(r"\nCustomer\s(.+?)\s*\n", data)
    res["customer_name"] = customer_name.group(1) if customer_name else None

    #Items
    items = []
    item_section = re.search(r"Cashier.*?\n(.*?)\n\s*Subtotal", data, re.S)
    if item_section:
        section = item_section.group(1)
        item_block = re.finditer(
            r"([A-Za-z ]+)\s+(\d+)\s+(\d+\.\d{2})\s*\n\s*(\d+\.\d{2})",
            section
        )
        for item in item_block:
            items.append({
                "product_name": item.group(1).strip(),
                "quantity": int(item.group(2)),
                "unit_price": float(item.group(3)),
                "total_price": float(item.group(4))
            })
    res["items"] = items

    #Subtotal
    subtotal = re.search(r"\nSubtotal\s+([\d]+\.\d{2})\s*\n", data)
    res["subtotal"] = float(subtotal.group(1)) if subtotal else None

    #GST
    gst = re.search(r"GST\sIncluded\s+([\d]+\.\d{2})\s*\n", data)
    res["gst"] = float(gst.group(1)) if gst else None

    #Total
    total = re.search(r"\nTotal\s+([\d]+\.\d{2})\s*\n", data)
    res["total"] = float(total.group(1)) if total else None

    #Payments
    payments = []
    payment_block = re.finditer(r"^Payments\s*\n\s*([A-Za-z ]+)\s+(\d+\.\d{2})", data, re.M)
    for payment in payment_block:
        payment_mode = payment.group(1).strip()
        amount = float(payment.group(2))

        payments.append({
            "payment_mode": payment_mode,
            "amount": amount
        })
    res["payments"] = payments

    return res

def process_receipts():
    for files in os.listdir(RAW_FOLDER):
        if not files.endswith(".txt"):
            continue
        input_path = os.path.join(RAW_FOLDER, files)
        try:
            with open(input_path, 'r') as f:
                data = f.read()

            parsed_files = receipt_parser(data)

            json_file = files.replace(".txt", ".json")
            output_path = os.path.join(JSON_FOLDER, json_file)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(parsed_files, f, indent=4)

            

        except Exception as e:
            print(f"Error processing {files}: {e}")

if __name__ == "__main__":
    process_receipts()