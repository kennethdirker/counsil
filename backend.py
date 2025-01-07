from design_by_committee import db, app
import sqlalchemy as sa
from app.models import Discussion


def example():
    # We need the app_context() to query the database
    with app.app_context():
        query = sa.select(Discussion)
        discussions = db.session.scalars(query).all()
    for d in discussions:
        print(d.title)


if __name__ == '__main__':
    example()