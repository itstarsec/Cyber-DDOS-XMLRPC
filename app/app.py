from flask import Flask, redirect, url_for, request, render_template
import xmlrpc
app = Flask(__name__)

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html', e=error), 500
#	return "Wrong favicon link, please try again!"
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/ddos', methods = ['POST'])
def login():
	if request.method == 'POST':
		user = request.form['url']
		hash_int = xmlrpc.main(user)
		return render_template('result.html', data=hash_int)
#		return "ddos %s success! " % hash_int
#		return redirect(url_for('result',url = hash_int))

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 1234)
