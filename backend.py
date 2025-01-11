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


if __name__ == '__main__':
    # example()
    with app.app_context():
        user = db.first_or_404(sa.select(User).where(User.id == 3))
        print(user.structured())