import os

from flask import Flask, request, Response, jsonify
from flask_caching import Cache

import requests

config = {
    "DEBUG": True,          # Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related config
    "CACHE_DEFAULT_TIMEOUT": 300
}

base_url = "https://hatchways.io/api/assessment/blog/posts"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py', silent=True)
        app.config.from_mapping(config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    cache = Cache(app)

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({ "success": True })

    @app.route('/api/posts', methods=['GET'])
    @cache.cached(timeout=10, query_string=True)
    def posts():
        """

        """

        if "tags" not in request.args:
            return "Tags parameter is required", 400
        
        tags = request.args.get("tags").split(",")

        sortBy = request.args.get("sortBy", "id")

        if sortBy not in ["id", "likes", "reads", "popularity"]:
            return "sortBy parameter is invalid", 400

        direction = request.args.get("direction", "asc")

        if direction not in ["asc", "desc"]:
            return "direction parameter is invalid", 400

        posts = []
        for tag in tags:
            queries = { "tag": tag }
            r = requests.get(base_url, params=queries)
            if r.status_code !=200:
                raise requests.ApiError('GET /tasks/ {}'.format(r.status_code))
            data = r.json()
            posts.extend(post for post in data["posts"] if post not in posts) # remove duplicate dict entries

        response = sorted(posts, key = lambda k:k[sortBy], reverse = (direction == "desc"))
        return jsonify({ "posts": response })

    return app