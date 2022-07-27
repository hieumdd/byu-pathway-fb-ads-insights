from typing import Any

from facebook.facebook_controller import facebook_controller


def main(request):
    data: dict[str, Any] = request.get_json()
    print(data)

    if "table" in data:
        response = facebook_controller(data)
        print(response)
        return response
    else:
        raise ValueError(data)
