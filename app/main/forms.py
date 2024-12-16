from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as _l
from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    about_me = TextAreaField(_l("About me"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l("Submit"))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(
                sa.select(User).where(User.username == username.data)
            )
            if user is not None:
                raise ValidationError(_("Please use a different username."))


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")


class NewDiscussionForm(FlaskForm):
    title = StringField(_l("Topic"), validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("Create")


class NewPostForm(FlaskForm):
    body = TextAreaField(_("Your contribution"), validators=[DataRequired()])
    submit = SubmitField("Post")

    def __init__(self, discussion_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.htmx = f'/discussions/{discussion_id}/new'
