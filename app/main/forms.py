from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as _l
from app import db
from app.models import User


class NewDiscussionForm(FlaskForm):
    title = StringField(_l("Topic"), validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Create")


class NewPostForm(FlaskForm):
    body = TextAreaField(_("Your contribution"), validators=[DataRequired()])
    submit = SubmitField("Post")

    def __init__(self, discussion_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.htmx = f'/discussions/{discussion_id}/new'
