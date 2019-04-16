import flask

app = flask.Flask("_main_")

@app.route("/")
def my_index():
    return flask.render_template("index.html",token="hello")

app.run(debug=True)