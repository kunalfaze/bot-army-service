# Import the Firebase service
from pprint import pprint

import firebase_admin
from firebase_admin import auth
import uuid
from pymongo import MongoClient
from password_helper import make_pseudo_word


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/botArmyDb"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient

    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['botArmyDb']


STAGE_CRED = {
    "type": "service_account",
    "project_id": "faze-stage",
    "private_key_id": "1ba5cab54210dace0fdbf6c91089f4dd0c31b4d6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCUtium6d4GKsYP\nNWrxF7TBSVqgEoO2XTjb9BQoN+E/nV3PXvGqqW9TaSGCPBK3WdrHV/cg1XCDCOwX\nIhcrQwNxYWmsp1G+G//HCRePuwkgKX9H8jtyDCPXqa4r1+2dZKip5UB2QAJWK1EM\nk4MyPoax1WsfdYtz+4R5piPkWzDYLdO0TaY1GK+5anjKVNKNHpFfxywa33m6NDJD\nsOAb9zCTOg3796BbTx2yuQ/C0rUlwo2Zlnp9AZ5kMCsaZi8EYoHMpC4SzNW4Vph3\ndWLnyXRbX8UmGH1ySMl5sTDq4BpebpLUOjgOcxpHcAI/1Jwy+SJ+O9RzHoxwPzNW\n1oHXB2uBAgMBAAECggEABi9BfL3fvnrU1UEBQfD8qD1c8V4KaqvGaksEnmu82IdQ\nBX3TIrK3TGfe2BftO9aW7+DSHbmUBgEO8i3YOpPShB/l3rjagDkRdRAP3KnYbkUy\nM8uTSmc5Q4tycMSYb1SmY+LCwJWMJf8Dw4MBgGtjsOg5ffu77q6EbYY52nyqjlJL\nprinMgzudUc2ZDhPWbq4jl4m7a3a5a6jareWdSxq2GLSKSbTOy37CbYZz31ChXYY\nJw6zMtO29/sGjZEzcRfpAV/E1IEyT+Q3bLsQI7SQDlTB68VkijWuZubhVdHisDdK\nYjqLqWnqmesszvCtqR6rV2PEuKhSFa/6bo8pIrohSQKBgQDQXnXGoKAS54mYhUFu\nW9HZHrKelxpJSSdSFlwt7nrGiiwWbGF80h8vIlxfx52YenJGllK0EZy1VIR2NjZj\nmNwZ6XU4yw0DX+ePkvX+60bvVhKbFVcI2f/AlS652XOld73NUJnjfF1JP98hyKaR\nG2+VXD2Cro5dh+qHcVVlmc1GmQKBgQC2tJ8bTUdb8q2KiID0JITdYMnKfB21I+n2\nBkvUuNBa6oJNVXSMNV2TReSTv3q53IgmH9IIoI6I9s/meciTnKWPfGL8YJgeqv4E\nAGoY3vp6Yr2JAa+vmCyslioM5ZwbmVkeAa6YDXw64GFrNxSQbnJj78iPReRQhEkX\neEpqSGslKQKBgAu6lXSVzAzkXZlpPtKgdoJ7OOC2brNbW8xCF/Q57U1Jr8ufVCl7\nhmfXzk1R5iwUEGSqx4L9Ts3iMQaabJtUmmcW/hMxUs0y080AH7q2sap9NNTn8Zs8\n8il7/EJX3CufPt7Uv6TPdkzOPJghPEcEvVYx+ABoJPlc0jXHimAKtURZAoGAVLMb\nZ57FzByO00BA9+3OIoryQYqUgxspJUL5+J3NCbjZu1w4cZ9zyAiI1O3ZyTwxaesq\nhZFZQqmY6/HdSIFAR2qUwQdOvjjrFZPTm8ATQpVv5IoBllfnrgLXb68qVakbpUuG\nUzs9MlY/E2Mvh12MbkQFKFZwZ9tLvzOm2+rCsTECgYAo/4cfGCXJhlsDqiZrN5OT\nku2gaffRxlYRlGjkGMI/pZ90U3WyqeS2BwcC8ceoqO+K1dWdTI0X3iSvs6HQJAqY\n8J4e1z2mF/05fOl7NaBNVGVwJSlzPfinpNiXKxrrKKQPeHENHlvIs4WW2E1A9hj0\nwqz8HviLLlIVrplPMb+cCw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-s3dgj@faze-stage.iam.gserviceaccount.com",
    "client_id": "117791651170463930182",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-s3dgj%40faze-stage.iam.gserviceaccount.com"
};


def get_bot_user_collection_name():
    return "botUsers"


# build credentials with the service account dict
creds = firebase_admin.credentials.Certificate(STAGE_CRED)

# Initialize the default app
default_app = firebase_admin.initialize_app(creds)

print(default_app.name)  # "[DEFAULT]"

dbname = get_database()
BOT_USER_DB_COLLECTION = dbname[get_bot_user_collection_name()]

doc_list = []
for i in range(0, 1):
    uuid_no = uuid.uuid4()
    password = make_pseudo_word(8)
    email = "fcstagebot+{name}@gmail.com".format(name=password)
    user = auth.create_user(
        email=email,
        email_verified=True,
        password=password,
        display_name='John Doe',
        disabled=False)

    doc_list.append({"email": email,
                     "email_verified": True,
                     "password": password,
                     "display_name": 'John Doe',
                     "uid":user.uid,
                     "disabled": False})
    print('Successfully created new user: {0}'.format(user.uid))

BOT_USER_DB_COLLECTION.insert_many(doc_list)

# Retrieve default services via the auth package...
# auth.create_custom_token(...)

# Use the `app` argument to retrieve the other app's services
# auth.create_custom_token(..., app=other_app)
