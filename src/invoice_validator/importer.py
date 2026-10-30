import csv
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%d/%m/%Y").date()


def parse_amount(s: str) -> Decimal:
    if s == "":
        raise ValueError("Amount cannot be blank")
    return Decimal(s.strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def compute_total(net: Decimal, discount: Decimal, vat_rate: float = 0.16) -> Decimal:
    total = (net - discount) * Decimal(str(1 + vat_rate))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def import_invoices(path: str):
    valid = []
    errors = []

    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=1):
            if not row.get("net_amount") or row["net_amount"].strip() == "":
                raise ValueError("Blank net amount")

            try:
                invoice_id = row["invoice_id"].strip()
                issue_date = parse_date(row["issue_date"])
                due_date = parse_date(row["due_date"])
                net_amount = parse_amount(row["net_amount"])
                discount_amount = parse_amount(row["discount_amount"])
                total = compute_total(net_amount, discount_amount)

                valid.append(
                    {
                        "invoice_id": invoice_id,
                        "customer": row["customer"],
                        "issue_date": issue_date,
                        "due_date": due_date,
                        "net_amount": net_amount,
                        "discount_amount": discount_amount,
                        "total": total,
                    }
                )
            except Exception as e:
                errors.append({"row": row_idx, "reason": str(e)})

    return valid, errors