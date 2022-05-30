from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def default():
	return redirect(url_for('chatroom'))
	
@app.route('/chatroom')
def chatroom():
	return render_template('chatroom.html', page_name='chatroom')
	
@app.route('/chatroom/login')
def login():
	return render_template('login.html', page_name='login')
	
@app.route('/chatroom/signup')
def signup():
	return render_template('signup.html', page_name='signup')

# @app.route('/chatroom/signup/success')
# def signup_success():
# 	return render_template('signup_success.html', page_name='signup success')

@app.route('/whatever/<name>')
def say_hello(name):
	return render_template('hello.html', name=name)
	
if __name__ == "__main__":
	app.run(debug=True)
