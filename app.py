from flask import Flask, render_template, request, jsonify, redirect
from parser_kitchen.together import Our_result
app = Flask(__name__)
@app.route('/')
def main():
    return render_template("index.html")
@app.route('/find', methods = ["POST"])
def parse():
    job = str(request.form['job']).replace(" ", "-").lower()
    print(job)
    town = str(request.form['town']).replace(" ", "-").lower()
    print(town)
    data = Our_result(town, job).get_data()
    return render_template("out.html", vacancies=data)

if __name__ == "__main__":
    app.run(debug=True)
