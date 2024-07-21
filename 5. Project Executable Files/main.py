import pickle
from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model
model1 = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if request.method == 'POST':
            quarter = float(request.form['Quarter'])

            department = request.form['Department']
            if department.lower() == 'sewing':
                department = 1.0
            elif department.lower() == 'finishing':
                department = 0.0
            else:
                return render_template('index.html', prediction_text="Invalid department")

            day = request.form['Day of the week']
            days_map = {
                'Monday': 0.0, 'Tuesday': 4.0, 'Wednesday': 5.0,
                'Thursday': 3.0, 'Saturday': 1.0, 'Sunday': 2.0
            }
            if day not in days_map:
                return render_template('index.html', prediction_text="Invalid day")
            day = days_map[day]

            team = float(request.form['Team Number'])
            time = float(request.form['Time Allocated'])
            items = float(request.form['Unfinished Items'])
            over_time = float(request.form['Over Time'])
            incentive = float(request.form['Incentive'])
            idle_time = float(request.form['Idle Time'])
            idle_men = float(request.form['Idle Men'])
            style = float(request.form['Style Change'])
            workers = float(request.form['Number of Workers'])

            prediction = model1.predict(pd.DataFrame([[quarter, department, day, team, time, items, over_time, incentive, idle_time, idle_men, style, workers]], columns=[
                'quarter', 'department', 'day', 'team_number', 'time_allocated', 'unfinished_items',
                'over_time', 'incentive', 'idle_time', 'idle_men', 'style_change', 'no_of_workers'
            ]))

            prediction = (np.round(prediction, 4)) * 100

            return render_template('index.html', prediction_text="Prediction is {}".format(prediction))

        return render_template('index.html')

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
