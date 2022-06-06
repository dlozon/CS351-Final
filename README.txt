This needs some things setup in order for this to function, and I'm not
particularly sure how the libraries in the virtual environment will work

Python Libaries Needed
-boto3
-flask
-bcrypt

So basic structure:
-python with flask libraries
-script files, routes.py has the http routes to render the pages
-in the html, using templates for flask to allow a base.html template
-base.html template has bootstrap in it (comes with a lot of built in styling)

Assuming that you are on a windows computer with python3 installed...

- cd into TSpace
- activate the virtual environment --> venv\Scripts\activate (gotta use backslash)
- set the windows environment variable for the flask app file --> setx FLASK_APP "routes.py"

try running the application at this point --> py routes.py

If the server starts up and is accessable, yay!
