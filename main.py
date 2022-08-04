from typing import Any

from facebook.facebook_service import pipeline_service, tasks_service


def main(request):
    data: dict[str, Any] = request.get_json()
    print(data)

    if "table" in data:
        response = pipeline_service(data["table"], data.get("start"), data.get("end"))
    elif "tasks" in data:
        response = tasks_service(data.get("start"), data.get("end"))
    else:
        raise ValueError(data)

    print(response)
    return response
