"""
Flask application that displays EC2 instance metadata:
- Instance ID
- Uptime
- Region
- Kernel / Linux version

Uses IMDSv2 (token-based) to query the EC2 instance metadata service.
Run with: python3 app.py
Then visit: http://<instance-ip>:5000/
"""

import platform
import subprocess
from datetime import timedelta

import requests
from flask import Flask, render_template_string

app = Flask(__name__)

METADATA_BASE = "http://169.254.169.254/latest"
TOKEN_TTL_SECONDS = "21600"  # 6 hours


def get_imds_token():
    """Fetch an IMDSv2 session token."""
    try:
        resp = requests.put(
            f"{METADATA_BASE}/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": TOKEN_TTL_SECONDS},
            timeout=2,
        )
        resp.raise_for_status()
        return resp.text
    except requests.RequestException:
        return None


def get_metadata(path, token):
    """Fetch a single metadata field using the IMDSv2 token."""
    try:
        headers = {"X-aws-ec2-metadata-token": token} if token else {}
        resp = requests.get(f"{METADATA_BASE}/{path}", headers=headers, timeout=2)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException:
        return "N/A"


def get_instance_id(token):
    return get_metadata("meta-data/instance-id", token)


def get_region(token):
    # dynamic/instance-identity/document returns JSON containing the region
    try:
        headers = {"X-aws-ec2-metadata-token": token} if token else {}
        resp = requests.get(
            f"{METADATA_BASE}/dynamic/instance-identity/document",
            headers=headers,
            timeout=2,
        )
        resp.raise_for_status()
        return resp.json().get("region", "N/A")
    except requests.RequestException:
        return "N/A"


def get_uptime():
    """Read system uptime from /proc/uptime and format it as human-readable."""
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        return str(timedelta(seconds=int(uptime_seconds)))
    except (FileNotFoundError, ValueError, IndexError):
        # Fallback for non-Linux / restricted environments
        try:
            output = subprocess.check_output(["uptime", "-p"], text=True)
            return output.strip()
        except Exception:
            return "N/A"


def get_kernel_info():
    """Return kernel name + release + version (uname -a style)."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "full": f"{uname.system} {uname.release} ({uname.version}) {uname.machine}",
    }


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EC2 Instance Info</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 2.5rem 3rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            width: 100%;
            max-width: 560px;
        }
        h1 {
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
            color: #f97316;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        td {
            padding: 0.75rem 0;
            border-bottom: 1px solid #334155;
            vertical-align: top;
        }
        td.label {
            color: #94a3b8;
            width: 40%;
            font-weight: 600;
        }
        td.value {
            font-family: "SFMono-Regular", Consolas, monospace;
            word-break: break-word;
        }
        tr:last-child td {
            border-bottom: none;
        }
        .footer {
            margin-top: 1.5rem;
            font-size: 0.75rem;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>&#9881; EC2 Instance Information</h1>
        <table>
            <tr>
                <td class="label">Instance ID</td>
                <td class="value">{{ instance_id }}</td>
            </tr>
            <tr>
                <td class="label">Region</td>
                <td class="value">{{ region }}</td>
            </tr>
            <tr>
                <td class="label">Uptime</td>
                <td class="value">{{ uptime }}</td>
            </tr>
            <tr>
                <td class="label">Kernel</td>
                <td class="value">{{ kernel.full }}</td>
            </tr>
        </table>
        <div class="footer">Refresh the page to update these values.</div>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    token = get_imds_token()
    context = {
        "instance_id": get_instance_id(token),
        "region": get_region(token),
        "uptime": get_uptime(),
        "kernel": get_kernel_info(),
    }
    return render_template_string(PAGE_TEMPLATE, **context)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/api/info")
def api_info():
    """JSON version of the same data, useful for scripts/monitoring."""
    token = get_imds_token()
    return {
        "instance_id": get_instance_id(token),
        "region": get_region(token),
        "uptime": get_uptime(),
        "kernel": get_kernel_info(),
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)