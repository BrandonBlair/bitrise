from responses import RequestsMock, GET

from requests import Session

from bitrise import BitriseClient
from bitrise.services.apps import BitriseApp
from bitrise.services.builds import BitriseBuild


test_token = 'unimportant'
success_status = 200
test_app_slug = 'appslug'
test_build_slug = 'buildslug'


def test_bitrise_services():
    client = BitriseClient(api_token=test_token)

    # Apps
    apps_payload = [
        {'title': 'app1'},
        {'title': 'app2'},
        {'title': 'app3'}
    ]

    apps_json = {
        'data': apps_payload
    }
    with RequestsMock() as get_resp:
        get_resp.add(GET, url=client.bitrise.apps.url, status=success_status, json=apps_json)

        app_list = client.apps
        assert app_list[0].data['title'] == apps_payload[0]['title']

    # Builds
    sessn = Session()
    apps_url = client.bitrise.apps.url
    slug_url = f"{apps_url}/{test_app_slug}"
    app = BitriseApp(sessn, apps_url, {'slug': test_app_slug})

    builds_payload = [
        {'title': 'build1'},
        {'title': 'build2'},
        {'title': 'build3'}
    ]

    builds_json = {
        'data': builds_payload
    }
    with RequestsMock() as get_resp:
        builds_url = f"{slug_url}/builds?limit=10"
        get_resp.add(GET, url=builds_url, status=success_status, json=builds_json)

        builds = app.builds

        assert builds[0].data['title'] == builds_payload[0]['title']

    # Build Details
    builds_url = f"{apps_url}/{test_app_slug}/builds"
    print("Builds url: ", builds_url)
    build = BitriseBuild(sessn, builds_url, {'slug': test_build_slug})

    build_details_payload = [
        {'title': 'detail1'},
        {'title': 'detail2'},
        {'title': 'detail3'}
    ]

    build_details_json = {
        'data': build_details_payload
    }
    with RequestsMock() as get_resp:
        get_resp.add(
            GET,
            url=f"{builds_url}/{test_build_slug}",
            status=success_status,
            json=build_details_json
        )

        details = build.details

        assert details[0].data == build_details_payload[0]
