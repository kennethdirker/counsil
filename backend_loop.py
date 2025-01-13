import time
import random

from design_by_committee import db, app
import sqlalchemy as sa
from app.models import Discussion, User, Post


def contribute_to(discussion: Discussion, member: User):
    recent_posts = discussion.get_posts_since_last_contribution(user_id=member.id)
    return "placeholder"


def eagerness_to_contribute(member, discussion):
    last_post_id = db.session.scalar(
        sa.select(sa.func.max(Post.id))
        .where(Post.discussion_id == discussion.id)
        .where(Post.user_id == member.id)
    )
    if last_post_id is None:
        last_post_id = 0
    posts_since_count = db.session.scalar(
        sa.select(sa.func.count(Post.id))
        .where(Post.discussion_id == discussion.id)
        .where(Post.id > last_post_id)
    )
    return (posts_since_count * 10) + 1


def roulette_wheel_selection(members, discussion):
    # Step 1: Compute eagerness for each panel member
    eagerness_values = [eagerness_to_contribute(member, discussion) for member in members]

    # Step 2: Normalize eagerness values to create a probability distribution
    total_eagerness = sum(eagerness_values)
    probabilities = [eagerness / total_eagerness for eagerness in eagerness_values]

    # Step 3: Use the probability distribution to select a panel member
    chosen_member = random.choices(members, weights=probabilities, k=1)[0]

    return chosen_member


def progress(discussion: Discussion):
    if discussion.has_stalled():
        return

    member = roulette_wheel_selection(discussion.assigned_users, discussion)
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
