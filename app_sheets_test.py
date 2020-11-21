from expense_logger import sheets_test, login_sheets

def main():
    login_sheets.login()

    sheet = sheets_test.get_sheet()

    sheets_test.get_sheet_data(sheet)

if __name__ == '__main__':
    main()