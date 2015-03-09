import os
import requests
import json
import random
from datetime import datetime, timedelta
import dateutil.parser
import time

import hashlib
from itsdangerous import TimestampSigner

from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for,
    session,
    flash,
    abort,
    current_app,
    render_template_string
)

from flask.ext.security import login_required
from flask.ext.mail import Message

from mongoengine import DoesNotExist, ValidationError

from www import (
    app,
    models,
    forms,
    locator,
    mail
)

from .utils import log_traceback, to_xml, to_csv

def _generate_token(email):
    from itsdangerous import TimestampSigner
    signer = TimestampSigner(app.config['SECRET_KEY'])
    return signer.sign(email).decode('utf8')

def _check_token(token):
    from itsdangerous import TimestampSigner, SignatureExpired
    signer = TimestampSigner(app.config['SECRET_KEY'])
    try:
        email = signer.unsign(token, max_age=app.config['TOKEN_MAX_AGE_SECONDS'])
        return email
    except SignatureExpired as e:
        current_app.logger.info('token expired %s' % e)
        return None

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
    locator.send_message({ "active": "www" })
    return render_template('index.html')

@app.route("/greenpaper")
def greenpaper():
    return render_template('greenpaper.html')

@app.route("/background-and-findings")
def background_and_findings():
    return render_template('background_and_findings.html')

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

@app.route("/<service_slug>/blog")
def blog(service_slug):
    try:
        service = models.Service.objects.get(slug=service_slug)
    except (DoesNotExist, ValidationError):
        abort(404)
    return render_template(get_scaffold_or_template(service_slug, 'blog'), service=service)

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
        return json.dumps(thing), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif format == "xml":
        return to_xml(thing), 200, {'Content-Type': 'application/xml; charset=utf-8'}
    elif format == "csv":
        return to_csv(thing), 200, {'Content-Type': 'text/csv; charset=utf-8'}
    else:
       abort(404)

@app.route("/search")
def search_results():
    search_term = request.args.get('q', '')
    scope = request.args.get('scope', '')
    results = []
    if scope == 'organisation':
        resp = requests.get("%s/organisations" % app.config['REGISTRY_BASE_URL'], params={'search_term': search_term})
        if resp.status_code == 200:
            for item in resp.json():
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

@app.route("/local-alerts/done", methods=['POST'])
def local_alerts_done():
    try:
        service = models.Service.objects.get(slug='local-alerts')
    except (DoesNotExist, ValidationError):
        abort(404)
    return render_template('local_alerts_done.html', service=service)

@app.route("/the-hatch")
@login_required
def the_hatch():
    applicants = models.InviteApplicant.objects.all()
    return render_template('invite_applications.html', applicants=applicants)

@app.route("/apply-for-invite", methods=['GET','POST'])
def apply():
    form = forms.InviteForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        if not models.InviteApplicant.objects.filter(email=email).first():
            applicant = models.InviteApplicant(full_name=full_name, email=email)
            applicant.save()
            token = _generate_token(email)
            confirmation_url = "%s/confirm-email/%s" % (app.config['BASE_URL'], token)
            html = render_template('confirm_email.html',  full_name=full_name, confirmation_url=confirmation_url)

            msg = Message(html=html,
                subject="Your application for an idealgov login",
                sender="noreply@idealnotreal.gov",
                recipients=[email])

            try:
                mail.send(msg)
                message  = "Thanks. You'll be getting a confirmation email soon at: %s." % email
                flash(message)
                return render_template('done.html', message=message)
            except Exception as ex:
                log_traceback(current_app.logger, ex)
                applicant.delete()
                flash("We weren't able to handle your request", 'error')
        else:
            flash("We've already had an application from : %s." % email)

        return redirect(url_for('apply'))
    return render_template('invite.html', form=form)


@app.route("/invite-user")
@login_required
def invite_user():
    email = request.args.get('email')
    full_name = request.args.get('full_name')
    if not (email or full_name):
        current_app.logger.info('must provide email and full name')
        return 400, 'Bad Request'

    www_id = app.config['WWW_CLIENT_ID']
    www_key = app.config['WWW_CLIENT_KEY']
    to_sign = '%s:%s:%s' % (www_id, email, full_name)
    signer = TimestampSigner(www_key, digest_method=hashlib.sha256)
    signed = signer.sign(to_sign)
    headers = { 'Authorisation': signed }
    url = '%s/register-user' % app.config['REGISTRY_BASE_URL']
    resp = requests.post(url, data={'email':email, 'full_name': full_name}, headers=headers)

    if resp.status_code == 201:
        user = models.InviteApplicant.objects.filter(email=email).first()
        user.invited = True
        user.save()
        token = _generate_token(email)
        confirmation_url = "%s/confirm-account/%s" % (app.config['BASE_URL'], token)
        html = render_template('confirm_account.html',  full_name=full_name, confirmation_url=confirmation_url)

        msg = Message(html=html,
                subject="Your idealgov account",
                sender="noreply@idealnotreal.gov",
                recipients=[email])
        try:
            mail.send(msg)
            flash("User account created. Invite sent to: %s." % email)
        except Exception as ex:
            log_traceback(current_app.logger, ex)
            flash("Failed to send invite to: %s" % email, 'error')
    else:
        flash('Error creating account', 'error')

    return redirect(url_for('the_hatch'))


@app.route("/confirm-email/<token>")
def confirm_email(token):
    email = _check_token(token).decode('utf8')
    if email:
        current_app.logger.info('email is %s' % email)
        message = "Email: %s confirmed." % email
        success=True
        user = models.InviteApplicant.objects.filter(email=email).first()
        user.email_confirmed = True
        user.save()
    else:
        current_app.logger.info('token has expired.')
        message = "Token %s has expired." % token
        success=False
    return render_template('confirmed.html', message=message, success=success)


@app.route("/confirm-account/<token>", methods=['GET','POST'])
def confirm_account(token):
    email = _check_token(token).decode('utf8')
    form = forms.SetPasswordForm()
    user = models.InviteApplicant.objects.filter(email=email).first()
    if not email:
        current_app.logger.info('token has expired.')
        flash('Link has expired', 'error')
    else:
        if user.password_set:
            flash('Account already confirmed and password set')
            return render_template('done.html', message='Account already confirmed and password set')

    if form.validate_on_submit():
        password = form.password.data
        www_id = app.config['WWW_CLIENT_ID']
        www_key = app.config['WWW_CLIENT_KEY']
        to_sign = '%s:%s:%s' % (www_id, email, password)
        signer = TimestampSigner(www_key, digest_method=hashlib.sha256)
        signed = signer.sign(to_sign)
        headers = { 'Authorisation': signed }
        url = '%s/update-user-password' % app.config['REGISTRY_BASE_URL']
        resp = requests.post(url, data={'email': email}, headers=headers)
        if resp.status_code == 200:
            user = models.InviteApplicant.objects.filter(email=email).first()
            user.password_set = True
            user.save()
            flash('Your password has been updated')
            return render_template('done.html', message='Your password has been updated')
        else:
            flash('Failed to set new password in registry', 'error')

    return render_template('set_account_password.html', form=form, token=token, user=user)
