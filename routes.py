from flask import Flask, make_response, render_template, redirect, url_for, request
import boto3
from botocore.config import Config
import bcrypt

# client = boto3.client('dynamodb')
app = Flask(__name__)

# config for dynamodb
my_config = Config(region_name='us-east-1',
					signature_version='v4',
					retries={'max_attempts': 10, 'mode': 'standard'})
client = boto3.client('dynamodb', config=my_config)

# default route
@app.route('/')
def default():
	return redirect(url_for('chatroom'))
	
# route for chatroom page	
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
	if request.cookies.get('logged_in_temp') or request.cookies.get('logged_in_perm'):
		# if user is logged in, render chatroom page
		if request.method == 'GET':
			# Read messages from database
			# Write messages to client
			response = client.scan(TableName='chatroom')
			if response['Items']:
				return render_template('chatroom.html', messages=response['Items'])
		else:
			# if user is logged in and sending a message, put message in db
			username = request.form['username']
			message = request.form['message']
			# time = 
			response = client.put_item(
				TableName='chatroom',
				Item={
					# 'time_sent': {'N': time},
					'username': {'S': username},
					'message': {'S': message}
				}
			)
			return render_template('chatroom.html', page_name='chatroom')
	else:
		# if user in not logged in, do not allow them to send messages
		return render_template('chatroom.html', page_name='chatroom')
	return render_template('chatroom.html', page_name='chatroom')

# route for login page	
@app.route('/chatroom/login', methods=['GET', 'POST'])
def login():
	# if user is already logged in, redirect to chatroom
	if request.cookies.get('logged_in_temp') or request.cookies.get('logged_in_perm'):
		return redirect(url_for('chatroom'))
	# if user is not logged in, show login page
	if request.method == 'GET':
		return render_template('login.html', page_name='login')
	else:
		# get user name from form
		username = request.form['username']

		# password = request.form['password']
		# saltyTears = bcrypt.gensalt()
		# pwo = bcrypt.hashpw(request.form['password'].encode('utf-8'), saltyTears)

		# get usernames from dynamodb
		response = client.get_item(
			TableName='users',
			Key={
				'username': {'S': username}
			}
		)
		# if username exists, check password
		if 'Item' in response:
			# if password is correct, redirect to chatroom
			if bcrypt.checkpw(request.form['password'].encode('utf-8'), response['Item']['password']['B']):
				# if remember me is checked, set session to expire in 30 days
				remember = request.form.get('remember')
				if remember:
					# if remember me is checked, cookie will not expire, but will in 30 days (cookies have to expire per specification)
					resp = make_response(redirect(url_for('chatroom')))
					resp.set_cookie('logged_in_perm', bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt()), secure=True, httponly=True, max_age=2592000)
					return resp
				else:
					# if remember me is not checked, cookie expires when browser is closed
					resp = make_response(redirect(url_for('chatroom')))
					resp.set_cookie('logged_in_temp', bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt()), secure=True, httponly=True)
					return resp
			else:
				# if password is incorrect, redirect to login
				return render_template('login.html', page_name='login', error='Incorrect password')
		else:
			# if username doesn't exist, redirect to signup
			return render_template('signup.html', page_name='signup', error='User does not exist')
	return render_template('login.html', page_name='login')

# route for signup page
@app.route('/chatroom/signup', methods=['GET', 'POST'])
def signup():
	# if user is already logged in, redirect to chatroom
	if request.cookies.get('logged_in_temp') or request.cookies.get('logged_in_perm'):
		return redirect(url_for('chatroom'))
	# if user is not logged in, show signup page
	if request.method == 'GET':
		return render_template('signup.html', page_name='signup')
	else:
		# get user name from form
		username = request.form['username']

		# password = request.form['password']

		# generate salt(hash)
		saltyTears = bcrypt.gensalt()
		# hash password
		pwo = bcrypt.hashpw(request.form['password'].encode('utf-8'), saltyTears)
		# check if username already exists
		response = client.get_item(
			TableName='users',
			Key={
				'username': {'S': username}
			}
		)
		# if username exists, redirect to signup
		if 'Item' in response:
			return render_template('signup.html', page_name='signup', error='Username already taken')
		else:
			# if username doesn't exist, add to dynamodb
			response = client.put_item(
				TableName='users',
				Item={
					'username': {'S': username},
					'password': {'B': pwo},
					'tears': {'B': saltyTears}
				}
			)
			return redirect(url_for('login'))
	return render_template('signup.html', page_name='signup')

# @app.route('/chatroom/signup/success')
# def signup_success():
# 	return render_template('signup_success.html', page_name='signup success')

@app.route('/whatever/<name>')
def say_hello(name):
	return render_template('hello.html', name=name)
	
if __name__ == "__main__":
	app.run(debug=True)
