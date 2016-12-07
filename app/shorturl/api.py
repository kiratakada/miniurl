import json, httplib, string, base64, ast

from datetime import datetime
from flask.ext.restful import Resource as ApiResource
from flask.ext.restful import Api, reqparse
from flask import abort, Response, jsonify, request, redirect

from app import app, db

api = Api(app)

class ShortUrlApi(ApiResource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('url', type=unicode, required=True, location='json')
        self.reqparser.add_argument('signature', type=unicode, required=True, location='json')
        super(ShortUrlApi, self).__init__()

    def post(self):

        def check_signature(frontend_signature=None):
            date_today = datetime.now()
            key1 = base64.b64encode(args['url'])
            key2 = "%s%s" % (key1, app.config['SHORTEN_SALT'])
            server_signature = base64.b64encode(key2)

            if server_signature == frontend_signature:
                return True
            return False

        args = self.reqparser.parse_args()

        #split raw url with ?
        try:
            raw_url = args['url'].split('?')[0]
        except:
            raw_url = 'http://www.kiratakada.com/'

        key = base64.b64encode(raw_url)
        check = check_signature(args['signature'])

        if not check:
            temp = {}
            temp['status'] = httplib.UNAUTHORIZED
            temp['developer_message'] = "Invalid Signature"
            temp['error_code'] = 401101
            temp['user_message'] = "Unauthorized"

            return Response(json.dumps(temp), status=httplib.UNAUTHORIZED,
                mimetype='application/json')

        #remove unsused character ex: "=" from keys
        key = key.replace("=", '').strip()
        access = key[::-1][:8]

        exist_data = app.kvs.get('lnk:%s' % access)

        if exist_data:
            data = ast.literal_eval(exist_data)
            urls = data['shorten']
        else:
            urls = '%s%s' % (app.config['SHORTEN_BASE'], access)

            # set expired 6 Months on redis
            app.kvs.set('lnk:%s' % access, {'url': args['url'], 'shorten': urls}, ex=15552000)

        rv = {}
        rv['url'] = urls

        return Response(json.dumps(rv),
            status=httplib.OK, mimetype='application/json')


class ShortUrlLinkApi(ApiResource):

    def get(self, token=None):
        data = app.kvs.get('lnk:%s' % token)

        if not data:
            return Response(status=httplib.NOT_FOUND)
        else:
            logs = ast.literal_eval(data)
            return redirect(logs['url'], 301)


api.add_resource(ShortUrlApi, '/v1/urlshortener')
api.add_resource(ShortUrlLinkApi, '/<token>', endpoint='urlshortener')