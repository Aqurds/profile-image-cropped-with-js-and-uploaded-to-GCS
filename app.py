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


credentials = {
  "type": "service_account",
  "project_id": "propane-passkey-802",
  "private_key_id": "730384b78dce565567abdeb1034b098ce0437c7d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJqh/4JQyjXvMZ\nY34Hj4Rme3hyBh9Z7k2Xvd9BfSlAjXG3Pbhwbiex5TYNpPFN5oTdxpTBVZ0m/8X+\nOSF0Rvn55tF3WNvxo3OhwkN3593Zm4AMUNFbXc6taeRCBs1YrWa6FPSv+TDnWUmn\nnQTaaJ322VsVO8RScKFsCaAaEbVD1BLGTDTp03uJAAL5klVA9g78DGuhSjAbnqWW\nZbzi32y3eT9NiLSKEYUNUFxJzOPNnn/9jXJrbxoLgQpAYZtFdJhtFg/+aXk/WGn5\nUXXS+fFcoQnrob9fIhZzN9U+zmEeuER/BH4vYPIqhf2tHFVK4rJIdqiQJdbq8USk\n13kuzXj3AgMBAAECggEAW9h3pvR4xQ9BeJavl5Htox8oxAW10aeO/0UioRj36MaC\nvAoILmx897CE5cHxhKEwcjE3HrZ3VIO5EQfEDMkmoIJXdBusUGk5CLsJL1sS10DT\nGMjWEN6wepp3svqWG4Ud/DH/HwZHF5a6zPPeefqbtwlXSlxmFYXmfuYDXNwjyjfE\nGV78ZYIBUZGP+B5zmGwUoVH7BDMIxpz/TjcjFPnKJouGi2x9NxUyxGvR+sgJpnL/\nNG2bp/lBSrCbmANCIxDQ3UdFEXJx5iWlj5QaUg4pLjxJSt73JaZoZQHPKDwHumGh\nHwKCpVHyQlBgfCjLOexZpYQyCSg3ePSKwGTYPlfzwQKBgQD8X5EXYPpq0zaysAs3\nO1w3VUfoki+pqqO3zK3HJDmxgd6FP7s5f7yNvhp+gEpV6FavONWLwtdy5TZh+8xs\n3kiMICKo2pCgfRjdYqaLp+eo/1QNGmgMuKTlvHUWi0BuxxyEsLpBTpfI6r+zr8aV\nEFlTj9cMWEg95YZWuQ1AlchARQKBgQDMkAKhcPvc4CpSManfdI2V8POc36OkevLI\nF1WxcC3wLUDd8r4bBK9QszGOr9S3WgWxAUN2OG86bkByz+Ev/tpdAeK1oO9kYkK+\nA8AIGZIVWKgchjpMTovj+Uw2WOM8DDCLLFQ9xYGrKwfKq89oymyomlCAc78gqV8Y\njovp8Do+CwKBgQCOC+AnT39DFySnSGzXpoKN5mM15OoMzi2d6wc4mgwa++TaDPf9\nMgdXpFNXNjAg0EfSEeQn6P/I/HgyiD4UXLxqmj/H2FUk76RKHxdsbZH3TdbqFR3R\nYy/02rDwgmo+r7U+fhYnYewOuwoxQdM83VnZrZE1so7ev8xwDXIHEwcGHQKBgQCx\nDEtak0FKEDJQ5W8TWftZNSyEMAOgTlFm4NtoMaFw6Jnl/zyOgeWCwTU5O/Gtp5qZ\ncnCDF6EdP2NEe6t5MOip6wHfFaVcircdYn2IBSmslAkcdwhqFul4rMJLn288/4fc\nTMe0lwb9sMaToVRobBrTaowWQRfBGxaVWHq8RREDtQKBgChPheF69/GblFtR71sc\ncjzxwmeVHSqXWqZaAQIdSRN9NZ7AP06ScrlAgmphWgxYkQ50nFedtAPdLFdpcSsC\nRighMfaoaWl/DvO2pxlxRX9/xXrGlc8YxtJi+8R5Fg1Pz4cKnJm/kmcdMYSGIfml\nKgmHsy+LexbW35zWa+ob7HP8\n-----END PRIVATE KEY-----\n",
  "client_email": "base64-to-gcp@propane-passkey-802.iam.gserviceaccount.com",
  "client_id": "100224780312130152236",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/base64-to-gcp%40propane-passkey-802.iam.gserviceaccount.com"
}



# the function to upload base64 image string data to GCS and get back the url of the image
def upload_base64_data_to_gcs(bucket_name, base64_data, target_key):
    try:
        client = storage.Client(credentials=credentials)
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
