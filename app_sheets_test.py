from expense_logger import sheets_test, sheets_login

def main():
    sheets_login.login()

    sheet = sheets_test.get_sheet()

    sheets_test.get_sheet_data(sheet)

if __name__ == '__main__':
    main()