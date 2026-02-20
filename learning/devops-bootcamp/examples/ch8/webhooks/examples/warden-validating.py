from flask import Flask, request, jsonify

warden = Flask(__name__)

#POST route for Admission Controller
@warden.route('/validate', methods=['POST'])

#Admission Control Logic
def deployment_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")
    try:
        if request_info["request"]["object"]["metadata"]["labels"].get("billing"):
            #Send response back to controller if validations succeeds
            return k8s_response(True, uid, "Billing label exists")
    except:
        return k8s_response(False, uid, "No labels exist. A Billing label is required")

    #Send response back to controller if failed
    return k8s_response(False, uid, "Not allowed without a billing label")

#Function to respond back to the Admission Controller
def k8s_response(allowed, uid, message):
     return jsonify({"apiVersion": "admission.k8s.io/v1", "kind": "AdmissionReview", "response": {"allowed": allowed, "uid": uid, "status": {"message": message}}})

if __name__ == '__main__':
    warden.run(ssl_context=('certs/wardencrt.pem', 'certs/wardenkey.pem'),debug=True, host='0.0.0.0')