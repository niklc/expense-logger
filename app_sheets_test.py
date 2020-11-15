import src.sheets_test
import src.login_sheets

def main():
    src.login_sheets.login()

    sheet = src.sheets_test.get_sheet()

    src.sheets_test.get_sheet_data(sheet)

if __name__ == '__main__':
    main()