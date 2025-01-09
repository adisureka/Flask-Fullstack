import sqlite3
import csv

def create_table_user(cursor):
	query = """
	CREATE TABLE IF NOT EXISTS users(
		uid INTEGER PRIMARY KEY AUTOINCREMENT,
		user_name TEXT UNIQUE,
		password TEXT NOT NULL)
	"""
	cursor.execute(query)

def create_table_product(cursor):
	query = """
	CREATE TABLE IF NOT EXISTS products(
		pid INTEGER PRIMARY KEY AUTOINCREMENT,
		product_name TEXT NOT NULL,
		description TEXT,
		price REAL NOT NULL
		)
	"""
	cursor.execute(query)

def create_cursor():
	conn = sqlite3.connect("./Resources/database.db")
	cursor = conn.cursor()
	return conn, cursor

def load_data(cursor, conn, path):
	data = []
	with open(path) as file:
		file.readline()
		file.readline()
		file.readline()
		csvreader = csv.reader(file)
		for row in csvreader:
			name,_,description,*x,price,_,_,_,_,_,_ = row
			if price.replace(".","").isdigit():
				data.append([name, description, float(price)])
		# print(len(row))
		# print(name, description, price)
	#cursor.executemany("INSERT INTO products (product_name, description, price) VALUES (?,?,?)",
		               #data)
	#print(len(data)) 114
	print("load_data successfully")
	print(data[0])
	count = 0
	# for row in data:
	# 	print(count)
	# 	cursor.execute(f"INSERT INTO products(product_name,description, price) VALUES({row[0]},{row[1]},{row[2]})")
	row = data[0]
	# note to have "" surround your "{}" for sql input
	#cursor.execute(f'INSERT INTO products(product_name, description,price) VALUES ("{row[0]}","aproduct",10)')
	cursor.executemany("INSERT INTO products(product_name, description,price) VALUES (?,?,?)", data)
	conn.commit() # with out commit file will never insert into it

def get_data(table_name):
	_,cursor = create_cursor()
	data = []

	query = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
	for entry in query:
		data.append(entry)
	return data

def update_data(*data):
	conn,cursor = create_cursor()
	query = f"""INSERT INTO USERS (user_name, password) VALUES ('{data[0]}','{data[1]}')"""
	try:
		cursor.execute(query)
	except sqlite3.IntegrityError as e:
		print(str(e))
		return False
	conn.commit()
	return True
def main():
	conn, cursor = create_cursor()
	# create_table_user(cursor)
	# create_table_product(cursor)
	# load_data(cursor, conn, "./Resources/AVM 2024-04-15 AVM Wholesale Price Sheet.csv")
	#print(get_data("products"))
	print(update_data("Ali", "aaaa"))
	print(get_data("users"))

if __name__ == "__main__":
	main()