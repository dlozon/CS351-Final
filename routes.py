from inspect import signature
from flask import Flask, render_template, redirect, url_for, request, flash
import boto3
from botocore.config import Config
import bcrypt

client = boto3.client('dynamodb')
app = Flask(__name__)

my_config = Config(region_name='us-east-1',
					signature_version='v4',
					retries={'max_attempts': 10, 'mode': 'standard'})
client = boto3.client('dynamodb', config=my_config)

@app.route('/')
def default():
	return redirect(url_for('chatroom'))
	
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
	# if request.method == 'POST':
	return render_template('chatroom.html', page_name='chatroom')
	
@app.route('/chatroom/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html', page_name='login')
	else:
		username = request.form['username']
		password = request.form['password']
		saltyTears = bcrypt.gensalt()
		pwo= bcrypt.hashpw(request.form['password'].encode('utf-8'), saltyTears)
		response = client.get_item(
			TableName='users',
			Key={
				'username': {
					'S': username
				}
			}
		)
		if 'Item' in response:
			if bcrypt.checkpw(password.encode('utf-8'), response['Item']['password']['B']):
				return redirect(url_for('chatroom'))
			else:
				flash('Incorrect password')
		else:
			flash('User not found')
		return render_template('login.html', page_name='login', username=username, password=password)

@app.route('/chatroom/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html', page_name='signup')
	else:
		username = request.form['username']
		# password = request.form['password']
		saltyTears = bcrypt.gensalt()
		pwo = bcrypt.hashpw(request.form['password'].encode('utf-8'), saltyTears)
		response = client.get_item(
			TableName='users',
			Key={
				'username': {
					'S': username
				}
			}
		)
		if 'Item' in response:
			flash('User already exists')
		else:
			response = client.put_item(
				TableName='users',
				Item={
					'username': {
						'S': username
					},
					'password': {
						'B': pwo
					},
					'tears': {
						'B': saltyTears
					}
				}
			)
			return redirect(url_for('login'))
		return render_template('signup.html', page_name='signup', username=username, password=pwo)

# @app.route('/chatroom/signup/success')
# def signup_success():
# 	return render_template('signup_success.html', page_name='signup success')

@app.route('/whatever/<name>')
def say_hello(name):
	return render_template('hello.html', name=name)
	
if __name__ == "__main__":
	app.run(debug=True)
