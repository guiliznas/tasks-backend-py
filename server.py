from src.tester import Tester

tester = Tester()

# tester.run()
# tester.run_random()
# tester.run_batch(size=10)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
  app.run(debug=True)