from design_by_committee import db, app
import sqlalchemy as sa
from app.models import Discussion, User, Post


def example():
    # We need the app_context() to query the database
    with app.app_context():
        query = sa.select(Discussion)
        discussions = db.session.scalars(query).all()
    for d in discussions:
        print(d.title)


def contribute_to(dis):
    return "placeholder"


if __name__ == '__main__':
    # example()
    while True:
        with app.app_context():
            query = sa.select(Discussion)
            discussions = db.session.scalars(query).all()
            for discussion in discussions:
                if discussion.state != 'RUNNING':
                    continue
                if discussion.has_stalled():
                    continue
                for member in discussion.assigned_users:
                    if discussion.has_stalled():
                        break
                    recent_posts = discussion.get_posts_since_last_contribution(user_id=member.id, discussion_id=discussion.id)
                    contribution = contribute_to(discussion)
                    post = Post(body=contribution, user_id=member.id, discussion_id=discussion.id, is_npc=True)
                    db.session.add(post)
                    db.session.commit()
