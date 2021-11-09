from flask import Flask
from flask_restful import Resource, reqparse, Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


from base import data, db
db.init_app(app)
app.app_context().push()
db.create_all()

class data_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page_url', type=str, required=True, help='page_url of the data_Item')
    parser.add_argument('page_view_count', type=int, required=True, help='page_view_count of the data_Item')
    parser.add_argument('last_seen', type=str, required=True, help='last_seen of the data_Item')
    parser.add_argument('timestamp', action='append', required=True, help='timestamp list of the data_Item')
    
    def get(self, data_Item_Id):
        item = data.find_by_id(data_Item_Id)
        if item:
            return item.json()
        return {'Message': 'ID = {} is not found'.format(data_Item_Id)}
    
    def post(self, data_Item_Id):
        if data.find_by_id(data_Item_Id):
            return {' Message': 'Data Item with ID = {} already exists'.format(data_Item_Id)}
        args = data_List.parser.parse_args()
        item = data(data_Item_Id, args['page_url'], args['page_view_count'], args['last_seen'], args['timestamp'])
        item.save_to()
        return item.json()
        
    def put(self, data_Item_Id):
        args = data_List.parser.parse_args()
        print(args.timestamp)
        item = data.find_by_id(data_Item_Id)
        if item:
            item.page_url = args['page_url']
            item.page_view_count = args['page_view_count']
            item.last_seen = args['last_seen']
            item.timestamp = args['timestamp']
            item.save_to()
            return {'dataItem': item.json()}
        item = data(data_Item_Id, args['page_url'], args['page_view_count'], args['last_seen'], args['timestamp'])
        item.save_to()
        return item.json()
            
    def delete(self, data_Item_Id):
        item  = data.find_by_id(data_Item_Id)
        if item:
            item.delete()
            return {'Message': 'Data Item with ID = {} has been deleted from records'.format(data_Item_Id)}
        return {'Message': 'ID = {} is already not on the list'.format(data_Item_Id)}
    
class All_data(Resource):
    def get(self):
        return {'Data': list(map(lambda x: x.json(), data.query.all()))}
    
api.add_resource(All_data, '/')
api.add_resource(data_List, '/<string:data_Item_Id>')

if __name__=='__main__':
    
    app.run(debug=True)
