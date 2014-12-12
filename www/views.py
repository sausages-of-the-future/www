from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from mongoengine import DoesNotExist, ValidationError
from www import app, models
import os

def get_scaffold_or_template(service_slug, template_type):
    template = '%s_%s.html' % (service_slug, template_type)
    if not os.path.exists('%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__))
, app.template_folder, template)):
        template = 'default_%s.html' % template_type
    return template

#filters
@app.template_filter('cucumber')
def cucumber_filter(s):
    s = s.replace('Given', '<strong>Given</strong>')
    s = s.replace('When', '<br/><strong>When</strong>')
    s = s.replace('Then', '<br/><strong>Then</strong>')
    return '<p class="policy">%s</p>' % s

@app.route("/")
def index():
    services = models.Service.objects.all()
    return render_template('index.html', services=services)

@app.route("/<service_slug>")
def service(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    service_base_url = app.config[service.service_base_url_config]
    return render_template(get_scaffold_or_template(service_slug, 'service'), service=service, service_base_url=service_base_url)

@app.route("/<service_slug>/policy")
def policy(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'policy'), service=service)

@app.route("/<service_slug>/legislation")
def legislation(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'legislation'), service=service)

@app.route("/<service_slug>/o/<things_slug>/<thing_slug>")
def thing(service_slug, things_slug, thing_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    service_base_url = app.config[service.service_base_url_config]
    return render_template(get_scaffold_or_template(service_slug, 'thing'), service=service, service_base_url=service_base_url)

@app.route("/search")
def search_results():
    search_term = request.args.get('q', '')
    scope = request.args.get('scope', '')
    results = [
            {'url': '/organisations/o/organisations/7d4ae8099a7a742be63dba33cd9062ea', 'title': 'Sunway Group Ltd'},
            {'url': '/organisations/o/organisations/7d4ae8099a7a742be63dba33cd9062ea', 'title': 'Sunway Ltd'},
            {'url': '/organisations/o/organisations/7d4ae8099a7a742be63dba33cd9062ea', 'title': 'Sunway Community Federation CIC'},
            {'url': '/organisations/o/organisations/7d4ae8099a7a742be63dba33cd9062ea', 'title': 'Sunway Digital'},
            {'url': '/organisations/o/organisations/7d4ae8099a7a742be63dba33cd9062ea', 'title': 'Sunway Charitable Trust'},
              ]
    return render_template('search-results.html', results=results, search_term=search_term, scope=scope)

@app.route("/<service_slug>/performance")
def performance(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'performance'), service=service)
