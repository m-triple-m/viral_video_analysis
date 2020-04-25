from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from processData import Processor
import json
import plotly
from predict import Predictor


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "$@#%^&%^*(&*&^%4!!"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(20), nullable = True)
    password = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'

db.create_all()
pro = Processor('datasets/INvideos.csv', 'datasets/IN_category_id.json')
predictor = Predictor('models')

@app.route('/')
@app.route('/home')
def home():
    if not session.get('user'):
        return redirect('/signin')
    return render_template('index.html', loggedin = session.get('user'))

@app.route('/signin', methods = ["POST", "GET"])
def Signin():
    
    if request.method == 'POST':
        data = request.form
        
        user = User.query.filter_by(username = data.get('username')).first()
        if user:
            print(user)
            if user.password == data.get('password'):
                print('login success')
                session['user'] = user.username
                return jsonify('success')
                
            else:
                return jsonify('failed')
        else:
            return jsonify('failed')

    return render_template('signin.html')

@app.route('/signup', methods = ["POST", "GET"])
def Signup():
    if request.method == 'POST':
        data = request.form
        user = User(username = data.get('username'), email = data.get('email'), password = data.get('password'))
        db.session.add(user)
        db.session.commit()
        print('data saved!!')
        return jsonify('success')

    return render_template('signup.html')

@app.route('/logout')
def Logout():
    session['user'] = None
    return redirect('/signin')


@app.route('/plot1')
def plot1():
    graphs = []

    data = pro.getVideosData()[:20]
        
    graphs = [dict(x = data['channel_title'], y = data['views'], type = 'bar')]
    print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot2.html', graphJSON = graphJSON)

@app.route('/views')
def Views():
    graphs = []

    data = pro.getVideosData()
        
    graphs = [dict(x = data[data["views"] < 25e5]['views'], type = 'histogram')]
    print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('viewhist.html', graphJSON = graphJSON)

@app.route('/likes')
def Likes():
    graphs = []

    data = pro.getVideosData()
        
    graphs = [dict(x = data[data["likes"] <= 1e4]["likes"], type = 'histogram')]
    print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('likeshist.html', graphJSON = graphJSON)

@app.route('/comments')
def Comments():
    graphs = []

    data = pro.getVideosData()
        
    graphs = [dict(x = data[data["comment_count"] < 30000]["comment_count"], type = 'histogram')]
    print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('commentshist.html', graphJSON = graphJSON)

@app.route('/title')
def Title():
    graphs = []

    data = pro.getTitleLength()
        
    graphs = [dict(x = data['title_length'].values, type = 'histogram')]
    print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('titlehist.html', graphJSON = graphJSON)


@app.route('/title2')
def Title2():
    graphs = []

    data = pro.getTitleLength()
        
    graphs = [dict(x = data['views'].values, y = data['title_length'].values, mode = 'markers', type = 'scatter')]
    # print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('titlescatter.html', graphJSON = graphJSON)

@app.route('/channel')
def ChannelVideos():
    graphs = []

    df = pro.getVideosData()
    data = df.groupby("channel_title").size().reset_index(name="video_count") \
    .sort_values("video_count", ascending=False).head(20)
        
    graphs = [dict(y= data['video_count'].values, x = data['channel_title'].values, 
            type = 'bar')]
    # print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('channel.html', graphJSON = graphJSON)


@app.route('/cate')
def Category():
    graphs = []

    data = pro.getCategoryNames()
    # data = df.groupby("channel_title").size().reset_index(name="video_count") \
    # .sort_values("video_count", ascending=False).head(20)
        
    graphs = [dict(y= data['No_of_videos'].values, x = data["category_name"].values, 
            type = 'bar')]
    # print(graphs)
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('category.html', graphJSON = graphJSON)


@app.route('/predict', methods = ['GET', 'POST'])
def Prediction():
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        prediction_type = request.form.get('prediction')
        data = list(map(int, data))
        data.extend([False, False, False])
        print(data)
        if prediction_type == 'views':
            result = predictor.predictViews(data)
        elif prediction_type == 'likes':
            result = predictor.predictLikes(data)
        elif prediction_type == 'comments':
            result = predictor.predictComments(data)
        else:
            print('invalid request!!!')
            return jsonify([])

        return jsonify(result)
    return render_template('predictview.html')

if __name__ == "__main__":
    app.run(debug=True)