import src.sheets_test

class LogService:

    def log(self, amount: float, description: str) -> None:
        print(str(amount) + ' ' + description)

        sheet = src.sheets_test.get_sheet()

        row = [amount, description]

        src.sheets_test.apend_row(sheet, row)