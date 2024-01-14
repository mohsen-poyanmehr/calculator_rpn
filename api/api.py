from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, MetaData, Table
from databases import Database
from fastapi.responses import JSONResponse
import csv
from fastapi.middleware.cors import CORSMiddleware

# SQLite database URL
DATABASE_URL = "sqlite:///./my_database.db"

# SQLAlchemy Models
metadata = MetaData()

calculator = Table(
    "calculator",
    metadata,
    Column("expression", String, index=True),
    Column("result", String, index=True),
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

class Expression(BaseModel):
    expression: str

class Cal(BaseModel):
    expression: str
    result: str

from fastapi import FastAPI

app = FastAPI()

# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database instance
database = Database(DATABASE_URL)

# Dependency to get the database connection
async def get_database():
    if not database.is_connected:
        await database.connect()
    return database

# Dependency to get the SQLAlchemy model
def get_calculator_table():
    return calculator

def calculate_rpn(expressions: str):
    list1 =expressions.split(' ')
    list2=[]
    for e in list1 :
        if e.isdigit() or (e[0]=="-" and e[1:].isdigit()):
            list2.append(int(e))
        elif e in ['+','-','/','*']:
            if len(list2)>=2:
                y = list2.pop()
                x = list2.pop()
                if e == "+":
                    list2.append(x+y)
                elif e == "-":
                    list2.append(x-y)
                elif e == "*":
                    list2.append(x*y)
                else:
                    list2.append(x/y)
            else:
               raise Exception("operator must have two operands") 
        else:
            raise Exception("The input is not correct")
    return list2[0]

@app.get("/")
def read_root():
    return {"message": "Hello, Calculator!"}

# just calculatort
@app.get("/rpn/{expressions}")
def rpn(expressions: str):
    list1 =expressions.split(' ')
    list2=[]
    print(list1)
    for e in list1 :
        if e.isdigit() or (e[0]=="-" and e[1:].isdigit()):
            list2.append(int(e))
        elif e in ['+','-','/','*']:
            if len(list2)>=2:
                y = list2.pop()
                x = list2.pop()
                print(x)
                print(y)
                if e == "+":
                    list2.append(x+y)
                elif e == "-":
                    list2.append(x-y)
                elif e == "*":
                    list2.append(x*y)
                else:
                    list2.append(x/y)
            else:
               raise Exception("operator must have two operands") 
        else:
            raise Exception("The input is not correct")
    return list2[0]

# save result of expression of calculator in database
@app.post("/rpn_databse/")
# async def create_database(cal: Expression):
async def create_database(cal: Expression, db: Database = Depends(get_database), calculator=Depends(get_calculator_table)):
    try: 
        query = calculator.insert().values({"expression": cal.expression, "result":  calculate_rpn(cal.expression)})
        await db.execute(query)
        return JSONResponse(content={"message": "Data written to database successfully", "response":calculate_rpn(cal.expression)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to database: {str(e)}")

# save databse in file csv
@app.post("/csv/")
async def write_to_csv(db: Database = Depends(get_database), calculator_table=Depends(get_calculator_table), filename: str = "exported_data.csv"):    
    try:
        query = calculator_table.select()
        result = await db.fetch_all(query)
        list_my_dict=[]
        for row in result:
            list_my_dict.append({"expression":row[0],"result":row[1]})
        if not result:
            return JSONResponse(content={"message": "No data to export"}, status_code=200)
        
        with open(filename, 'a', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=result[0].keys())
            # Check if the file is empty and write header if needed
            if csvfile.tell() == 0:
                csv_writer.writeheader()
            
            # csv_writer.writerow(data2)
            csv_writer.writerows(list_my_dict)

        return JSONResponse(content={"message": "Data written to CSV successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to CSV: {str(e)}")
