from dotenv import load_dotenv
load_dotenv()

import database as db
import pandas as pd
import os

"""
Steps to extract StockData and IndexData from the database and output the csv for each code:
1. Get all the codes from ListStock
2. Get all data from database all at once
3. Group by code
4. Output to csv
5. Repeat for IndexData
"""

def exportToCsv(TableClass:db.StockData|db.IndexData, data:pd.DataFrame, code:str):
    dir_path = f"data/{TableClass.__name__}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    data.to_csv(f"data/{TableClass.__name__}/{code}.csv", index=False)

def getFromDB(TableClass:db.StockData|db.IndexData, code:str) -> pd.DataFrame:
    dbs = next(db.get_dbs())
    query = dbs.query(TableClass).filter(TableClass.code == code).order_by(TableClass.date)
    data = pd.read_sql(sql=query.statement, con=dbs.bind) # type: ignore
    return data

def exportCode(TableClass:db.StockData|db.IndexData, codeList:pd.DataFrame):
    for code in codeList['code']:
        data = getFromDB(TableClass, code)
        exportToCsv(TableClass, data, code)

def main():
    # StockData
    # stockList = db.get_list_stock()
    # exportCode(db.StockData, stockList)
    # IndexData
    indexList = db.get_list_index()
    exportCode(db.IndexData, indexList)

if __name__ == "__main__":
    main()