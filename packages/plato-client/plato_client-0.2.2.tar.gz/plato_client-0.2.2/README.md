# Plato Client
Plato Client is a Python library that provides an interface to interact with the Plato Core API. It allows users to manage documents, generate content, and train models.

## Features
### Current
- Make calls to OpenAi Text Creation, Chat, and Image geenration endpoints without needing to manage API keys

### Coming Soon...
- Authentication with the Plato Core using the Oauth2 Client Credentials flow
- Document management abstraction (upload, download, find, and delete)
- User Management (via a Fastapi router you can add)
- Session Management (via a Fastapi router you can add)
- Content generation abstraction with various options (e.g., image generation, multihop, cache, moderation)
- Model training abstraction
- Centralized logging (routes to Datadog)

Please see https://bainco.atlassian.net/wiki/spaces/aagplato/pages/16918315581/Plato+Core#%F0%9F%92%80-Code-Skeletons for additonal information.

## Usage

Here are some examples of what you can do with the Plato Client:


```python
from plato_client.client import PlatoClient
client = PlatoClient(endpoint="http://127.0.0.1:8080")

# Generate text
print(client.text_completion("Roses are blue", model="gpt-4"))

# Chat
pprint(client.chat_completion(messages=[{"role": "user", "content": "Hello!"}]))

# Generate Image
print( client.create_images(prompt="Draw image of a dog playing by the pool", n=2, size="512x512"))
````

## Requirements
- Python 3.10.10 or later
- Poetry (Python Package Manager)
- Pip


## Installation
To install the Plato Client, you can run

```bash
make install
```

After installing the venv, source it (with source .venv/bin/activate) and the initialize pre-commit with pre-commit install. This will add pre-commits locally, such that code quality checks are run before each commit. To disable it, just add --no-verify after the commit (example: git commit -a -m "<commit-message>" --no-verify)