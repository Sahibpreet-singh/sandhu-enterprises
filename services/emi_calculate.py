from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_emi(
    item_amount,
    advance_amount,
    interest_rate,
    total_installments
):
    """
    Returns:
    finance_amount, total_interest, total_payable, installment_amount
    """

    finance_amount = item_amount - advance_amount

    total_interest = finance_amount * (interest_rate / 100)

    total_payable = finance_amount + total_interest

    installment_amount = round(total_payable / total_installments, 2)

    return {
        "finance_amount": round(finance_amount, 2),
        "total_interest": round(total_interest, 2),
        "total_payable": round(total_payable, 2),
        "installment_amount": installment_amount
    }


def generate_due_dates(start_date, total_installments, installment_mode):
    """
    installment_mode: MONTHLY / WEEKLY
    """
    due_dates = []
    current_date = start_date

    for _ in range(total_installments):
        due_dates.append(current_date)

        if installment_mode == "MONTHLY":
            current_date += relativedelta(months=1)
        elif installment_mode == "WEEKLY":
            current_date += relativedelta(weeks=1)

    return due_dates
