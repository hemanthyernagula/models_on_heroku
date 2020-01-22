from flask import Flask,render_template

app = Flask(__name__)


l = ['hemanth','krishna','Shiva','Shashi']



@app.route('/')
def home():

    return "<h1> Hello Hemanth </h1>"


#127.0.0.1:5000/2
@app.route('/<int:num1>')
def krishna(num1):

    num = num1
    return "<h1> Hello Krishna {} </h1>".format(l[num])


@app.route('/names')
def name():

    return render_template('test2.html',names = l)  


if __name__=="__main__":
    app.run()