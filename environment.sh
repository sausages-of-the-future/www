export SETTINGS='config.DevelopmentConfig'
export APP_ROOT='.'
export SECRET_KEY='local-dev-not-secret'
export CSRF_ENABLED=True
export SECURITY_PASSWORD_HASH='bcrypt'
export REGISTRY_BASE_URL='http://registry.gov.local'
export ORGANISATIONS_BASE_URL='http://organisations.gov.local'
export FISHING_BASE_URL='http://fishing.gov.local'
export BASE_URL='http://www.gov.local'

source environment_private.sh
