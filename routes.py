from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def default():
	return redirect(url_for('chatroom'))
	
@app.route('/chatroom')
def chatroom():
	# TODO check cookie user logged in
	return render_template('chatroom.html', page_name='chatroom')
	
@app.route('/chatroom/login', methods=['GET', 'POST'])
def login():
	if request.method == "GET":
		return render_template('login.html', page_name='login')
	else:
		username = request.form['username']
		password = request.form['password']
		# TODO query for user in database
		# if user not found: return error message 'User not found' (possibly error page that automatically redirects)
		# if password doesn't match: error message 'Incorrect Password'
		# if user found and password matches: render chatroom, logged in (create cookie)
		return 'Username: %s\nPassword: %s' % (username, password)
	
@app.route('/chatroom/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "GET":
		return render_template('signup.html', page_name='signup')
	else:
		username = request.form['username']
		password = request.form['password']
		# TODO query for username in database
		# if user exists: error message 'User already exists'
		# if user not found: create new database user, success message with redirect to chatroom logged in
		return 'Username: %s\nPassword: %s' % (username, password)


# @app.route('/chatroom/signup/success')
# def signup_success():
# 	return render_template('signup_success.html', page_name='signup success')

@app.route('/whatever/<name>')
def say_hello(name):
	return render_template('hello.html', name=name)
	
if __name__ == "__main__":
	app.run(debug=True)
