from dataclasses import dataclass
import logging
import math
import json

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=10,
    filemode='w'
)


@dataclass
class InvoiceRaw:
    subtotal : float = 0
    tax : float = 0
    total : float = 0
    
    def __post_init__(self):
        checking = self.subtotal + self.tax
        if not math.isclose(checking, self.total):
            logging.error( 
                "Invoice total mismatch: subtotal=%s, tax=%s, total=%s",
                self.subtotal, self.tax, self.total
            )


with open(r"D:\30 Days Goal\ledgermind-ai\data.json", "r") as f:
    data = json.load(f)
    
for d in data:
    invoice = InvoiceRaw(d.get("subtotal"), d.get("tax"), d.get("total"))
    print(invoice)

