from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class Sentiment(FlaskForm):
    review = TextAreaField('review',
        validators=[DataRequired(),Length(min=2,max=1000)])

    submit = SubmitField('Predict')


