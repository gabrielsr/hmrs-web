from flask.cli import AppGroup

from .webapp import db
from .models import Profile
from .auth.principal import Principal
from .auth.credential import PasswordCredential

from .seed import profiles, credentials, principals

seed_cli = AppGroup("seed")


@seed_cli.command("users")
def seed_users():
    "Add seed data to the database."
    for p in principals:
        db.session.add(Principal(**p))
    for m in profiles:
        db.session.add(Profile(**m))
    for c in credentials:
        db.session.add(PasswordCredential(**c))

    db.session.commit()

