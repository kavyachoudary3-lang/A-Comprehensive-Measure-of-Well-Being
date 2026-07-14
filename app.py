import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


def classify_hdi(life_expectancy, mean_years_schooling, expected_years_schooling, gni_per_capita):
    health_score = min(max((life_expectancy - 50) / 35, 0.0), 1.0)
    education_score = (
        min(max(mean_years_schooling / 15, 0.0), 1.0)
        + min(max(expected_years_schooling / 18, 0.0), 1.0)
    ) / 2
    income_score = 0.0
    if gni_per_capita > 100:
        income_score = min(
            max(
                (math.log(gni_per_capita) - math.log(100)) / (math.log(75000) - math.log(100)),
                0.0,
            ),
            1.0,
        )

    overall_score = round(0.35 * health_score + 0.35 * education_score + 0.30 * income_score, 3)

    if overall_score >= 0.8:
        category = "Very High"
    elif overall_score >= 0.6:
        category = "High"
    elif overall_score >= 0.4:
        category = "Medium"
    else:
        category = "Low"

    return {
        "score": overall_score,
        "score_percent": round(overall_score * 100, 1),
        "category": category,
        "health_score": round(health_score, 3),
        "education_score": round(education_score, 3),
        "income_score": round(income_score, 3),
    }


class HDIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/":
            self._serve_file("index.html", "text/html; charset=utf-8")
        elif path == "/styles.css":
            self._serve_file("styles.css", "text/css; charset=utf-8")
        elif path == "/script.js":
            self._serve_file("script.js", "application/javascript; charset=utf-8")
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/predict":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body)

        try:
            result = classify_hdi(
                float(data["life_expectancy"]),
                float(data["mean_years_schooling"]),
                float(data["expected_years_schooling"]),
                float(data["gni_per_capita"]),
            )
        except (KeyError, TypeError, ValueError):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Please provide valid numeric values."}).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode("utf-8"))

    def _serve_file(self, filename, content_type):
        file_path = ROOT / filename
        if not file_path.exists():
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(file_path.read_bytes())

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), HDIRequestHandler)
    print("HDI predictor running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
