from fastapi import FastAPI
import pyodbc
from fastapi.responses import HTMLResponse
from azure.appconfiguration.provider import load
app = FastAPI()

def connect():
    config = load(connection_string="Endpoint=https://learningapp4000con.azconfig.io;Id=1i9U;Secret=ztfpPhi4UGzaTK3qpHEMs0ypXcrfc9JHkcxzkInOgxlfUhyrEyKPJQQJ99BCACi5YpzMNsX2AAACAZACeCa0")
    return pyodbc.connect(config["AZURE_SQL_CONNECTIONSTRING"])

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
    html = "<table border=1><tr>"
    html += "".join(f"<th>{col}</th>" for col in columns)
    html += "</tr>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table>"
    
    return html