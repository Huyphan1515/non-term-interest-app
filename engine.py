import pandas as pd
def calculate_interest(df):
    RATE = 0.05
    TAX = 0.95

    balance = 0
    acc_interest = 0
    last_interest_date = None

    outputs = []

    for _, row in df.iterrows():
        date = pd.to_datetime(row["Ngày phát sinh GD"])
        hour = int(row["Giờ GD"])
        trans = row["Giao dịch"]

        deposit = float(row.get("Gốc nạp", 0) or 0)
        withdraw = float(row.get("Gốc rút", 0) or 0)
        revert_profit = float(row.get("Lợi nhuận revert", 0) or 0)

        interest_date = date if hour < 10 else date + pd.Timedelta(days=1)

        # --- TÍNH LÃI ---
        if last_interest_date is None:
            days = 0
            profit = 0
        else:
            days = max((interest_date - last_interest_date).days, 0)
            profit = balance * days * RATE / 365

        profit_after_tax = profit * TAX
        acc_interest += profit_after_tax

        # --- XỬ LÝ GIAO DỊCH ---
        if trans == "Tạo":
            balance = deposit

        elif trans == "Nạp":
            balance += deposit

        elif trans == "Rút":
            rut_ln = min(withdraw, acc_interest)
            rut_goc = max(withdraw - rut_ln, 0)

            acc_interest -= rut_ln
            balance -= rut_goc

        elif trans == "Revert":
            acc_interest -= revert_profit

        elif trans == "Tất toán":
            balance = 0
            acc_interest = 0

        outputs.append({
            "Ngày GD": date.date(),
            "Giao dịch": trans,
            "Ngày tính lãi": interest_date.date(),
            "Số ngày tính lãi": days,
            "Gốc cuối": round(balance),
            "LN phát sinh": round(profit),
            "LN lũy kế": round(acc_interest),
        })

        if last_interest_date is None or interest_date > last_interest_date:
            last_interest_date = interest_date

    return pd.DataFrame(outputs)
