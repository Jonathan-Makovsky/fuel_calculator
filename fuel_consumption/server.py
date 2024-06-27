from flask import request, Flask

# Good examples of using flask for basic requests: https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/hello")
def hello():
    return "<p>halo!</p>"

@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)

@app.route('/postreq', methods=['POST'])
def postreq():
    return '''The Given value is: {}'''.format(request.args.get('value'))


# GET requests will be blocked
'''
{
    "language" : "Python",
    "framework" : "Flask",
    "website" : "Scotch",
    "version_info" : {
        "python" : "3.9.0",
        "flask" : "1.1.2"
    },
    "examples" : ["query", "form", "json"],
    "boolean_test" : true
}
'''
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)