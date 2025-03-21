from fastapi import FastAPI
import pyodbc
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

def connect():
    return pyodbc.connect(os.getenv("SQLAZURECONNSTR_AZURE_SQL_CONNECTIONSTRING"))

@app.get("/", response_class=HTMLResponse)
def read_root():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM dbo.Course")
    columns = [column[0] for column in cursor.description]  # Get column names
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    
    # Generate HTML table
    html = "<table border='10'><tr>"
    html += "".join(f"<th>{col}</th>" for col in columns)
    html += "</tr>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table>"
    
    return html