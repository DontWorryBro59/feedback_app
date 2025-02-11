from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from myapp import db



# consult_name, date, comment, rating, phone_number
class Feedbacks(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    consult_name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    date_feed: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    comment: so.Mapped[str] = so.mapped_column(sa.String(1000))
    rate: so.Mapped[int] = so.mapped_column()
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(30))
    send: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)


# id, full_name, worker_post, rating, contacts
class Workers(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    worker_post: so.Mapped[str] = so.mapped_column(sa.String(64))
    contacts: so.Mapped[str] = so.mapped_column(sa.String(128))
    rating: so.Mapped[float] = so.mapped_column(nullable=False, default=0)


class Admins(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
