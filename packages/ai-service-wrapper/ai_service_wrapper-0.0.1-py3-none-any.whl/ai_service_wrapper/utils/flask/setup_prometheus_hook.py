import time

from flask import request

from ..prometheus import metrics

def start_timer():
    request.start_time = time.time()

def get_request_info():
    apikey = request.headers.get('x-api-key', "No Apikey")
    metrics.APIKEY_COUNT.labels('app', apikey).inc()

def stop_timer(res):
    response_time = time.time() - request.start_time
    metrics.REQUEST_LATENCY.labels('app', request.path).observe(response_time)
    return res

def record_request_data(res):
    metrics.REQUEST_COUNT.labels('app', request.method, request.path, res.status_code).inc()
    return res

def setup_metrics(app):
    app.before_request(start_timer)
    app.before_request(get_request_info)
    app.after_request(record_request_data)
    app.after_request(stop_timer)