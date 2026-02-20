from flask import Flask, request, jsonify
import re
import jsonpatch
import base64

warden = Flask(__name__)

#POST route for Admission Controller
@warden.route('/validate', methods=['POST'])
#Admission Control Logic - validating
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")

    # Code for validating webhook HERE

#POST route for Admission Controller
@warden.route("/mutate", methods=["POST"])
#Admission Control Logic - mutating
def mutatating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")

    # Code for mutating webhook HERE
if __name__ == '__main__':
    warden.run(ssl_context=('certs/wardencrt.pem', 'certs/wardenkey.pem'),debug=True, host='0.0.0.0')
