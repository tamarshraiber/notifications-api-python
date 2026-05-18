from flask import Flask, request, jsonify
from processor import NotificationProcessor
from seed import seed
from repository import add_notification, get_all, find_by_id
from service import NotificationService
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

seed()

processor = NotificationProcessor()
service = NotificationService()

@app.route("/notifications", methods=["POST"])
def create():
    data = request.json or {}
    n = service.create_notification(data.get("target_channels"), data.get("message"))
    return jsonify(n.to_dict())


@app.route("/notifications", methods=["GET"])
def list_all():
    notifications = service.list_notifications()
    return jsonify([n.to_dict() for n in notifications])


@app.route("/notifications/<int:nid>", methods=["GET"])
def get_one(nid):
    n = service.get_notification(nid)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.to_dict())


@app.route("/notifications/<int:nid>", methods=["PUT"])
def update_one(nid):
    n = service.update_notification(nid, request.json)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.to_dict())


@app.route("/notifications/<int:nid>/send", methods=["POST"])
def send_one_route(nid):
    n = service.send_one(nid)
    if not n:
        return jsonify({"error": "not found"}), 404
    return jsonify(n.to_dict())


@app.route("/notifications/send-bulk", methods=["POST"])
def send_bulk():
    notifications = service.send_all()
    return jsonify([n.to_dict() for n in notifications])


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled exception")
    return jsonify({"error": "internal server error"}), 500


if __name__ == "__main__":
    app.run(port=3000)



