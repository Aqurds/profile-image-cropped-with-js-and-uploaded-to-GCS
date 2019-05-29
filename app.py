from flask import Flask, render_template, request, jsonify
import os
import base64
import random
from google.cloud import storage
# from PIL import Image
# import cv2

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024



# home route
@app.route('/')
def home():
    return render_template('index.html')




# the function to upload base64 image string data to GCS and get back the url of the image
def upload_base64_data_to_gcs(bucket_name, base64_data, target_key):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        bucket.blob(target_key).upload_from_string(base64_data)
        return bucket.blob(target_key).public_url

    except Exception as e:
        print(e)

    return None



# # the function to upload image to GCS and get back the url of the image
# def upload_image_to_gcs(bucket_name, local_path, local_file_name, target_key):
#     try:
#         client = storage.Client()
#         bucket = client.bucket(bucket_name)
#         full_file_path = os.path.join(local_path, local_file_name)
#         bucket.blob(target_key).upload_from_filename(full_file_path)
#         return bucket.blob(target_key).public_url
#
#     except Exception as e:
#         print(e)
#
#     return None
#



# api route to get cropped image data
@app.route('/croppedimage', methods=['POST', 'GET'])
def croppedimage():

    imagedata = request.data

    # get the file size of the base64 data of cropped image
    print((len(imagedata) * 3) / 4)

    # this line will slice the original data, if ajax post the whole base64 string without slicing the head
    # rawimagedata = imagedata.split(",")[1]

    # decode the base64 string
    imgdata = base64.b64decode(imagedata)

    # this context will write the base64 data in a text file, if that's needed for different useage
    # with open('test.txt', 'w') as text:
    #     text.write(imagedata.decode("utf-8"))

    x = random.randint(1, 100000)
    x = str(x)

    filename = x + 'profile.png'  # Here put your specific image name

    # upload base64 data to GCS
    image_link_url = upload_base64_data_to_gcs("staging.propane-passkey-802.appspot.com", imgdata, filename)
    print(image_link_url)

    # # write the base64 data as image to local machine
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)


    # # upload image to GCS
    # local_path = os.path.dirname(os.path.realpath(__file__))
    # image_link_url = upload_image_to_gcs("staging.propane-passkey-802.appspot.com", local_path, filename, filename)
    # print(image_link_url)


    return jsonify({'imageurl': image_link_url})





if __name__ == '__main__':
    app.run(debug=True)
