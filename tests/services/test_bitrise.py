from responses import RequestsMock, GET

from bitrise import BitriseClient


test_token = 'unimportant'
success_status = 200
apps_payload = [
        {'title': 'app1'},
        {'title': 'app2'},
        {'title': 'app3'}
    ]

apps_json = {
    'data': apps_payload
}


def test_bitrise_services():
    client = BitriseClient(api_token=test_token)

    # Apps
    with RequestsMock() as get_resp:
        get_resp.add(GET, url=client.bitrise.apps.url, status=success_status, json=apps_json)

        app_list = client.apps
        assert app_list == apps_payload
