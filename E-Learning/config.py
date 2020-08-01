import os

class Config(object):
    #py -c "import os;print(os.urandom(16))"

    SECRET_KEY   = os.environ.get("SECRET_KEY") or b'-\x06\xac\x8d\xa9\\\xe4\x89/^\xc6\xce9Qn\x7f'

    MONGODB_SETTINGS ={"db" : "UTA_Enrollment"}