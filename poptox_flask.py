from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
import os
try:
    from flask.ext.cors import CORS
except ImportError:
    cors = False
from REST import exponential_rest as exponential


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})


app = Flask(__name__)
api = Api(app)
try:
    CORS(app)
except Exception as e:
    print(str(e))


@app.route('/')
def hello_world():
    import sys
    version = sys.version
    return 'Poptox REST Server. Python Version = %s' % version


# Declare endpoints for each model
# These are the endpoints that will be introspected by the swagger() method & shown on API spec page
# TODO: Add model endpoints here once they are refactored
api.add_resource(exponential.ExponentialGet, '/rest/poptox/exponential/')
api.add_resource(exponential.ExponentialPost, '/rest/poptox/exponential/<string:jobId>')


@app.route("/api/spec/")
def spec():
    """
    Route that returns the Swagger formatted JSON representing the Ubertool API.
    :return: Swagger formatted JSON string
    """
    # from flask_swagger import swagger
    from uber_swagger import swagger

    swag = swagger(app)

    # TODO: Use in production and remove 'jsonify' below
    # return json.dumps(
    #     swag,
    #     separators=(',', ':')  # This produces a 'minified' JSON output
    # )

    return jsonify(swag)  # This produces a 'pretty printed' JSON output


@app.route("/api/")
def api_doc():
    """
    Route to serve the API documentation (Swagger UI) static page being served by the backend.
    :return:
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=7779, debug=True)
