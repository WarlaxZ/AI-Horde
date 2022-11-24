import datetime
import uuid

from horde.flask import db
# from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    # TODO CLEAN THIS UP, BUNCH OF DUPLICATES
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4)  # Whilst using sqlite use this, as it has no uuid type
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Then move to this
    username = db.Column(db.String(50), unique=True, nullable=False)
    oauth_id = db.Column(db.String(50), unique=True, nullable=False)
    api_key = db.Column(db.String(50), unique=True, nullable=False)
    kudos = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


    suspicious = db.Column(db.Boolean, default=False)
    worker_invited = db.Column(db.Boolean, default=False)
    moderator = db.Column(db.Boolean, default=False)
    concurrency = db.Column(db.Integer, default=30)
    usage_multiplier = db.Column(db.Float, default=1.0)
    kudos = db.Column(db.Integer, default=0)
    same_ip_worker_threshold = db.Column(db.Integer, default=3)
    public_workers = db.Column(db.Boolean, default=False)
    trusted = db.Column(db.Boolean, default=False)
    evaluating_kudos = db.Column(db.Integer, default=0)
    kudos_details = db.Column(db.JSON, default={
        "accumulated": 0,
        "gifted": 0,
        "admin": 0,
        "received": 0,
        "recurring": 0,
    })
    monthly_kudos = db.Column(db.JSON, default={
        "amount": 0,
        "last_received": None,
    })
    suspicions = db.Column(db.JSON, default=[])
    contact = db.Column(db.String(50), default=None)
    min_kudos = db.Column(db.Integer, default=0)
    username = db.Column(db.String(50), default="Anonymous")
    oauth_id = db.Column(db.String(50), default="anon")
    api_key = db.Column(db.String(50), default="0000000000")
    invite_id = db.Column(db.String(50), default="")
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    public_workers = db.Column(db.Boolean, default=True)
    contributions = db.Column(db.JSON, default={
        thing_name: 0,
        "fulfillments": 0,
    })
    usage = db.Column(db.JSON, default={
        thing_name: 0,
        "requests": 0,
    })
    # We allow anonymous users more leeway for the max amount of concurrent requests
    # This is balanced by their lower priority
    concurrency = db.Column(db.Integer, default=500)

    # actually use this:
    ret_dict = {
        "username": self.username,
        "oauth_id": self.oauth_id,
        "api_key": self.api_key,
        "kudos": self.kudos,
        "kudos_details": self.kudos_details.copy(),
        "id": self.id,
        "invite_id": self.invite_id,
        "contributions": self.contributions.copy(),
        "usage": self.usage.copy(),
        "usage_multiplier": self.usage_multiplier,
        "concurrency": self.concurrency,
        "worker_invited": self.worker_invited,
        "moderator": self.moderator,
        "suspicions": self.suspicions,
        "public_workers": self.public_workers,
        "trusted": self.trusted,
        "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        "last_active": self.last_active.strftime("%Y-%m-%d %H:%M:%S"),
        "monthly_kudos": serialized_monthly_kudos,
        "evaluating_kudos": self.evaluating_kudos,
        "contact": self.contact,
    }





class PromptRequest(db.Model):
    """For storing prompts in the DB"""
    __tablename__ = "prompt"
    id = db.Column(db.String(50), primary_key=True, default=uuid.uuid4) # Whilst using sqlite use this, as it has no uuid type
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Then move to this
    prompt = db.Column(db.Text, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User", backref=db.backref("prompt", lazy="dynamic"))

    tricked_workers = db.Column(db.JSON, default=[], nullable=False)
    params = db.Column(db.JSON, default={}, nullable=False)
    total_usage = db.Column(db.Integer, default=0, nullable=False)
    nsfw = db.Column(db.Boolean, default=False, nullable=False)
    ipaddr = db.Column(db.String(39))  # ipv6
    safe_ip = db.Column(db.Boolean, default=False, nullable=False)
    trusted_workers = db.Column(db.Boolean, default=False, nullable=False)

    # A lot of these look like they don't belong to prompt and should be moved
    processing_gens = db.Column(db.JSON, default=[], nullable=False)
    fake_gens = db.Column(db.JSON, default=[], nullable=False)
    last_process_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    workers = db.Column(db.JSON, default=[], nullable=False)
    faulted = db.Column(db.Boolean, default=False, nullable=False)
    consumed_kudos = db.Column(db.Integer, default=0, nullable=False)

    ttl = db.Column(db.Integer, default=1200, nullable=False)

    created = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    updated = db.Column(
        db.DateTime(timezone=False), nullable=True, onupdate=datetime.datetime.utcnow
    )

    def set_job_ttl(self):
        raise NotImplementedError("This is not implemented yet")
