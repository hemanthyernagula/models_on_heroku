from flask import  Flask,render_template,request,flash
from forms import  Sentiment
from mtp import test_your_data
app = Flask(__name__)
app.config['SECRET_KEY'] = '15d7d1s4'


models = [
    {'title':'Sentiment Analysis',
     'description': 'Data is having positive and negative reviews \
                    data is cleaned and featurized with NLP techniques\
                    like Bag Of Words, TFIDF and a binary classifier \
                    like Logistic Regression is applied on it to \
                    predict the class of the review (Positive or Negative)',
     'image':'sentiment.png'

    }
]

@app.route('/',methods=['POST','GET'])
def home():
    return render_template('home.html',models = models,title='My Projects')

@app.route('/sentiment',methods=['GET','POST'])
def sentiment():
    form = Sentiment()
    if form.validate_on_submit():
        review = form.review.data
        label  = test_your_data(review)
        if label == 1:
            label = ['Positive','success']
        elif label == 0:
            label = ['Negative','warning']
        
        return render_template('sentiment.html',title="sentiment analysis",review=review,label=label,form=form)    
    
    return render_template('sentiment.html',title="sentiment analysis",form=form)


if __name__ == "__main__":
    app.run()
