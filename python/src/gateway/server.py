import os, gridfs, pika, json, logging, datetime
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

date = datetime.date.today()
logging.basicConfig(filename=f"{date}gateway.log", filemode='w', format="%(name)s - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)



server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")

mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    logging.debug(msg=f"The token is: {token}")

    if not err:
        return token
    else:
        logging.error(msg=f"{err}")
        return err


@server.route("/upload", methods=["POST"])
def upload():
    key, err = validate.token(request)
    logging.debug(f"Key is: {key}")

    if err:
        logging.error(f"{err}")
        return err

    key = json.loads(key)
    logging.debug(f"Key was loaded")
    if key["admin"]:
        logging.debug(f"File that was sent: \n{request.files}")
        if len(request.files) > 1 or len(request.files) < 1:
            logging.debug(f"Either more than or less than 1 file was supplied, Code: 400")
            return "exactly 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, key)

            if err:
                logging.error(f"{err}")
                return err
        logging.info(f"Success, Code: 200")
        return "success!", 200
    else:
        logging.debug(f"Not Authorized, Code: 401")
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    key, err = validate.token(request)
    logging.debug(f"Key is: {key}")
    if err:
        return err

    key = json.loads(key)

    if key["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
    logging.debug(f"Host running on {server.host} and port {server.port}")