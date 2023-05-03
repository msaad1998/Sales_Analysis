import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='sales')
def load_data():
    data=pd.read_csv("products.csv")
    engine = create_engine('mysql+pymysql://root:@localhost:3306/sales')
    columns_to_keep = ['product_id', 'category', 'product_weight']
    data = data[columns_to_keep]
    data.to_sql(name='products',  con=engine,if_exists = 'append', index=False)

    data=pd.read_csv("customers.csv")
    columns_to_keep = ['customer_id', 'zip_code', 'city', 'state']
    data = data[columns_to_keep]
    data.to_sql(name='customers',  con=engine,if_exists = 'append', index=False)

    data=pd.read_csv("sellers.csv")
    columns_to_keep = ['seller_id', 'zip_code', 'city', 'state']
    data = data[columns_to_keep]
    data.to_sql(name='seller',  con=engine,if_exists = 'append', index=False)

    data=pd.read_csv("timet.csv")
    columns_to_keep = ['time_id', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date','order_estimated_delivery_date']
    data = data[columns_to_keep]
    data.to_sql(name='timet',  con=engine,if_exists = 'append', index=False)

    data = pd.read_csv("sales_fact.csv")

    columns_to_keep = ['id', 'product_id', 'customer_id', 'seller_id', 'order_id', 'time_id', 'revenue']
    data = data[columns_to_keep]
    data.to_sql(name='sales_fact', con=engine, if_exists='append', index=False)


#creating tables in database sales in xampp

def create_schema():
    cursor = cnx.cursor()
    query = """CREATE TABLE products (
                    product_id VARCHAR(255) PRIMARY KEY,
                    category VARCHAR(255),
                    product_weight DECIMAL(10,2)
                )"""
    cursor.execute(query)

    query = """CREATE TABLE customers (
                    customer_id VARCHAR(255) PRIMARY KEY,
                    zip_code VARCHAR(255),
                    city VARCHAR(255),
                    state VARCHAR(255)
                )"""
    cursor.execute(query)

    query = """CREATE TABLE seller (
                       seller_id VARCHAR(255) PRIMARY KEY,
                       zip_code VARCHAR(255),
                       city VARCHAR(255),
                       state VARCHAR(255)
                   )"""
    cursor.execute(query)

    query = """CREATE TABLE timet (
                    time_id INT PRIMARY KEY,
                    order_approved_at VARCHAR (255),
                    order_delivered_carrier_date VARCHAR (255),
                    order_delivered_customer_date VARCHAR (255),
                    order_estimated_delivery_date VARCHAR (255)
                )"""
    cursor.execute(query)
    query = """CREATE TABLE sales_fact (
                    id INT PRIMARY KEY,
                    product_id VARCHAR(255),
                    customer_id VARCHAR(255),
                    seller_id VARCHAR(255),
                    order_id VARCHAR (255) ,
                    time_id INT ,
                    revenue DECIMAL(10,2),
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (seller_id) REFERENCES seller(seller_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (time_id) REFERENCES timet(time_id)
                )"""
    cursor.execute(query)
    cursor.close()
    cnx.close()

def Queries():
    print("Press 1 to get total revenue generated from a specific customer")
    print("Press 2 to get the number of customers who bought more than 6 products")
    print("Press 3 to get the total number of customers and sellers registered on the platform")
    ch=input()
    cursor = cnx.cursor()
    if int(ch)==1:
        print("Enter customer id")
        id=input()
        id=(id)


        cursor.execute("SELECT sum(revenue) FROM sales_fact where customer_id='{}'".format(id))
        rows = cursor.fetchone()
        for row in rows:
            print('Total revenue generated by customer:',row)
    elif int(ch)==2:
        cursor.execute("SELECT COUNT(*) FROM sales_fact GROUP BY customer_id HAVING COUNT(product_id) > 6;")
        result = cursor.fetchone()
        print('Total number of Customers that bought more than 6 products are :',result[0])
    elif int(ch)==3:
        cursor.execute("SELECT COUNT(*) FROM customers;")
        customers = cursor.fetchone()
        print("Total number of customers: ", customers[0])

        cursor.execute("SELECT COUNT(*) FROM seller;")
        sellers = cursor.fetchone()
        print("Total number of sellers: ", sellers[0])

    # cursor.close()
    # cnx.close()

Queries()