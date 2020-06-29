from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, NumberRange

# class ShowForm(Form):
#     artist_id = StringField(
#         'artist_id',
#         validators=[DataRequired()],
#     )
#     venue_id = StringField(
#         'venue_id',
#         validators=[DataRequired()],
#     )
#     start_time = DateTimeField(
#         'start_time',
#         validators=[DataRequired()],
#         default=datetime.today()
#     )

class MovieForm(Form):
    title = StringField(
        'title',
        validators=[DataRequired()]
    )
    release = DateTimeField(
        'release',
        validators=[DataRequired()],
        default=datetime.today()
    )
    image_link = StringField(
        'image_link'
    )
    # phone = StringField(
    #     'phone',
    #     validators=[Regexp(r'^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$', message='Not a Phone Number')]
    # )
    # website = StringField(
    #     'website'
    # )
    # facebook_link = StringField(
    #     'facebook_link', 
    #     validators=[Regexp(r'(^https?:\/\/)?(www.)??facebook.com\/[a-zA-z]*', message='Not a Facebook Link')]
    # )

class ActorForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    age = IntegerField(
        'age',
        validators=[DataRequired(), NumberRange(min=0, max=110, message='Invalid age')]
    )
    gender = SelectField(
        'gender',
        validators=[DataRequired()],
        choices=[
            ('F','Female'),
            ('M','Male'),
            ('TF','Trans-Female'),
            ('TM','Trans-Male'),
            ('NB','Non-Binary')
        ]
    )
    image_link = StringField(
        'image_link'
    )
    # website = StringField(
    #     'website'
    # )
    # facebook_link = StringField(
    #     # TODO implement enum restriction
    #     'facebook_link',
    #     validators=[Regexp(r'(^https?:\/\/)?(www.)??facebook.com\/[a-zA-z]*', message='Not a Facebook Link')]
    # )

