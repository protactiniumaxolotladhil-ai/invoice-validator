from datetime import date
from decimal import Decimal
import pytest

from invoice_validator.importer import (
    parse_date,
    parse_amount,
    compute_total,
    import_invoices,
)


def test_parse_date():
    assert parse_date("03/04/2026") == date(2026, 4, 3)


def test_parse_amount():
    assert parse_amount("1.005") == Decimal("1.01")


def test_compute_total():
    assert compute_total(Decimal("1000.00"), Decimal("100.00")) == Decimal("1044.00")


def test_import_duplicate_id(tmp_path):
    csv_content = (
        "invoice_id,customer,issue_date,due_date,net_amount,discount_amount\n"
        "INV-001,Acme Corp,10/05/2026,10/06/2026,500.00,50.00\n"
        "INV-001,Beta LLC,11/05/2026,11/06/2026,300.00,30.00\n"
    )
    csv_file = tmp_path / "duplicates.csv"
    csv_file.write_text(csv_content)

    valid, errors = import_invoices(str(csv_file))
    assert len(valid) == 1
    assert len(errors) == 1


def test_import_blank_amount(tmp_path):
    csv_content = (
        "invoice_id,customer,issue_date,due_date,net_amount,discount_amount\n"
        "INV-002,Gamma Inc,10/05/2026,10/06/2026,,50.00\n"
    )
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text(csv_content)

    valid, errors = import_invoices(str(csv_file))
    assert len(errors) == 1
    assert "blank" in errors[0]["reason"].lower()


def test_compute_total_zero_discount():
    assert compute_total(Decimal("500.00"), Decimal("0.00")) == Decimal("580.00")
    

@pytest.mark.parametrize("raw, expected", [("2.675", 2.68), ("0.004", "0.00")])
def test_parse_amount_edges(raw, expected):
    assert parse_amount(raw) == Decimal(str(expected))
    
    
def test_parse_date_day_over_12():
    assert parse_date("31/12/2026") == date(2026, 12, 31)
    
def test_compute_total_full_discount():
    assert compute_total(Decimal("1000.00"), Decimal("1000.00")) == Decimal("0.00")