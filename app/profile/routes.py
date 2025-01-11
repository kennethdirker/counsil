from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.profile.forms import EditProfileForm, EmptyForm
from app.models import User
from app.profile import bp


@bp.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template(
        "profile/user.html",
        user=user,
        member=user.structured(),
        form=form
    )


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_("Your changes have been saved."))
        return redirect(url_for("profile.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("profile/edit_profile.html", title=_("Edit Profile"), form=form)