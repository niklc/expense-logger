from expense_logger import sheets_test

class LogService:

    def log(self, amount: float, description: str) -> None:
        print(str(amount) + ' ' + description)

        sheet = sheets_test.get_sheet()

        row = [amount, description]

        sheets_test.apend_row(sheet, row)