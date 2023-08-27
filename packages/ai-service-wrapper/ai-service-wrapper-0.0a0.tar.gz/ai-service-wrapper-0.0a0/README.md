# BE-Base-Python

# Implement
```python
from flask import Flask
from config import config
from ai_service_wrapper import AiServiceWrapper

def create_app():

    app = Flask(__name__)
    app.config.update(config)
    AiServiceWrapper(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run("0.0.0.0", 8000, debug=True)
```