import random, time

from design_by_committee import db, app
import sqlalchemy as sa
from app.models import Discussion, User, Post
from npc import NPC

from backend.agent_client import AgentClient


def eagerness_to_contribute(member, discussion):
    """"""
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
    """ Select which discussion member will (re)consider their viewpoint. """
    # Step 1: Compute eagerness for each panel member
    eagerness_values = [eagerness_to_contribute(member, discussion) for member in members]

    # Step 2: Normalize eagerness values to create a probability distribution
    total_eagerness = sum(eagerness_values)
    probabilities = [eagerness / total_eagerness for eagerness in eagerness_values]

    # Step 3: Use the probability distribution to select a panel member
    chosen_member = random.choices(members, weights=probabilities, k=1)[0]
    return chosen_member


def contribute_to(discussion: Discussion, member: User, npc: NPC):
    """"""
    recent_posts = discussion.get_posts_since_last_contribution(user_id=member.id)
    recent_posts_bodies = [post.body for post in recent_posts]
    print("recent_posts: ", )
    with open("backend_loop.log", "a") as myfile:
        myfile.write(f"recent posts:\n{recent_posts_bodies}\n\n")
    s = npc.reconsider_viewpoint(recent_posts_bodies)
    return s


def progress(discussion: Discussion, room, client):
    """"""
    # Check if NPCs are waiting for the human user to talk
    if discussion.has_stalled():
        return
    print("progressing")
    member = roulette_wheel_selection(discussion.assigned_users, discussion)
    contribution = contribute_to(discussion, member, room[member.id])
    if contribution:
        post = Post(body=contribution, user_id=member.id, discussion_id=discussion.id, is_npc=True)
        db.session.add(post)
        db.session.commit()


def conclude(room: dict):
    """"""
    # Calculate the majority vote
    print("Voting...")
    accepted = [npc.vote() for npc in room.values()].count(True) > (len(room) / 2)
    print(f"Votes counted... Vote {'accepted' if accepted else 'rejected'}!")
    with open("backend_loop.log", "a") as myfile:
        myfile.write(f"Concluding:\nVote accepted? {accepted}\n\n")
    return accepted


def main():
    print("Initializing agent client")
    client = AgentClient()

    # Initialize chatroom dictionary to account for already existing chats
    print("Initializing chatrooms")
    rooms = {}
    STATE_OPTIONS = ["RUNNING", "CONCLUDING"]
    query = sa.select(Discussion)
    discussions = db.session.scalars(query).all()
    for discussion in discussions:
        if discussion.state in STATE_OPTIONS:
            rooms[discussion.id] = {member.id: NPC(member, discussion, client, verbose = True) for member in discussion.assigned_users}

    # Main loop
    print("Checking discussions...")
    while True:
        time.sleep(1)
        query = sa.select(Discussion)
        discussions = db.session.scalars(query).all()
        for discussion in discussions:
            print("Processing discussion ", discussion.id, discussion.state)
            if discussion.state == 'SETUP':
                # Discussion starting state has not finalized yet...
                continue
            if discussion.has_stalled():
                # Wait for human to post in discussion...
                continue
            if discussion.state == 'INITIALIZING':
                # Discussion starting state has been defined
                rooms[discussion.id] = {member.id: NPC(member, discussion, client, verbose = True) for member in discussion.assigned_users}
                discussion.state = 'RUNNING'
                db.session.commit()
            if discussion.state == 'RUNNING':
                # Discussion is fully running
                progress(discussion, rooms[discussion.id], client)
                # All points have been made: Vote and finalize
            if discussion.state == 'CONCLUDING':
                conclude(rooms[discussion.id])
                discussion.state = 'FINISHED'
                db.session.commit()


if __name__ == '__main__':
    with app.app_context():  # use Flasky stuff without running the frontend
        main()
