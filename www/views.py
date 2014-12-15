from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from mongoengine import DoesNotExist, ValidationError
from www import app, models, forms
import os
import requests
import json

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

@app.route("/notes/<note_slug>")
def note(note_slug):
    return render_template('note_%s.html' % note_slug)

@app.route("/<service_slug>")
def service(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    service_base_url = app.config.get(service.service_base_url_config, '')
    return render_template(get_scaffold_or_template(service_slug, 'service'), service=service, service_base_url=service_base_url)

@app.route("/<service_slug>/policy")
def policy(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'policy'), service=service)

@app.route("/<service_slug>/complain", methods=['GET', 'POST'])
def complain(service_slug):
    sent = False
    form = forms.ComplaintForm(request.form)
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    if request.method == 'POST':
        if form.validate():
            sent = True
    return render_template(get_scaffold_or_template(service_slug, 'complain'), service=service, form=form, sent=sent)


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
        thing_uri = "%s/%s/%s" % (app.config['REGISTRY_BASE_URL'], things_slug, thing_slug)
        thing = requests.get(thing_uri).json()
    except (DoesNotExist, ValidationError):
        abort(404)

    service_base_url = app.config[service.service_base_url_config]
    return render_template(get_scaffold_or_template(service_slug, 'thing'), service=service, service_base_url=service_base_url, thing=thing)

@app.route("/search")
def search_results():
    search_term = request.args.get('q', '')
    scope = request.args.get('scope', '')
    results = []
    if scope == 'organisation':

        data = requests.get("%s/organisations" % app.config['REGISTRY_BASE_URL'])
        for item in data.json():
            split = item['uri'].split('/')
            results.append({'url': '/organisations/o/organisations/%s' % split[len(split) - 1], 'title': item['name']})
    return render_template('search-results.html', results=results, search_term=search_term, scope=scope)

@app.route("/<service_slug>/performance")
def performance(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'performance'), service=service)
