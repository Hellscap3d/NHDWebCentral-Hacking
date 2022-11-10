import flask, requests, os

app = flask.Flask(__name__)
baseurl = "https://site.nhd.org/"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if os.path.exists(f"overrides/{path}"):
        print("Using override")
        return flask.send_file(f"overrides/{path}")
    r = requests.request(flask.request.method, baseurl + path, headers=flask.request.headers, data=flask.request.data)
    if path == "Assets/editor.js?f@Portal.Core.ApplicationCore.Version":
        modcontent = r.content.replace(open("modold.js", "rb").read(), open("mod.js", "rb").read())
        return flask.Response(modcontent, mimetype=r.headers['content-type'], status=r.status_code)
    if path == "/Edit":
        return flask.Response(r.content.replace(b'<script src="/Assets/editor.js?f@Portal.Core.ApplicationCore.Version"></script>', b'<script src="/Assets/editor.js?f@Portal.Core.ApplicationCore.Version"></script>' + open("inject.html", "rb").read()), mimetype=r.headers['content-type'], status=r.status_code)
    return flask.Response(r.content, mimetype=r.headers['content-type'], status=r.status_code)

@app.route('/', methods=['GET', 'POST'])
def session():
    if flask.request.method == 'GET':
        return flask.render_template('session.html')
    elif flask.request.method == 'POST':
        session = flask.request.form['sessionid']
        resp = flask.make_response(flask.redirect('/Edit'))
        resp.set_cookie("portal-session", session)
        return resp

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")