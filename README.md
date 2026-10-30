# Invoice Validator

A Python 3.12 project for importing and validating invoices from CSV files.

## CSV Columns

The input CSV files must contain the following columns:
- `invoice_id`
- `customer`
- `issue_date`
- `due_date`
- `net_amount`
- `discount_amount`

## Specifications

- **Dates**: Formatted as `DD/MM/YYYY`.
- **Money**: Handled as `decimal.Decimal`, rounded half-up to 2 decimal places.
- **Total Calculation**: The total is calculated as $(\text{net} - \text{discount}) \times 1.16$ (16% VAT applied after the discount).
- **Validation**: Invoice IDs must be unique; a repeated ID is rejected as an error. Invalid rows (bad dates, blank or invalid amounts, duplicate IDs) are added to an errors list with the row number and reason. The import process does not raise exceptions for standard bad rows.