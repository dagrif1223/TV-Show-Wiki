# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from io import BytesIO
from flaskr import pages
import json
# Class for backend objects.
class Backend:
    # Backend class constructor
    def __init__(self, storage_client=storage.Client()):
        self.storage_client = storage_client
        self.content_bucket = storage_client.bucket('wiki_content')
        self.userInfo_bucket = storage_client.bucket('users-passwords')
        self.page_names = []

    # Gets an uploaded page from the content bucket.  
    def get_wiki_page(self, filename):
        if filename in self.page_names:
            blob = self.content_bucket.get_blob(filename + ".txt")
            file = blob.open()
            text = file.readlines()
            return text
        return None

    # Gets the name of all of the uploaded text files
    def get_all_page_names(self):
        blobs = self.content_bucket.list_blobs()
        self.page_names.clear()
        for blob in blobs:
            if blob.name[-4:] == ".txt":
                self.page_names.append(blob.name[:-4])
        return self.page_names
    
    # Adds data to the content bucket.
    def upload(self, filename, data):
        blob = self.content_bucket.blob(filename)
        with blob.open('wb') as f:
            f.write(data)

    """
    It stores password inside the file which named after each username in the gcs bucket. 
    """
    def sign_up(self,username,password,first_name, last_name):
        filename = username + ".txt"
        stats = storage.Blob(bucket = self.userInfo_bucket, name = filename).exists(self.storage_client)
        if stats:
            return "Username Taken!"
        blob = self.userInfo_bucket.blob(filename)
        data = {"username": username, "password": password, "first_name" : first_name, "last_name" : last_name}
        blob.upload_from_string(json.dumps(data))

    """
    It checks for the username by name of the file if it exists and then proceeds to check user credential inside the file.
    If it matches, lets the user login else does not.
    """
    def sign_in(self,username,password):
        filename = username + ".txt"
        blob = self.userInfo_bucket.blob(filename)
        stats = storage.Blob(bucket = self.userInfo_bucket, name = filename).exists(self.storage_client)
        if stats: 
            entered_password = hashlib.blake2b(password.encode()).hexdigest()
            stored_info = blob.download_as_text()
            info = json.loads(stored_info)
            stored_password = info["password"]
            if entered_password == stored_password:
                return True
        return False
    """
    Input: userId
    Returns: User Information except Password
    """
    def get_user_info(self,username):
        information = dict()
        filename = str(username) + ".txt"
        blob = self.userInfo_bucket.blob(filename)
        stored_info = blob.download_as_text()
        info = json.loads(stored_info)
        information["Firstname"] = info["first_name"]
        information["Secondname"] = info["last_name"]
        print(information)
        return information

    # Gets an image from the content bucket.
    def get_image(self, image_file):
        blob = self.content_bucket.get_blob(image_file)
        with blob.open('rb') as f:
            return BytesIO(f.read())

# b.upload('pages.py', 'Hello World!!')
#print(b.get_image('headshot.jpg'))

