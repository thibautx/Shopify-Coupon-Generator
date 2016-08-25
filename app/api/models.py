import uuid
from app import db
from datetime import datetime, timedelta


class Discount(db.Model):

    # required
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float, nullable=False)
    discount_type = db.Column(db.String(20))

    # not required
    prefix = db.Column(db.String)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    minimum_order_amount = db.Column(db.Float)
    usage_limit = db.Column(db.Integer)
    # applies_to_id = db.Column(db.Integer, nullable=True)
    # applies_once = db.Column(db.Boolean, default=False)
    # applies_to_resource = db.Column()
    times_used = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Discount, self).__init__(**kwargs)
        self._generate_code()
        # set defaults
        if self.starts_at is None:
            self.starts_at = datetime.now()
        if self.ends_at is None:
            self.ends_at = datetime.now() + timedelta(days=7)
        if self.status is None:
            self.status = 1
        if self.minimum_order_amount is None:
            self.minimum_order_amount = 10.00
        if self.usage_limit is None:
            self.usage_limit = 10
        if self.times_used is None:
            self.times_used = 0

    def _generate_code(self):
        self.code = str(uuid.uuid4())
        if self.prefix:
            self.code = self.prefix + '-' + self.code[len(self.prefix)+1:]


    def to_dict(self):
        d = self.__dict__.copy()
        del(d['_sa_instance_state'])
        d['starts_at'] = d['starts_at'].strftime("%Y-%m-%d")
        d['ends_at'] = d['ends_at'].strftime("%Y-%m-%d")
        return d
