from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
import sqlalchemy as sa
from app import db
from app.main.forms import NewDiscussionForm, NewPostForm
from app.models import User, Discussion, Post
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return render_template(
        "index.html",
        title=_("Home")
    )


@bp.route("/discussions", methods=["GET", "POST"])
@login_required
def discussions_index():
    form = NewDiscussionForm()
    if form.validate_on_submit():
        discussion = Discussion(title=form.title.data)
        db.session.add(discussion)
        db.session.commit()
        flash(_("New discussion started!"))
        return redirect(url_for("main.discussions_index"))
    query = sa.select(Discussion)
    discussions = db.session.scalars(query).all()
    return render_template("discussions/index.html", title=_("Discussions"), discussions=discussions, form=form)


@bp.route("/discussions/<id>")
@login_required
def discussions_view(id):
    discussion = db.first_or_404(sa.select(Discussion).where(Discussion.id == id))
    form = NewPostForm(discussion_id=discussion.id)
    query = sa.select(Post).where(Post.discussion_id == discussion.id).order_by(Post.id.desc())
    posts = db.session.scalars(query).all()
    return render_template("discussions/view.html", title=discussion.title, discussion=discussion, form=form,
                           posts=posts, last_post_id=discussion.last_post_id())


@bp.route("/discussions/<id>/posts/<last_post_id>")
@login_required
def discussions_view_posts(id, last_post_id):
    discussion = db.first_or_404(sa.select(Discussion).where(Discussion.id == id))
    query = (
        sa.select(Post)
        .where(Post.discussion_id == discussion.id)
        .where(Post.id > last_post_id)
        .order_by(Post.id.desc())
    )
    posts = db.session.scalars(query).all()
    return render_template("discussions/posts.html", discussion=discussion, posts=posts)


@bp.route("/discussions/<id>/new", methods=["POST"])
@login_required
def discussions_view_post(id):
    discussion = db.first_or_404(sa.select(Discussion).where(Discussion.id == id))
    form = NewPostForm(discussion_id=discussion.id)
    if form.validate_on_submit():
        post = Post(body=form.body.data, user_id=current_user.id, discussion_id=discussion.id)
        db.session.add(post)
        db.session.commit()
        form.body.data = ''
        return render_template("discussions/new.html", form=form)
