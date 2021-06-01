
from app import db


class OrderList(db.Model):
    __tablename__ = 'orderlist'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(80))
    def __repr__(self):
        return '<Product %r>' % self.name
 
 