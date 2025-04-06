# Michael Niebauer
# COT 5930-007 COT 4930-001: Cloud Native Development
# Project 3 - Implement change management to your application and 
# create automation for deployment as well as automated testing. 
# Upon completion 50% of your users should see a blue background, 
# while the other 50% should see a green background on your front layer. 
# Traffic should be split evenly and you should be able to run the 2
#  versions of the application in parallel. Do not implement the split 
# logic in your application.
# 

# Imports
import os
from flask import Flask, render_template, request, redirect, url_for, Response
from google.cloud import storage
import random
import string
import json
import requests
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import secretmanager

app = Flask(__name__)


def access_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/cot4930-001/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_data = response.payload.data.decode("UTF-8")
    print(f"Secret data: {secret_data}")
    return secret_data

API_KEY = access_secret("API_KEY")
#model = genai.GenerativeModel("gemini-1.5-flash", api_key=API_KEY)
genai.configure(api_key=API_KEY)


def getBucket():
    bucket = 'cot4930private'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    return bucket

# Generate a random name for both images and json files
def randomNameGenerator():
    name_length = 6
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=name_length))
    print(random_name)
    return random_name

def saveImagesToCloudStorage(file, randomName):
    print('saving image to cloud')
    bucket = getBucket()
    filename = file.filename
    fileType = os.path.splitext(filename)[1][1:].strip().lower()
    newName = randomName + '.' + fileType
    blob = bucket.blob(newName)
    blob.upload_from_file(file)

def saveJSONTOCloudStorage(randomName, json_data):
    bucket = getBucket()
    randomFileName = randomName + '.json'
    title = json_data.get("title")
    caption = json_data.get("caption")
    #print("Title:", title)
    #print("Caption:", caption)
    json_title_desc = {"title": str(title), "description": str(caption)}
    json_string = json.dumps(json_title_desc)
    blob = bucket.blob(randomFileName)
    blob.upload_from_string(json_string, content_type='application/json')

def getImageDescription(file):
    image = Image.open(file)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Generate content from an image and prompt
    response = model.generate_content([
    "Generate one title and one caption for this image inn json format", 
    image
    ], stream=True)
    # Print the generated content
    response.resolve()  # Wait for response
    #print(response.text)
    description = response.text.replace('`','')
    description = description.replace('json','')
    description = json.loads(description)
    print(description)
    return description



# load images stored in cloud bucket
# load and parse the json files with title and description
def loadImagesFromCloudStorage():
    bucket = 'cot4930-001-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blobs = bucket.list_blobs()
    image_urls = []
    titles = []
    descriptions = []
    for blob in blobs:
        # loop over blobs for image files
        # store the url in a list
        if blob.name.endswith(('.jpg', '.jpeg')):
            image_urls.append(blob.public_url)
        # loop over blobs for json files
        # parse the json file for title and description   
        if blob.name.endswith(('.json')):
            json_data = blob.download_as_text()
            data = json.loads(json_data)
            titles.append(data.get('title'))
            descriptions.append(data.get('description'))
    return image_urls, titles, descriptions






"""
def loadImagesFromCloudStorage():
    bucket = getBucket()
    blobs = bucket.list_blobs()
    image_names = []
    titles = []
    descriptions = []
    for blob in blobs:
        # loop over blobs for image files
        # store the url in a list
        if blob.name.endswith(('.jpg', '.jpeg')):
            #image_urls.append(blob.public_url)
            image_names.append(blob.name)
            #print(image_names)
            # loop over blobs for json files
            # parse the json file for title and description   
        if blob.name.endswith(('.json')):
            json_data = blob.download_as_text()
            data = json.loads(json_data)
            titles.append(data.get('title'))
            descriptions.append(data.get('description'))
    return image_names,titles, descriptions
"""

# Route for home page and form submission
@app.route('/')
def index():

    # get file names from cloud storage
    image_filenames, titles, descriptions = loadImagesFromCloudStorage()
    
    # if no images pass 0 to the front
    num = len(image_filenames)
    if num is None:
        num = 0
    # when the user submits an image
    # a random number is generated for the name
    # the image gets saved to cloud storage
    # save title and caption in json format
    #if request.method == 'POST':
    #    file = request.files['file']
    #    randomName = randomNameGenerator()
    #    saveImagesToCloudStorage(file, randomName)
    #    json_data = getImageDescription(file)
    #    saveJSONTOCloudStorage(randomName, json_data)
    return render_template('index.html', image_filenames=image_filenames, titles=titles, descriptions=descriptions,num = num)
    
@app.route('/upload', methods=['POST'])
def upload_image():
    randomName = randomNameGenerator()
    file = request.files['file']
    saveImagesToCloudStorage(file, randomName)
    #KEY_API = getAPIkey()
    #json_data =  getImageDescription(file, KEY_API)
    json_data =  getImageDescription(file)
    saveJSONTOCloudStorage(randomName, json_data)
    return redirect(url_for('index'))




# Serve images for html
#@app.route('/image/<image_filename>')
#def serve_image(image_filename):
#    bucket = getBucket()
#    blob = bucket.blob(image_filename)
    # Download the image as bytes
#    image_data = blob.download_as_bytes()
    # Return the image with the appropriate content type
#    return Response(image_data, mimetype='image/jpeg')

# main - main 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)