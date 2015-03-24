from flask import (
    Blueprint,
    render_template
)

paper = Blueprint('paper', __name__, template_folder="../templates/greenpaper")

@paper.route("/greenpaper")
def greenpaper():
    return render_template('greenpaper.html')

@paper.route("/background-and-findings")
def background_and_findings():
    return render_template('background-and-findings.html')

@paper.route("/concept")
def concept():
    return render_template('concept.html')

@paper.route("/registers")
def registers():
    return render_template('registers.html')

@paper.route("/services")
def services():
    return render_template('services.html')

@paper.route("/identity")
def identity():
    return render_template('identity.html')

@paper.route("/policy")
def policy():
    return render_template('policy.html')

@paper.route("/trust-and-consent")
def trust_and_consent():
    return render_template('trust-and-consent.html')

@paper.route("/technology")
def technology():
    return render_template('technology.html')

@paper.route("/platforms")
def platforms():
    return render_template('platforms.html')

@paper.route("/accountability")
def accountability():
    return render_template('accountability.html')

@paper.route("/where-to-start")
def where_to_start():
    return render_template('where-to-start.html')

@paper.route("/rules")
def rules():
    return render_template('rules.html')



