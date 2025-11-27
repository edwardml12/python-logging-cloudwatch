from fastapi import FastAPI, HTTPException
from services.item import Item
from services.logger import logger
import logging

app = FastAPI(title="FastAPI on Lambda")

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

apm = make_apm_client()
app.add_middleware(ElasticAPM, client=apm)

import mysql.connector
from mysql.connector import Error

import os
from dotenv import load_dotenv
import json

load_dotenv()
import elasticapm
from elasticapm.handlers.logging import LoggingHandler

apm_client = elasticapm.get_client()
apm_handler = LoggingHandler(client=apm_client)
apm_handler.setLevel(logging.WARNING)  # only ERROR+ go to APM

logger.addHandler(apm_handler)

@app.get("/health")
def health_check():
    logger.debug("Health check endpoint called.")
    return {"status": "ok"}


@app.get("/mysqltest")
def mysql_test():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_URL"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_NAME"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
        )

        # print(connection.is_connected())

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM test")

            rows = cursor.fetchall()

            rows_list = [list(row) for row in rows]
            print("Rows:", rows)
            return json.dumps(rows_list)

    except Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.get("/items")
def create_item():
    try:
        item = Item(name="Sample", description="This is a sample item")
        return item.get_item()
    except Exception as e:
        return {"error": str(e)}


@app.get("/function_with_raise")
def function_with_raise():
    try:
        raise ValueError("An intentional error occurred.")
    except Exception as e:
        logger.error(f"Error in function_with_raise: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/function_with_error")
def function_with_error():
    try:
        call_function_not_implemented()
    except Exception as e:
        logger.error(f"Error in function_with_error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
