from flask import Flask
import ssl

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    # app.run(ssl_context='adhoc') simple way. But you need to install pyopenssl

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='../../example.crt', keyfile='../../example.key')
    app.run(ssl_context=ssl_context)