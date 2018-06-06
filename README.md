# bitrise
Python bindings for Bitrise API

```
client = BitriseClient(api_token=test_token)  # Can also set BITRISE_TOKEN environment variable

for app in client.apps:
    for build in app.builds:
        print(
            f"-----------  App: {app.title}  ------------\n"
            f"build {build.slug}\n"
            f"Triggered: {build.triggered_at}\n\n"

            "Artifacts:\n"
            f"{', '.join([file.title for file in build.details.artifacts])}"
            "\n"
        )

print(f"You can still access the raw JSON from Bitrise. This app's JSON: {app.data}")
```