import sqlalchemy as sa
import sqlalchemy.orm as so
from myapp import db

#consult_name, date, comment, rating, phone_number
class Feedbacks(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    consult_name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    date_feed: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    comment: so.Mapped[str] = so.mapped_column(sa.String(1000))
    rating: so.Mapped[int] = so.mapped_column()
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(30))
    send: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

#id, full_name, worker_post, rating, contacts
class Workers(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    worker_post: so.Mapped[str] = so.mapped_column(sa.String(64))
    rating: so.Mapped[float] = so.mapped_column(sa.Float())
    contacts: so.Mapped[str] = so.mapped_column(sa.String(128))