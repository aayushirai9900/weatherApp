import requests
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#creating database using class
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/',methods=['GET','POST'])
def index():
    err_msg=''
    api='d650ef87a375d8e58c05fc7f5a17b3f2'
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    if request.method =='POST':
        new_city=request.form.get('city')
        if new_city:
           existing_city=City.query.filter_by(name=new_city).first()
            

           if not existing_city:
               r=requests.get(url.format(new_city,api)).json()
               if r['cod']==200:    
                    new_city_obj=City(name=new_city)
                    db.session.add(new_city_obj)
                    db.session.commit()
               else:
                    err_msg='not exist in world'
                
           else:
               err_msg='already exist'

    cities=City.query.all()
    
    weather_data=[]
    for city in cities:
        
        rn=requests.get(url.format(city.name,api)).json()
        weather={
            'city':city.name,
            'temperature':rn['main']['temp'],
            'description':rn['weather'][0]['description'],
            'icon':rn['weather'][0]['icon'],
        }
        weather_data.append(weather)
        weather_data.reverse()
         
    return render_template('weather.html',weather_data=weather_data)


@app.route('/delete/<name>/')
def delete_city(name):
    city=City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')

if __name__== "__main__":
    app.run(debug=True)


