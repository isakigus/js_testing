import os
import xlrd
from mappings import JS_Settings_mappings

path_xlsx = 'Publisher information.xlsx'
drivers = ['fox', 'chrome', 'ie']


def download_data_file(filename, spreadsheet_key):
    cmd = 'drive download -i %s --format xlsx' % spreadsheet_key
    if os.path.isfile(filename):
        os.system('rm "%s"' % filename)
    os.system(cmd)


def get_cookies_times_data(key, download=False):

    if download:
        download_data_file(path_xlsx, key)

    raw_data, data = parse_file(path_xlsx, 'JS Settings'), []

    for row in raw_data:
        try:
            if row[0].lower() == 'current' and row[3] == 'ctxjs':
                aux = {}
                for k, v in JS_Settings_mappings.items():
                    aux[k] = row[v + 1]
                data.append(aux)
        except:
            pass

    return data


def parse_file(path, sheet_name):

    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_name(sheet_name)

    print book

    # read rows
    i = 0
    row = first_sheet.row_values(i)
    yield row
    while row:
        i += 1
        try:
            row = first_sheet.row_values(i)
            yield row
        except:
            row = None
            pass


def get_tests_data(key):

    for rec in get_cookies_times_data(key):
        if not rec.get('pid'):
            continue

        for driver in drivers:
            pid = int(float(rec.get('pid')))

            yield {'function': 'test_cookies',
                   'name': 'ctx_cookie_times_%s_%s' % (pid, rec.get('name')),
                   'test_args': {'driver': driver, 'data': rec, 'mode': 'ctx'}
                   }

            yield {'function': 'test_cookies',
                   'name': 'ron_cookie_times_%s_%s' % (pid, rec.get('name')),
                   'test_args': {'driver': driver, 'data': rec, 'mode': 'ron'}
                   }
