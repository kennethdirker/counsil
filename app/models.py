import json
from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

assignees = sa.Table(
    'assignees',
    db.metadata,
    sa.Column('discussion_id', sa.Integer, sa.ForeignKey('discussion.id'), primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    npc: so.Mapped[bool] = so.mapped_column(server_default=sa.sql.false())
    avatar_image: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=True)

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    assigned_discussions = db.relationship('Discussion', secondary=assignees, back_populates='assigned_users')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        if self.avatar_image:
            return url_for('static', filename='avatar/' + self.avatar_image)
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except Exception:
            return
        return db.session.get(User, id)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def structured(self):
        try:
            return json.loads(self.about_me)
        except ValueError:
            return None


class Discussion(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    # SETUP, INITIALIZING, RUNNING, CONCLUDING
    state: so.Mapped[str] = so.mapped_column(sa.String(256), server_default='SETUP')

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="topic")

    assigned_users = db.relationship('User', secondary=assignees, back_populates='assigned_discussions')

    def last_post_id(self):
        query = sa.select(sa.func.max(Post.id)).where(Post.discussion_id == self.id)
        last_id = db.session.scalar(query)
        if last_id is None:
            last_id = 0
        return last_id

    def participants(self):
        query = sa.select(User).distinct().join(Post, User.id == Post.user_id).where(Post.discussion_id == self.id)
        return db.session.scalars(query).all()

    def is_assigned(self, user):
        return user in self.assigned_users

    def assign(self, user):
        if user.npc and not self.is_assigned(user):
            self.assigned_users.append(user)
            db.session.commit()

    def unassign(self, user):
        if self.is_assigned(user):
            self.assigned_users.remove(user)
            db.session.commit()

    def assigned_user_ids(self):
        return [user.id for user in self.assigned_users]

    def has_stalled(self):
        last_human_id = self.last_human_post_id()
        posts_since_query = (sa.select(sa.func.count(Post.id))
                             .where(Post.discussion_id == self.id)
                             .where(Post.id > last_human_id))
        posts_since_count = db.session.scalar(posts_since_query)
        return posts_since_count > current_app.config["DISCUSSION_STALL_AFTER_NPC_POST_LIMIT"]

    def last_human_post_id(self):
        query = sa.select(sa.func.max(Post.id)).where(Post.discussion_id == self.id).where(Post.is_npc == False)
        last_id = db.session.scalar(query)
        if last_id is None:
            last_id = 0
        return last_id

    def get_posts_since_last_contribution(self, user_id):
        last_post_id = db.session.scalar(sa.select(sa.func.max(Post.id))
                                         .where(Post.discussion_id == self.id)
                                         .where(Post.user_id == user_id)
                                         )
        if last_post_id is None:
            last_post_id = 0
        count_posts_since_query = (sa.select(sa.func.count(Post.id))
                             .where(Post.discussion_id == self.id)
                             .where(Post.id > last_post_id))
        amount = db.session.scalars(count_posts_since_query).all()[0]
        posts_since_query =(
            sa.select(Post).where(Post.discussion_id == self.id)
                           .order_by(Post.created_at)
        )
        return db.session.scalars(posts_since_query).all()[-amount:]
    
    
    def get_subject(self) -> str:
        """ Get the subject of the discussion, which is located in the first post. """
        query = sa.select(Post.body).where(Post.discussion_id == self.id).order_by(Post.created_at)
        return db.session.scalar(query)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    discussion_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Discussion.id), index=True)
    is_npc: so.Mapped[bool] = so.mapped_column(server_default=sa.sql.false())

    author: so.Mapped[User] = so.relationship(back_populates="posts")
    topic: so.Mapped[Discussion] = so.relationship(back_populates="posts")
