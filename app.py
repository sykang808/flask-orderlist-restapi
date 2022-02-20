import os
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_restx import Resource
from flask import request # change
from orderlist import *   
from json import dumps 
from flask_cors import CORS, cross_origin
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'*': {'origins': '*'}})
xray_recorder.configure(service='flask-orderlist-restapi')
XRayMiddleware(app, xray_recorder)

config.get_secret()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER' , config.DATABASE_CONFIG['DB_USER'] ),
    os.getenv('DB_PASSWORD', config.DATABASE_CONFIG['DB_PASSWORD']),
    os.getenv('DB_HOST', config.DATABASE_CONFIG['DB_HOST']),
    os.getenv('DB_NAME', config.DATABASE_CONFIG['DB_NAME'])
)

db = SQLAlchemy(app)

@api.route('/orderlists')
class OrderListIndex(Resource):
    def get(self):
        ret = []
        res = db.session.query(OrderList).all()
        for orderlist in res:
            ret.append(
                {
                    'id': orderlist.id,
                    'customer_id': orderlist.customer_id,
                    'product_id': orderlist.product_id,
                    'count': orderlist.count,
                    'status': orderlist.status
                }
            )
        return ret, 200


@api.route('/ordercount')
class OrderListIndex(Resource):
    def get(self):
        ret = []
        #res = db.session.query(OrderList).from_statement("SELECT status, count(status) FROM orderlist group by status")
        sql = "SELECT status, count(status) as count FROM orderlist group by status"
        res = db.engine.execute(sql)
        for orderlist in res:
            ret.append(
                {
                    'status': orderlist.status,
                    'count': orderlist.count,
                }
            )
        return ret, 200


@api.route('/orderlist')
@api.response(404, "Could not put orderlist")
class OrderListPost(Resource):
    def post(self):
        data = request.get_json(force=True)
        orderlist = OrderList(
            customer_id = data['customer_id'],
            product_id = data['product_id'],
            count = data['count'],
            status = data['status']
        )
        db.session.add(orderlist)
        db.session.commit()
        return {
                'id': orderlist.id,
                'customer_id': orderlist.customer_id,
                'product_id': orderlist.product_id,
                'count': orderlist.count,
                'status': orderlist.status
            }, 200


@api.route('/orderlist/<int:id>')
@api.response(404, "Could not find orderlist")
@api.param('id', 'The task identifier')
class OrderListItem(Resource):
    def get(self, id):
        orderlist = db.session.query(OrderList).get(id)
        return  {
                    'id': orderlist.id,
                    'customer_id': orderlist.customer_id,
                    'product_id': orderlist.product_id,
                    'count': orderlist.count,
                    'status': orderlist.status
                }, 200
    def patch(self, id):  
        orderlist = db.session.query(OrderList).get(id)
        data = request.get_json(force=True)

        if 'customer_id' in data:
            orderlist.name = data['customer_id']
        if 'product_id' in data:
            orderlist.description = data['product_id']
        if 'count' in data:
            orderlist.count = data['count']
        if 'status' in data:
            orderlist.status = data['status']
        db.session.commit()

        return  {
                    'id': orderlist.id,
                    'customer_id': orderlist.customer_id,
                    'product_id': orderlist.product_id,
                    'count': orderlist.count,
                    'status': orderlist.status
                }, 200

    def delete(self, id):  
        orderlist = db.session.query(OrderList).get(id)
        db.session.delete(orderlist)
        db.session.commit()
        return '', 204

@api.route('/')
class Main(Resource):
    def get(self):
        return {'status': OrderList.__tablename__}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80,debug=True)
 