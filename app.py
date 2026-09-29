import os
import secrets
import requests
from flask import Flask, request, jsonify, Response, abort

app = Flask(__name__)

@app.before_request
def service_identity():
    if request.path == '/health':
        return None
    key = os.environ.get('SERVICE_KEY', '')
    if not key:
        abort(503)
    if not secrets.compare_digest(request.headers.get('X-Service-Key', ''), key):
        abort(401)

@app.get('/health')
def health():
    return {'status': 'ready'}

def call(service, path, method='POST', **kwargs):
    headers = {'X-Service-Key': os.environ['SERVICE_KEY']}
    for key in ('X-User-Id', 'X-Tenant-Id'):
        if request.headers.get(key):
            headers[key] = request.headers[key]
    base = os.environ.get(service.upper() + '_URL', 'http://' + service + ':8080')
    return requests.request(method, base + path, headers=headers, timeout=10, **kwargs)

import re

ORDERS = {
    'north-001': {'tenant': 'north', 'total': 150, 'shipping_address': '10 North Street'},
    'south-002': {'tenant': 'south', 'total': 480, 'shipping_address': '20 South Street'},
}

@app.get('/orders/<order_id>')
def order(order_id):
    item = ORDERS.get(order_id)
    if not item or item['tenant'] != request.headers.get('X-Tenant-Id'):
        abort(404)
    return jsonify(item)

@app.get('/search')
def search():
    term = request.args.get('q', '')
    if not re.fullmatch(r'[A-Za-z0-9%_ .-]{0,240}', term):
        abort(400)
    result = call('query', '/search', json={'term': term})
    return Response(result.content, status=result.status_code, content_type='application/json')

@app.get('/lookup')
def lookup():
    result = call('query', '/lookup', json={'term': request.args.get('q', '')})
    return Response(result.content, status=result.status_code, content_type='application/json')
