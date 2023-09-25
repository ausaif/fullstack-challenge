import sqlite3
from uuid import uuid4

import pandas as pd

DB_NAME = "../backend/enodo.db"


def load_class_table(file, sheet):
    columns = {'OVACLS': 'class_id',
               'CLASS_DESCRIPTION': 'description'}
    df = pd.read_excel(file, sheet_name=sheet,
                       usecols=list(columns.keys()))
    df = df.rename(columns=columns).drop_duplicates()
    df['description'] = df['description'].map(str.strip)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("delete from class")
        count = df.to_sql('class', conn, index=False, if_exists='append', method='multi')
        print(f"{count} records inserted to class table")


def load_property_table(file, sheet):
    columns = {'Full Address': 'full_address', 'OVACLS': 'class_id',
               'ESTIMATED_MARKET_VALUE': 'estimated_market_value', 'BLDG_USE': 'building_use',
               'BUILDING_SQ_FT': 'building_sq_ft'}
    df = pd.read_excel(file, sheet_name=sheet,
                       usecols=list(columns.keys()))
    df['property_id'] = df.index.map(lambda _: str(uuid4()))
    df = df.rename(columns=columns)
    df['full_address'] = df['full_address'].map(str.strip)
    df['building_use'] = df['building_use'].fillna("").map(str.strip)
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("delete from property")
        count = df.to_sql('property', conn, index=False, if_exists='append', method='multi')
        print(f"{count} records inserted to property table")


def main():
    data_file = "../Enodo_Skills_Assessment_Data_File.xlsx"
    sheet = "Sheet1"
    with open(data_file, mode='rb') as file:
        load_class_table(file, sheet)
        load_property_table(file, sheet)


if __name__ == '__main__':
    main()
