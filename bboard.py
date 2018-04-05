from flask import Flask
from flask_restful import Api, Resource, request, marshal_with
from flask_httpauth import HTTPAuth
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import hashlib

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
auth = HTTPAuth(app)

app.config['SECRET_KEY'] = 'StonyMoon'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/bb'

db.create_all()

# class UserProfile(Resource):
#     @marshal_with(User.resource_fields, envelope='resource')
#     def get(self, id):
#         user = User.query.get(id)
#         return user
#
#
# class Map(Resource):
#     @marshal_with(User.resource_fields, envelope='resource')
#     def get(self):
#         return User.query.all()
#
#
# class BubbleDetail(Resource):
#     @marshal_with(Bubble.resource_fields, envelope='resource')
#     def get(self):
#         return Bubble.query.all()
#
#     def post(self):
#         uid = request.form['uid']
#         title = request.form['title']
#         content = request.form['content']
#         latitude = request.form['latitude']
#         longitude = request.form['longitude']
#         image1 = request.form['image1']
#         image2 = request.form['image2']
#         image3 = request.form['image3']
#         bubble = Bubble(uid=uid, title=title, content=content,
#                         latitude=latitude, longitude=longitude,
#                         image1=image1, image2=image2, image3=image3
#                         )
#         db.session.add(bubble)
#         db.session.commit()
#
#
# class MapBubble(Resource):
#     @marshal_with(Bubble.map_fields, envelope='result')
#     def get(self):
#         return Bubble.query.all()


# api.add_resource(Map, '/map')
# api.add_resource(UserProfile, '/user/<string:id>')
# api.add_resource(BubbleDetail, '/bubble')
# api.add_resource(MapBubble, '/map/bubble')

if __name__ == '__main__':
    app.run(debug=True)
