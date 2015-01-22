import os
import requests
import json
import random
from datetime import datetime, timedelta
import dateutil.parser

from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for,
    session,
    flash,
    abort,
    current_app
)

from mongoengine import DoesNotExist, ValidationError

from www import (
    app,
    models,
    forms
)

def get_scaffold_or_template(service_slug, template_type):
    template = '%s_%s.html' % (service_slug.replace('-', '_'), template_type)
    if not os.path.exists('%s/%s/%s' % (os.path.dirname(os.path.abspath(__file__))
, app.template_folder, template)):
        template = 'default_%s.html' % template_type
    return template

def fake_timeseris_data(min, max):
    result =  []
    ends = datetime.today()
    duration = 365
    count = duration
    while count >= 0:
        date = ends - timedelta(days=count)
        result.append({'date': {"day": date.day, "month": date.month, "year": date.year}, 'value': random.uniform(min, max)})
        count = count - 1
    return result


#filters
@app.template_filter('cucumber')
def cucumber_filter(s):
    s = s.replace('Given', '<strong>Given</strong>')
    s = s.replace('When', '<br/><strong>When</strong>')
    s = s.replace('Then', '<br/><strong>Then</strong>')
    return '<p class="policy">%s</p>' % s

@app.template_filter('format_money')
def format_money_filter(value):
    return "{:,.2f}".format(value)

@app.template_filter('format_date')
def format_date_filter(value):
    date = dateutil.parser.parse(str(value))
    return date.strftime('%A %d %B')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/start")
def start():
    services = models.Service.objects.all()
    return render_template('start.html', services=services)

@app.route("/notes/<note_slug>")
def note(note_slug):
    return render_template('note_%s.html' % note_slug)

@app.route("/work-visa")
def work_visa_service():
    # custom one for this service, as need to get some other info
    try:
        service = models.Service.objects.get(slug='work-visa')
    except (DoesNotExist, ValidationError):
        abort(404)

    lists_uri = "%s/lists" % (app.config['REGISTRY_BASE_URL'])
    lists = requests.get(lists_uri).json()
    occupation_list_id = ''
    for list_ in lists:
        if list_['name'] == "Shortage occupation list":
            occupation_list_id = list_['uri'].split('/')[len(list_['uri'].split('/') ) -1]

    service_base_url = app.config.get(service.service_base_url_config, '')
    return render_template('work_visa_service.html', service=service, service_base_url=service_base_url, occupation_list_id=occupation_list_id)

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
    agm_date = datetime.now() + timedelta(days=random.randint(5, 130))
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    if request.method == 'POST':
        if form.validate():
            sent = True
    return render_template(get_scaffold_or_template(service_slug, 'complain'), service=service, form=form, sent=sent, agm_date=agm_date)

@app.route("/<service_slug>/legislation")
def legislation(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)

    return render_template(get_scaffold_or_template(service_slug, 'legislation'), service=service)

@app.route("/<service_slug>/o/<things_slug>/<thing_slug>")
@app.route("/<service_slug>/o/<things_slug>/<thing_slug>.<format>")
def thing(service_slug, things_slug, thing_slug, format="html"):
    try:
        service = models.Service.objects.get(slug=service_slug)
        thing_uri = "%s/%s/%s" % (app.config['REGISTRY_BASE_URL'], things_slug, thing_slug)
        thing = requests.get(thing_uri).json()

    except (DoesNotExist, ValidationError):
        abort(404)

    service_base_url = app.config[service.service_base_url_config]

    if format == "html":
        return render_template(get_scaffold_or_template(service_slug, 'thing'), service=service, service_base_url=service_base_url, thing=thing, thing_slug=thing_slug)
    elif format == "json":
        return json.dumps(thing)
    else:
       abort(404)

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

    stats = []
    for stat in service.stats:
        stats.append({"name": stat['name'], "data": fake_timeseris_data(stat['min'], stat['max']), "y_max": stat['y_max']})

    return render_template(get_scaffold_or_template(service_slug, 'performance'), service=service, stats=json.dumps(stats))

#specific pages
@app.route("/fishing/byelaws")
def fishing_bye_laws():
    try:
        service = models.Service.objects.get(slug='fishing')
    except (DoesNotExist, ValidationError):
        abort(404)
    return render_template('fishing_thing.html', service=service)

#specific pages
@app.route("/work/book-appointment")
def work_book_appointment():
    try:
        service = models.Service.objects.get(slug='work')
    except (DoesNotExist, ValidationError):
        abort(404)
    return render_template('work_book_appointment.html', service=service)

#internal tools (should really be a seperate app)
@app.route("/internal/dashboard")
def internal_dashboard():
    return render_template('internal_dashboard.html')