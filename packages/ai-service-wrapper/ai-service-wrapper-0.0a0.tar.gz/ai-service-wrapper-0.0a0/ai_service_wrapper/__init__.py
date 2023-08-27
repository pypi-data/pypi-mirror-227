import prometheus_client
from flask import request, Response
from .apisignature.decorators import api_signature_required
from .apisignature.sign import create_sign_header
from .utils.prometheus.metrics import CONTENT_TYPE_LATEST
from .utils.flask import setup_prometheus_hook
from .utils.flask.http_scheme import HttpResonse

class AiServiceWrapper:

    def __init__(self, 
                 app, 
                 apply_prometheus=True, 
                 api_service_host=None): 

        self.app = app
        if apply_prometheus:
            setup_prometheus_hook.setup_metrics(app) 
        
        from .utils.flask.error_handler import error_handler
        app.register_blueprint(error_handler)

        @app.route('/health')
        def health():
            return HttpResonse.success(message="Ok", status_code=200)

        @app.route('/metrics/')
        def metrics():
            return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST) 
            
        @app.route("/test-api-signature")
        @api_signature_required(
            private_key_file=app.config["application"]["private_key_file"],
            apikey_service_host=app.config["application"]["apikey_service_host"]
        )
        def test_api_signature():
            return  HttpResonse.success(None, "Ok", 200)

        @app.route("/sign-api-signature", methods=["POST"]) 
        def sign_api_signature():
            apikey = request.headers.get("x-api-key")
            if not apikey:
                return HttpResonse.fail(None, "No api key provided", 403)
            headers = create_sign_header(apikey=apikey)
            return HttpResonse.success(headers, "Sign success!", 200)