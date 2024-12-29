import os
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import json
import re
import fnmatch
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

max_hours = 1
year = 'first yr'

prn = ""

CORS(app)  # Enable CORS for all routes



def parse_duration(duration):
    """Converts an ISO 8601 duration string to total hours."""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        return hours + minutes / 60 + seconds / 3600
    else:
        return 0


def calculate_weight(hrs, yr):
    # Define the thresholds for each yr
    year_thresholds = {
        'first year': 4,  # 6 hours
        'second year': 3,  # 5 hours
        'third year': 2,  # 4 hours
        'fourth year': 1  # 3 hours
    }

    weight = (hrs + year_thresholds[yr])
    return weight
    #  2 3 4 5 6 7
    #  2         7
    #  3         8
    #  4         9
    #  5         10


def filter_records_within_subtopic(df_group, hrs, yr):
    weight = calculate_weight(hrs, yr)
    print(f"WEIGHT: {weight}")
    # Sort records by duration and select the one closest to the weight
    # df_group['WeightDifference'] = (df_group['DurationHours'] - weight).abs()  # Calculate weight difference
    # print(df_group[['DurationHours', 'WeightDifference']])
    # closest_record = df_group.iloc[df_group['WeightDifference'].argsort()[:1]]

    if 2 <= weight <= 3:
        # return df_group.iloc[df_group['DurationHours'].argsort()[:1]]
        position = 1  # Specify the position you want to choose (e.g., 5)
        return df_group.iloc[df_group['DurationHours'].argsort()[position - 1:position]]

    elif 4 <= weight <= 5:
        # return df_group.sort_values(by='DurationHours').head(2)
        # return df_group.iloc[df_group['DurationHours'].argsort()[:1]]
        position = 2  # Specify the position you want to choose (e.g., 5)
        return df_group.iloc[df_group['DurationHours'].argsort()[position - 1:position]]

    elif 6 <= weight <= 7:
        # return df_group.sort_values(by='DurationHours').head(3)
        # return df_group.iloc[df_group['DurationHours'].argsort()[:1]]
        position = 3  # Specify the position you want to choose (e.g., 5)
        return df_group.iloc[df_group['DurationHours'].argsort()[position - 1:position]]

    elif 8 <= weight <= 9:
        # return df_group.sort_values(by='DurationHours').head(4)
        # return df_group.iloc[df_group['DurationHours'].argsort()[:1]]
        position = 4  # Specify the position you want to choose (e.g., 5)
        return df_group.iloc[df_group['DurationHours'].argsort()[position - 1:position]]

    elif 10 <= weight <= 11:
        # return df_group.sort_values(by='DurationHours').head(5)
        # return df_group.iloc[df_group['DurationHours'].argsort()[:1]]
        position = 5  # Specify the position you want to choose (e.g., 5)
        return df_group.iloc[df_group['DurationHours'].argsort()[position - 1:position]]


def process_excel_file(hr, yr, topic, prn):
    if topic == "machine_learning":
        df = pd.read_excel("./static/Machine_Learning_Roadmap.xlsx")
    elif topic == "cloudcomputing":
        df = pd.read_excel("./static/Cloud_Computing_roadmap.xlsx")
    elif topic == "blockchain":
        df = pd.read_excel("./static/Blockchain_roadmap.xlsx")

    # Parse the Duration column to total hours
    df['DurationHours'] = df['Duration'].apply(parse_duration)

    df.to_excel(prn + '_records_with_duration.xlsx', index=False)

    # Group DataFrame by 'Subtopic' column and filter records within each group
    selected_records = df.groupby('Subtopic').apply(filter_records_within_subtopic, hrs=hr, yr=yr)

    # Reset index to remove groupby indices
    selected_records.reset_index(drop=True, inplace=True)

    # Save the selected records to a new Excel file
    selected_records.to_excel(prn + "_selected_records3.xlsx", index=False)

    # Load the selected records from the new Excel file
    selected_df = pd.read_excel(prn + "_selected_records3.xlsx")

    # Order the records by 'Main Topic' column
    ordered_df = selected_df.sort_values(by='Main Topic')

    # Convert the ordered records to the specified JSON format
    json_data = [
        {"label": row['Title'], "link": row['URL']}
        for _, row in ordered_df.iterrows()
    ]

    # Save the JSON data to a file
    with open("./static/" + prn + "_items.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)


@app.route('/createprofile')
def create_profile():
    username = request.args.get('username')
    return render_template('EduPlusCampus.html', username=username)


@app.route('/')
def index():
    # if prn in
    files = os.listdir("./static")

    # Iterate through each file
    for file in files:
        # Check if the file name contains the given prn
        if fnmatch.fnmatch(file, f'*{prn}*'):
            return render_template('tabular_flowchart.html')
    return render_template('index.html')

@app.route('/get_username', methods=['POST'])
def get_username():
    data = request.get_json()
    global prn
    prn = data.get('username')
    print(prn)

@app.route('/dflowchart')
def dflowchart():
    return render_template('diagram_flowchart.html')


@app.route('/tflowchart')
def tflowchart():
    return render_template('tabular_flowchart.html')


@app.route('/home')
def home():
    return render_template('EduPlusCampus.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/redo')
def redo():
    return render_template('index.html')



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        field_of_study = request.form['field_of_study']
        year_of_study = request.form['year_of_study']
        daily_hours = int(request.form['daily_hours'])
        cgpa = request.form['cgpa']
        hrs = daily_hours
        yr = year_of_study

        if float(cgpa) < 6.0:
            daily_hours += 2
        elif 6.0 < float(cgpa) < 8.0:
            daily_hours += 1
        else:
            daily_hours -= 1

        print(f"THE MAX HOURS ARE: {hrs} AND THE YEAR IS {yr}")
        process_excel_file(hr=hrs,
                           yr=yr, topic=field_of_study,
                           prn=prn)  # Process the Excel file and generate JSON data before starting the server

        return render_template('tabular_flowchart.html', field_of_study=field_of_study, year_of_study=year_of_study,
                               daily_hours=daily_hours, cgpa=cgpa)


@app.route('/items.json')
def get_items_json():
    return send_from_directory('static', prn + '_items.json')


def map_data(filtered_recommendations):
    links_file_name = "./static/links.csv"
    links_file = pd.read_csv(links_file_name)
    filtered_df = []
    for filtered_recommendation in filtered_recommendations:
        filtered_df += [links_file[links_file['sno'].isin(filtered_recommendation['sno'].values)][['name', 'url']]]

    return filtered_df


def retrieve_item(field_of_study, year_of_study, daily_hours, cgpa):
    items = []
    for i in range(1, daily_hours + 1):
        lower_limit = 90 // i

        items.append(pd.DataFrame({'time': [daily_hours], 'stage': [1], 'priority': [lower_limit]}))
        items.append(pd.DataFrame({'time': [daily_hours], 'stage': [2], 'priority': [lower_limit]}))
        items.append(pd.DataFrame({'time': [daily_hours], 'stage': [3], 'priority': [lower_limit]}))
        items.append(pd.DataFrame({'time': [daily_hours], 'stage': [4], 'priority': [lower_limit]}))

    return items


def get_recommendations(df, items):
    numeric_features = df[['time', 'stage', 'priority']]
    filtered_recommendations = []
    top_n_instances_new = pd.DataFrame(columns=['time', 'stage', 'priority'])
    for new_item in items:
        scaler = StandardScaler()
        numeric_features_scaled = scaler.fit_transform(numeric_features)
        new_item_scaled = scaler.transform(new_item)

        # Calculate cosine similarity between the new item and existing instances
        cosine_similarities_new = cosine_similarity(new_item_scaled, numeric_features_scaled)

        # Find indices of the most similar instances
        similar_indices_new = cosine_similarities_new.argsort()[0][::-1]

        # Select the top N similar instances
        N = 5  # Adjust as needed

        top_n_instances_new = pd.concat([top_n_instances_new, df.iloc[similar_indices_new[:N]]], ignore_index=True)

    filtered_recommendations += [top_n_instances_new[top_n_instances_new['stage'] == 1]]
    filtered_recommendations += [top_n_instances_new[top_n_instances_new['stage'] == 2]]
    filtered_recommendations += [top_n_instances_new[top_n_instances_new['stage'] == 3]]
    filtered_recommendations += [top_n_instances_new[top_n_instances_new['stage'] == 4]]

    return filtered_recommendations


def create_json(filtered_dfs):
    json_file_path = './static/items.json'
    all_items = []

    for filtered_df in filtered_dfs:
        items = filtered_df.to_dict(orient='records')
        # Rename columns to match JSON format
        for item in items:
            item['label'] = item.pop('name')
            item['link'] = item.pop('url')

        all_items.extend(items)

    with open(json_file_path, 'w') as json_file:
        json.dump(all_items, json_file, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
