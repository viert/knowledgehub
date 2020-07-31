from glasskit.api import json_response, paginated
from glasskit.utils import get_user_from_app_context
from glasskit.errors import NotFound
from ask.controllers import AuthController
from ask.models import User
from ask.models.event import Event


events_ctrl = AuthController("events", __name__, require_auth=True)


@events_ctrl.route("/")
def index():
    user: User = get_user_from_app_context()
    events = user.get_new_events().sort("created_at", -1)
    return json_response(paginated(events, transform=lambda event: event.api_dict()))


@events_ctrl.route("/<event_id>/dismiss", methods=["POST"])
def dismiss(event_id):
    user: User = get_user_from_app_context()
    event = Event.get(event_id, "event not found")
    if event.user_id != user._id:
        raise NotFound("event not found")
    if not event.dismissed:
        event.dismiss()
    return json_response({"data": event.api_dict()})


@events_ctrl.route("/dismiss_all", methods=["POST"])
def dismiss_all():
    user: User = get_user_from_app_context()
    Event.update_many({"user_id": user._id, "dismissed": False}, {"$set": {"dismissed": True}})
    return json_response({"status": "dismissed"})
