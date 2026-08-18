from flask import Flask, render_template
import requests

app = Flask(__name__)

TOKEN_URL = "http://169.254.169.254/latest/api/token"
METADATA_URL = "http://169.254.169.254/latest/meta-data"

def get_metadata(path):
    token = requests.put(
        TOKEN_URL,
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    ).text

    response = requests.get(
        f"{METADATA_URL}/{path}",
        headers={"X-aws-ec2-metadata-token": token}
    )

    return response.text

@app.route("/")
def index():
    instance_id = get_metadata("instance-id")
    private_ip = get_metadata("local-ipv4")
    public_ip = get_metadata("public-ipv4")

    # Get region using identity document
    token = requests.put(
        TOKEN_URL,
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    ).text

    identity = requests.get(
        "http://169.254.169.254/latest/dynamic/instance-identity/document",
        headers={"X-aws-ec2-metadata-token": token}
    ).json()

    region = identity["region"]

    return render_template(
        "index.html",
        instance_id=instance_id,
        private_ip=private_ip,
        public_ip=public_ip,
        region=region
    )

app.run(host="0.0.0.0", port=8080)