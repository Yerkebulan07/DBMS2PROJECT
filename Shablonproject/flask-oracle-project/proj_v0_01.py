import cx_Oracle
from flask import Flask, request, session, render_template, redirect, url_for
from hashlib import sha256

try:
    conn = cx_Oracle.connect('super/abcd1234@//localhost:1521/orcl')
except Exception as err:
    print('Error while creating the connection ', err)


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

def insert_into_users(columns, *args):
	email, password, first_name, last_name = args
	values = ":1"
	for i in range(1, len(args)):
		values += ", :" + str(i+1)
	try:
		cur = conn.cursor()
		sql_insert = f"INSERT INTO USERS(id, {columns}) VALUES(USERS_SEQ.nextval, {values})"
		data = (email, sha256(password.encode("UTF-8")).hexdigest(), first_name, last_name)
		cur.execute(sql_insert, data)
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



	
# @app.route('/')
# @app.route('/home')
# def index():
# 	err = []
# 	if session['email'] is not None and session['password'] is not None:
# 		email = session['email']
# 		password = session['password']
# 		users = select_from_users_where(
# 			"id, email, first_name, last_name", 
# 			"email=:1 AND password=:2", 
# 			email, password
# 		)
# 		if len(users) > 0:
# 			return render_template('home.html', users=users)
# 		else:
# 			err.append("Username OR password is incorrect.")
# 			return render_template('login.html', errors=err)
# 	else:
# 		return redirect('/login')
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
		return redirect(url_for('register'))
	else:
		users = select_from_users('id, email, first_name, last_name')
		return render_template('register.html', users=users)

@app.route('/')
def index():
	if session['email'] == None:
		return render_template('login.html')
	else:
		print(session['email'])
		return render_template('home.html', user=session['email'])

@app.route('/login', methods=['POST', 'GET'])
def login():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = sha256(request.form['password'].encode("UTF-8")).hexdigest()
		users = select_from_users_where(
			"id, email, first_name, last_name", 
			"email=:1 AND password=:2", 
			email, password
		)
		print(password +" until ) ")
		if len(users) > 0:
			print(users)
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

