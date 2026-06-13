import pandas as pd
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional

# ======================
# 1. Financial Records
# ======================
class FinancialRecord:
    def __init__(self, record_id: str, amount: float, description: str, date: str, category: str, status: str = "Unreconciled"):
        self.record_id = record_id
        self.amount = amount
        self.description = description
        self.date = date
        self.category = category  # e.g., Revenue, Expense, Asset, Liability
        self.status = status  # Reconciled, Unreconciled, Discrepancy

    def mark_as_reconciled(self):
        self.status = "Reconciled"

    def mark_as_discrepancy(self):
        self.status = "Discrepancy"

    def __repr__(self):
        return f"FinancialRecord(id={self.record_id}, amount={self.amount}, description='{self.description}', date={self.date}, category={self.category}, status={self.status})"

# ======================
# 2. Bank Reconciliation
# ======================
class BankReconciliation:
    def __init__(self, bank_account: str, statement_date: str):
        self.bank_account = bank_account
        self.statement_date = statement_date
        self.records: List[FinancialRecord] = []
        self.bank_statement_balance: float = 0.0
        self.book_balance: float = 0.0
        self.discrepancies: List[Dict] = []

    def add_record(self, record: FinancialRecord):
        self.records.append(record)
        if record.category in ["Revenue", "Asset"]:
            self.book_balance += record.amount
        elif record.category in ["Expense", "Liability"]:
            self.book_balance -= record.amount

    def reconcile(self, bank_statement_balance: float):
        self.bank_statement_balance = bank_statement_balance
        for record in self.records:
            if abs(record.amount - bank_statement_balance) < 0.01:  # Simulate matching
                record.mark_as_reconciled()
            else:
                record.mark_as_discrepancy()
                self.discrepancies.append({
                    "record_id": record.record_id,
                    "amount": record.amount,
                    "description": record.description,
                    "date": record.date,
                    "discrepancy_type": "Amount Mismatch"
                })
        return {
            "bank_statement_balance": self.bank_statement_balance,
            "book_balance": self.book_balance,
            "discrepancies": self.discrepancies,
            "reconciliation_date": datetime.now().strftime("%Y-%m-%d")
        }

# ======================
# 3. Journal Entries
# ======================
class JournalEntry:
    def __init__(self, entry_id: str, date: str, description: str):
        self.entry_id = entry_id
        self.date = date
        self.description = description
        self.debits: List[Dict] = []
        self.credits: List[Dict] = []

    def add_debit(self, account: str, amount: float):
        self.debits.append({"account": account, "amount": amount})

    def add_credit(self, account: str, amount: float):
        self.credits.append({"account": account, "amount": amount})

    def is_balanced(self) -> bool:
        total_debits = sum(debit["amount"] for debit in self.debits)
        total_credits = sum(credit["amount"] for credit in self.credits)
        return abs(total_debits - total_credits) < 0.01

    def __repr__(self):
        return f"JournalEntry(id={self.entry_id}, date={self.date}, description='{self.description}', debits={self.debits}, credits={self.credits})"

# ======================
# 4. Month-End Close
# ======================
class MonthEndClose:
    def __init__(self, month: str, year: int):
        self.month = month
        self.year = year
        self.accruals: List[Dict] = []
        self.prepayments: List[Dict] = []
        self.allocations: List[Dict] = []
        self.journal_entries: List[JournalEntry] = []
        self.status = "In Progress"  # In Progress, Completed

    def add_accrual(self, description: str, amount: float, account: str):
        self.accruals.append({
            "description": description,
            "amount": amount,
            "account": account,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

    def add_prepayment(self, description: str, amount: float, account: str):
        self.prepayments.append({
            "description": description,
            "amount": amount,
            "account": account,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

    def add_allocation(self, description: str, amount: float, from_account: str, to_account: str):
        self.allocations.append({
            "description": description,
            "amount": amount,
            "from_account": from_account,
            "to_account": to_account,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

    def add_journal_entry(self, entry: JournalEntry):
        if entry.is_balanced():
            self.journal_entries.append(entry)
        else:
            raise ValueError("Journal entry is not balanced!")

    def complete_close(self):
        self.status = "Completed"
        return {
            "month": self.month,
            "year": self.year,
            "accruals": self.accruals,
            "prepayments": self.prepayments,
            "allocations": self.allocations,
            "journal_entries": self.journal_entries,
            "status": self.status
        }

# ======================
# 5. Internal Audits
# ======================
class InternalAudit:
    def __init__(self, audit_id: str, scope: str, start_date: str, end_date: str):
        self.audit_id = audit_id
        self.scope = scope
        self.start_date = start_date
        self.end_date = end_date
        self.findings: List[Dict] = []
        self.corrective_actions: List[Dict] = []
        self.status = "In Progress"  # In Progress, Completed

    def add_finding(self, description: str, severity: str, category: str):
        self.findings.append({
            "description": description,
            "severity": severity,  # Low, Medium, High
            "category": category,  # e.g., Financial, Operational, Compliance
            "date_identified": datetime.now().strftime("%Y-%m-%d")
        })

    def add_corrective_action(self, finding_description: str, action: str, owner: str, deadline: str):
        self.corrective_actions.append({
            "finding_description": finding_description,
            "action": action,
            "owner": owner,
            "deadline": deadline,
            "status": "Open"  # Open, In Progress, Completed
        })

    def complete_audit(self):
        self.status = "Completed"
        return {
            "audit_id": self.audit_id,
            "scope": self.scope,
            "findings": self.findings,
            "corrective_actions": self.corrective_actions,
            "status": self.status
        }

# ======================
# 6. Payment Discrepancies
# ======================
class PaymentDiscrepancy:
    def __init__(self, discrepancy_id: str, payment_type: str, amount: float, description: str, date: str):
        self.discrepancy_id = discrepancy_id
        self.payment_type = payment_type  # Incoming, Outgoing
        self.amount = amount
        self.description = description
        self.date = date
        self.status = "Open"  # Open, Investigating, Resolved
        self.resolution: Optional[str] = None

    def investigate(self, notes: str):
        self.status = "Investigating"
        self.notes = notes

    def resolve(self, resolution: str):
        self.status = "Resolved"
        self.resolution = resolution

    def __repr__(self):
        return f"PaymentDiscrepancy(id={self.discrepancy_id}, type={self.payment_type}, amount={self.amount}, description='{self.description}', status={self.status})"

# ======================
# 7. Financial Analysis
# ======================
class FinancialAnalyzer:
    @staticmethod
    def detect_discrepancies(records: List[FinancialRecord]) -> List[FinancialRecord]:
        discrepancies = []
        for record in records:
            if record.status == "Discrepancy":
                discrepancies.append(record)
        return discrepancies

    @staticmethod
    def generate_financial_report(records: List[FinancialRecord], start_date: str, end_date: str) -> Dict:
        filtered_records = [r for r in records if start_date <= r.date <= end_date]
        total_revenue = sum(r.amount for r in filtered_records if r.category == "Revenue")
        total_expenses = sum(r.amount for r in filtered_records if r.category == "Expense")
        net_income = total_revenue - total_expenses
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "total_records": len(filtered_records),
            "discrepancies": len([r for r in filtered_records if r.status == "Discrepancy"])
        }

# ======================
# Example Usage
# ======================
if __name__ == "__main__":
    # --- Financial Records ---
    record1 = FinancialRecord("R001", 5000.0, "Client Payment", "2024-06-01", "Revenue")
    record2 = FinancialRecord("R002", 2000.0, "Office Supplies", "2024-06-02", "Expense")
    record3 = FinancialRecord("R003", 3000.0, "Rent", "2024-06-03", "Expense")
    record4 = FinancialRecord("R004", 10000.0, "Invoice Payment", "2024-06-04", "Revenue")

    # --- Bank Reconciliation ---
    reconciliation = BankReconciliation("Chase Business", "2024-06-30")
    reconciliation.add_record(record1)
    reconciliation.add_record(record2)
    reconciliation.add_record(record3)
    reconciliation.add_record(record4)
    reconciliation_result = reconciliation.reconcile(bank_statement_balance=12000.0)
    print("\n--- Bank Reconciliation Result ---")
    print(reconciliation_result)

    # --- Journal Entries ---
    entry1 = JournalEntry("JE001", "2024-06-01", "Record Client Payment")
    entry1.add_debit("Accounts Receivable", 5000.0)
    entry1.add_credit("Revenue", 5000.0)

    entry2 = JournalEntry("JE002", "2024-06-02", "Record Office Supplies Expense")
    entry2.add_debit("Office Supplies Expense", 2000.0)
    entry2.add_credit("Cash", 2000.0)

    print("\n--- Journal Entries ---")
    print(entry1)
    print(entry2)

    # --- Month-End Close ---
    month_end = MonthEndClose("June", 2024)
    month_end.add_accrual("Salaries Accrual", 15000.0, "Salaries Payable")
    month_end.add_prepayment("Insurance Prepayment", 3000.0, "Prepaid Insurance")
    month_end.add_allocation("Allocate Overhead", 5000.0, "Overhead", "Department A")
    month_end.add_journal_entry(entry1)
    month_end.add_journal_entry(entry2)
    month_end_result = month_end.complete_close()
    print("\n--- Month-End Close Result ---")
    print(month_end_result)

    # --- Internal Audits ---
    audit = InternalAudit("AUDIT-2024-001", "Financial Records Review", "2024-06-01", "2024-06-30")
    audit.add_finding("Unreconciled bank transactions", "High", "Financial")
    audit.add_finding("Missing supporting documents", "Medium", "Compliance")
    audit.add_corrective_action(
        "Unreconciled bank transactions",
        "Reconcile all bank transactions by EOM",
        "Accounting Team",
        "2024-06-25"
    )
    audit_result = audit.complete_audit()
    print("\n--- Internal Audit Result ---")
    print(audit_result)

    # --- Payment Discrepancies ---
    discrepancy1 = PaymentDiscrepancy("D001", "Incoming", 5000.0, "Client overpayment", "2024-06-05")
    discrepancy1.investigate("Checking client contract for correct amount")
    discrepancy1.resolve("Refunded excess amount to client")

    discrepancy2 = PaymentDiscrepancy("D002", "Outgoing", 1500.0, "Vendor underpayment", "2024-06-10")
    discrepancy2.investigate("Reviewing vendor invoice")
    discrepancy2.resolve("Processed additional payment to vendor")

    print("\n--- Payment Discrepancies ---")
    print(discrepancy1)
    print(discrepancy2)

    # --- Financial Analysis ---
    records = [record1, record2, record3, record4]
    discrepancies = FinancialAnalyzer.detect_discrepancies(records)
    report = FinancialAnalyzer.generate_financial_report(records, "2024-06-01", "2024-06-30")

    print("\n--- Discrepancies Detected ---")
    for discrepancy in discrepancies:
        print(discrepancy)

    print("\n--- Financial Report (June 2024) ---")
    print(report)
