from flask import Flask, request, jsonify
from processor import NotificationProcessor
from seed import seed
from repository import add_notification, get_all, find_by_id
from service import NotificationService

app = Flask(__name__)

seed()

processor = NotificationProcessor()
service = NotificationService()

@app.route("/notifications", methods=["POST"])
def create():
    data = request.json or {}
    n = service.create_notification(data.get("targetChannels"), data.get("message"))
    return jsonify(n.__dict__)


@app.route("/notifications", methods=["GET"])
def list_all():
    notifications = service.list_notifications()
    return jsonify([n.__dict__ for n in notifications])


@app.route("/notifications/<int:nid>", methods=["GET"])
def get_one(nid):
    n = service.get_notification(nid)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.__dict__)


@app.route("/notifications/<int:nid>", methods=["PUT"])
def update_one(nid):
    n = service.update_notification(nid, request.json)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.__dict__)


@app.route("/notifications/<int:nid>/send", methods=["POST"])
def send_one_route(nid):
    n = service.send_one(nid)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.__dict__)


@app.route("/notifications/send-bulk", methods=["POST"])
def send_bulk():
    notifications = service.send_all()
    return jsonify([n.__dict__ for n in notifications])


if __name__ == "__main__":
    app.run(port=3000)



