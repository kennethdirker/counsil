import time

from design_by_committee import db, app
import sqlalchemy as sa
from app.models import Discussion, User, Post


def contribute_to(discussion: Discussion, member: User):
    recent_posts = discussion.get_posts_since_last_contribution(user_id=member.id,
                                                                discussion_id=discussion.id)
    return "placeholder"


def progress(discussion: Discussion):
    for member in discussion.assigned_users:
        time.sleep(1)
        if discussion.has_stalled():
            break

        contribution = contribute_to(discussion, member)
        if contribution:
            post = Post(body=contribution, user_id=member.id, discussion_id=discussion.id, is_npc=True)
            db.session.add(post)
            db.session.commit()


def conclude(discussion: Discussion):
    pass


def main():
    while True:
        query = sa.select(Discussion)
        discussions = db.session.scalars(query).all()
        for discussion in discussions:
            if discussion.state == 'SETUP':
                continue
            if discussion.has_stalled():
                continue
            if discussion.state == 'RUNNING':
                progress(discussion)
            if discussion.state == 'CONCLUDING':
                conclude(discussion)


if __name__ == '__main__':
    with app.app_context():  # use Flasky stuff without running the frontend
        main()
