#NOTE webserfor for ice_breaker_v5_full_stack

from dotenv import load_dotenv
from flask import Flask,render_template, request, jsonify
from ice_breaker_v5_full_stack import ice_break_with
import os
load_dotenv()

print(f"API Key: {os.getenv('LANGCHAIN_API_KEY')[:10]}...")
print(f"Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"Project:  {os.getenv('LANGCHAIN_PROJECT')}")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("ice_breaker_index.html")

@app.route("/process",methods = ["POST"])
def process():
    name = request.form['name']
    summary, profile_pic_url = ice_break_with(name= name)

    return jsonify(
        {
            "summary_and_facts":summary.to_dict(),
            "photoUrl": profile_pic_url
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
