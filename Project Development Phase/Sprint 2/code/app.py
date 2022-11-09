from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import requests
from watson_developer_cloud import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



app = Flask(_name_)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ZzORf6jIVK'
app.config['MYSQL_PASSWORD'] = 'e6u31tnYxX'
app.config['MYSQL_DB'] = 'ZzORf6jIVK'
mysql = MySQL(app)
app.secret_key = 'a'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trackfood')
def trackfood():
    return render_template('trackfood.html')
@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        img = request.files['foodimg']
        pathname = './static/'+session['email']+'.jpg'
        img.save(pathname)
        # using ibm watson visualrecognition api to identify the fooditem
        authenticator = IAMAuthenticator(
            '4biolQXfmt25NoJHWtHzlZ-bpbU7p85zrvuzdgI8Tl_W')
        visual_recognition = VisualRecognitionV3(
            version='2018-03-19',
            authenticator=authenticator
        )
        try:
            visual_recognition.set_service_url(
                'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/7024ae63-5bac-4faf-bf7c-17d733db7625')
            with open(pathname, 'rb') as images_file:
                classes = visual_recognition.classify(
                    images_file=images_file,
                    classifier_ids=["food"]).get_result()
            fooditem = classes['images'][0]['classifiers'][0]['classes'][0]['class']
        except:
            return render_template('trackfood.html', msg=0)
        if fooditem.lower() == 'non-food':
            allnutrients = []
            allnutrients.append(fooditem.upper())
            allnutrients.append(0)
            return render_template('trackfood.html', msg=allnutrients)
        else:
            # using usda api to get the nutrients of the food item
            nutrients = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query={}&pageSize={}&api_key={}'.format(
                fooditem, '1', 'vIrQaHQPu9zk57HxLIcUMBlxxcco78tZgg3tHzfW'))
            data = json.loads(nutrients.text)
            nlist =[]
            vlist =[]
            n = int(len(data['foods'][0]['foodNutrients']))
            for i in range(0,n):

                nlist.append(data['foods'][0]['foodNutrients'][i]['nutrientName'])
                vlist.append(str(data['foods'][0]['foodNutrients'][i]['value'])+" "+data['foods'][0]['foodNutrients'][i]['unitName'])
            dic={"nutri": nlist , "value":vlist , "n" : int(n)}
            return render_template('trackfood.html',vlist=vlist, nlist=nlist,n=n,fooditem=fooditem.upper())



if _name_ == '_main_':
    app.run(host='0.0.0.0', debug=True,port=8080)
