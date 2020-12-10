import cx_Oracle
from flask import Flask, request, session, render_template, redirect, url_for, flash
from hashlib import sha256
from datetime import datetime, date, time
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import os


try:
    conn = cx_Oracle.connect('super/abcd1234@//localhost:1521/orcl')
except Exception as err:
    print('Error while creating the connection ', err)


UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\img')
app = Flask(__name__)
app.secret_key = "secret_key"



def select_from_users(select):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM USERS"	
		cur.execute(sql_select)
		users = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return users

def select_from_users_where(select, where, *args):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM USERS WHERE {where}"
		data = tuple(args)
		cur.execute(sql_select, data)
		users = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return users

def select_all_from_product():
	try:
		cur = conn.cursor()
		sql_select = "SELECT * FROM PRODUCT"	
		cur.execute(sql_select)
		products = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return products

def select_product_from_products(product, *args):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT * FROM PRODUCT WHERE {product}"
		data = tuple(args)
		cur.execute(sql_select, data)
		product = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return product

def select_product_and_product_owner_name(where, *args):
	try:
		cur = conn.cursor()
		sql_select = f"select product.id, product.name, product.price, product.image_url, product.description, merchants.merchant_name, product.merchant_id from product INNER JOIN merchants ON product.merchant_id = merchants.id and  product.{where} "
		data = tuple(args)
		cur.execute(sql_select, data)
		products = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return products

def select_product_id_from_kart(user_id):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT PRODUCTID FROM KART WHERE USERID = {user_id}"
		print(sql_select)
		cur.execute(sql_select)
		ids = cur.fetchall()
	except Exception as err:
		print('Error selecting id from kart ', err)
	else:
		print('selected all products id from Kard.')
	finally:
		cur.close()
	return ids

def delete_product_from_kart(product_id, user_id):
	try:
		cur = conn.cursor()
		sql_select = f"DELETE FROM kart WHERE PRODUCTID = {product_id} AND USERID = {user_id}"
		cur.execute(sql_select)
	except Exception as err:
		print('Error when deleting product from kard ', err)
		conn.rollback()
	else:
		print('Deleted Kard.')
		conn.commit()
	finally:
		cur.close()
	

def insert_into_users(columns, *args):
	email, password, first_name, last_name = args
	values = ":1"
	for i in range(1, len(args)):
		values += ", :" + str(i+1)
	try:
		cur = conn.cursor()
		#sql_insert = f"INSERT INTO USERS(id, {columns}) VALUES(USERS_SEQ.nextval, {values})"
		#data = (email, , first_name, last_name)
		password = sha256(password.encode("UTF-8")).hexdigest()
		cur.callproc('sign_pkg.signUp', [first_name, last_name, email, password])
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		print('ERROR while inserting the data ', errorObj)
		err.append("Username already exists.")
		users = select_from_users('id, email, first_name, last_name')
		return render_template('register.html', users=users, errors=err)
	else:
		print('Insert Completed.')
		conn.commit()
	finally:
		cur.close()

def insert_into_product(merchant_id, product_name, product_price, product_image_url, product_description):
	err = []
	try:
		cur = conn.cursor()
		data = (product_name, merchant_id, product_price, product_image_url, product_description)
		cur.callproc('product_pkg.addProduct', data)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		err.append("ERROR: " + str(errorObj))
		print('ERROR while inserting the data ', errorObj)
	else:
		print('Insert Completed.')
		conn.commit()
	finally:
		cur.close()
	return err	
		
def insert_into_merchants(merchant_name, admin_id):
	try:
		cur = conn.cursor()
		sql_insert = f"insert into merchants values(merchId.nextval, '{merchant_name}', {admin_id}, sysdate)"
		print(sql_insert)
		cur.execute(sql_insert)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		print('ERROR while inserting the data ', errorObj)
		err.append("Merchant already exists.")
	else:
		print('Insert Completed.')
		conn.commit()
	finally:
		cur.close()

def select_adminId_from_merchants(user_id, *args):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT id FROM MERCHANTS WHERE {user_id}"
		data = tuple(args)
		cur.execute(sql_select, data)
		merchant_admin_id = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return merchant_admin_id

def select_merchantId_from_merchants(admin_id, *args):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT id FROM MERCHANTS WHERE {admin_id}"
		data = tuple(args)
		cur.execute(sql_select, data)
		merchant_id = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return merchant_id

@app.route('/register', methods=['POST', 'GET'])
def register():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		insert_into_users(
			"email, password, first_name, last_name",
			 email, password, first_name, last_name
		)
		return redirect('/login')
	else:
		users = select_from_users('id, email, first_name, last_name')
		return render_template('register.html', users=users)

@app.route('/product/delete/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
	if request.method == 'GET':
		product = select_product_from_products('id=:1',product_id)
		return render_template('product_delete.html', product=product)
	else:
		cur = conn.cursor()
		cur.callproc('kart_pkg.deleteProductInKart', [product_id])               # delete all products in kart
		answer = cur.callfunc('product_pkg.deleteProduct', str, [product_id])    # delete product from products
		print(answer)
		conn.commit()

		return redirect('/')

@app.route('/product/update/<int:product_id>', methods = ['POST', 'GET'])
def product_update(product_id):
	if request.method == 'POST':
		product_name = request.form['name']
		product_description = request.form['description']
		product_price = request.form['price']
		# product_image_url = request.form['image_url']
		if request.files['file'].filename != '':
			image = request.files['file']
			product_image_url = image.filename
			image.save(os.path.join(UPLOADS_PATH, secure_filename(image.filename)))


		cur = conn.cursor()
		answer = cur.callfunc('product_pkg.updateProduct', str, [product_id, product_name, product_price, product_image_url, product_description])
		if answer== 'Updated':
			conn.commit()
		return redirect('/product/'+str(product_id))
		
	else:
		product = select_product_from_products('id=:1' ,product_id)
		return render_template('product_update.html', product = product)

@app.route('/search', methods = [ 'GET'])
def search_product():
	if request.method =='GET':
		if 'email' in session:
			product_name = request.args.get('productSearch')
			cur = conn.cursor()
			answer = cur.callfunc('product_pkg.searchProduct',str, [product_name])
			products_ids = answer.split()
			products = []
			for product_id in products_ids:
				products.append(select_product_from_products('id=:1', (int)(product_id)))
			print(products)
			return render_template('search.html', products=products, searched_product=product_name)
				
				

@app.route('/')
def index():
	if request.method== 'GET':
		if 'email' in session:
			products = select_all_from_product()
			return render_template('home.html', user=session['email'], products=products)
		else: 
			return redirect('/login')

@app.route('/kart/delete/<int:product_id>', methods=['POST', 'GET'])
def delete_kart(product_id):
	if request.method == 'POST':
		user_id = select_from_users_where('id', 'email=:1',session['email'])[0][0]
		delete_product_from_kart(product_id, user_id)
		return redirect('/kart')


@app.route('/product/<int:product_id>', methods=['POST', 'GET'])
def product_detail(product_id):
	if request.method == 'GET':
		if not session['email']:
			return redirect('/login')
		else:
			#product = select_product_from_products('id=:1' ,product_id)
			
			user_id = select_from_users_where('id', 'email=:1',session['email'])
			merchant_id = select_merchantId_from_merchants('admin_id=:1', user_id[0][0])
			product = select_product_and_product_owner_name('id=:1' ,product_id)
			
			print(product[0][3])
			if merchant_id!=[]:
				merchant_id = merchant_id[0][0]
				merchant_id_of_product = product[0][6]
				print(merchant_id_of_product)
				print(merchant_id)
				if merchant_id_of_product == merchant_id:
					
					return render_template('product_detail.html', product = product, owner=1)
			return render_template('product_detail.html', product = product, owner=0)	
	if request.method == 'POST':
		user_id = select_from_users_where('id', 'email=:1',session['email'])[0][0]
		cur = conn.cursor()
		cur.callproc('kart_pkg.addKart', [user_id, product_id])
		conn.commit()

		return redirect('/')
	
		
@app.route('/kart')
def my_kart():
	if request.method == 'GET':
		if session['email'] :
			user_id = select_from_users_where('id', 'email=:1',session['email'])[0][0]
			products_id = select_product_id_from_kart(user_id)
			products_id = [item for t in products_id for item in t]
			products = []
			calculate_prices = 0
			for product_id in products_id:
				products.append(select_product_from_products('id=:1', product_id))
			print(products)
			if len(products_id)>0:
				cur = conn.cursor()

				calculate_prices = 	cur.callfunc('kart_price.calculatePrice', int, [user_id])
			
			return render_template('kart.html', products=products, calculate_prices = calculate_prices)
		
		else:
			return redirect('/login')



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/product/create', methods=['POST', 'GET'])
def create_product():
	if request.method == 'POST':
		if session['email'] :
			product_name = request.form['name']
			product_description = request.form['description']
			product_price = request.form['price']
			
			

			user_id = select_from_users_where('id', 'email=:1',session['email'])
			user_id = user_id[0][0]
			
			if request.files['file'].filename != '':
				image = request.files['file']
				
				
				product_image_url = image.filename
				image.save(os.path.join(UPLOADS_PATH, secure_filename(image.filename)))
			merchant_id = select_merchantId_from_merchants('admin_id=:1', user_id)
			

			print(merchant_id)
			if merchant_id ==[]:
				user_name = select_from_users_where('first_name', 'email=:1',session['email'])[0][0]
				print(user_name)
				insert_into_merchants(user_name, user_id)
			
			insert_into_product(merchant_id[0][0], product_name, product_price, product_image_url, product_description)

			return redirect('/')
		else:
			return redirect('/login')
	else:
		return render_template('create_product.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = sha256(request.form['password'].encode("UTF-8")).hexdigest()
		# users = select_from_users_where(
		# 	"id, email, first_name, last_name", 
		# 	"email=:1 AND password=:2", 
		# 	email, password
		# )
		cur = conn.cursor()
		answer = cur.callfunc("sign_pkg.signInByFunction", str, [email, password])
		print(answer)
		if answer=='Success':
			
			session['email'] = email
			session['password'] = password
			return redirect("/")
		else:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		# return redirect('/login')
	else:
		return render_template('login.html')


@app.route('/logout')
def logout():
	session['email'], session['password'] = None, None
	return redirect('/login')


if __name__=="__main__":
	app.run(debug=True)


conn.close()

