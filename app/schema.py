# Project: Create app/schema.py with nested LineItem, VendorInfo, and InvoiceSchema.
# Fail validation if the sum of item subtotals + tax != total.

import json
import logging
import math
from typing import List, Optional
import warnings
warnings.filterwarnings("ignore")
from pydantic import BaseModel, Field, model_validator

logging.basicConfig(
    filename="invoice.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    # level=logging.info
    filemode='w'
)


class LineItem(BaseModel):
    description: str = ""
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

    @property
    def subtotal(self) -> float:
        return self.price * self.quantity


class VendorInfo(BaseModel):
    name: str = ""
    address: Optional[str] = None


class InvoiceSchema(BaseModel):
    vendor: VendorInfo
    items: List[LineItem] = Field(default_factory=list)
    tax: float = Field(ge=0, default=0.0)
    total: float = Field(ge=0)

    @model_validator(mode="after")
    def invoice_checker(self):
        subtotal = sum(item.subtotal for item in self.items)
        expected_total = subtotal + self.tax

        if math.isclose(self.total, expected_total, rel_tol=1e-9, abs_tol=1e-9):
            logging.info("Invoice Created Successfully!")
        else:
            logging.error("Value Mismatch: expected %s, got %s", expected_total, self.total)


with open(r"D:\30 Days Goal\ledgermind-ai\app\invoices.json", "r", encoding="utf-8") as file:
    invoices = json.load(file)

for index, invoice_data in enumerate(invoices, start=1):
    try:
        invoice = InvoiceSchema(**invoice_data)
        logging.info(f"Invoice {index} passed")
        print(f"Invoice {index} -> Passed")
    except Exception as e:
        logging.error(f"Invoice {index} failed: {e}")
        print(f"Invoice {index} -> Failed: {e}")
