from flask import Flask;
import os
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        name = request.form["name"]
        email= request.form["email"]
        mobile = request.form["mobile"]
        return redirect(url_for('output', name=name, email=email, mobile=mobile))
    return render_template('Home.html')
@app.route("/output", methods=['GET', 'POST'])
def output():
    name = request.form.get('name')
    email= request.form.get('email')
    mobile = request.form.get('mobile')
    return render_template('output.html', name=name, email=email, mobile=mobile)
if __name__ == "__main__":
    app.run(debug=True, port=8080)
