# bitrise
Python bindings for Bitrise API

```
client = BitriseClient(api_token=test_token)  # Can also set BITRISE_TOKEN environment variable

for app in client.apps:
    for build in app.builds:
        for file in build.details.artifacts:
            print(
                "---------------------------------------"
                f"Filename: {file.title}\n"
                f"Size in bytes: {file.file_size_bytes}"
            )
```