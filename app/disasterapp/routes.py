import json
import pickle
from collections import Counter

import pandas as pd
import plotly
from disasterapp import app
from disasterapp.tokenizer_function import tokenize_only_english
from flask import jsonify, render_template, request
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
from util_scripts import tokenizer_function
from util_scripts.tokenizer_function import Tokenizer, tokenize

MODEL_PATH = "../models/classifier_me.pkl"
DB_PATH = "sqlite:///../data/DisasterResponse.db"


@app.before_first_request
def load_model_data():
    global df
    global model
    # load data

    engine = create_engine(DB_PATH)
    df = pd.read_sql_table("DisasterResponse", engine)
    with open(MODEL_PATH, "rb") as fp:
        model = pickle.load(fp)


# index webpage displays cool visuals and receives user input text for model
@app.route("/")
@app.route("/index")
def index():
    # extract data needed for visuals
    # Message counts of different generes
    genre_counts = df.groupby("genre").count()["message"]
    genre_names = list(genre_counts.index)
    genre_counts = genre_counts.to_list()

    # Message counts for different categories
    cat_counts_df = df.iloc[:, 4:].sum().sort_values(ascending=False)
    cat_counts = list(cat_counts_df)
    cat_names = list(cat_counts_df.index)

    # Top keywords in Social Media in percentages
    social_media_messages = " ".join(df[df["genre"] == "social"]["message"])
    social_media_tokens = tokenize_only_english(social_media_messages)

    # social_media_tokens = tokenize(social_media_messages)
    social_media_wrd_counter = Counter(social_media_tokens).most_common()

    items, counts = zip(*social_media_wrd_counter)
    word_frequency = pd.Series(counts, index=items) / sum(counts) * 100
    social_media_wrds = word_frequency.index[:50].to_list()
    social_media_wrd_pct = word_frequency[:50].to_list()

    # direct_messages = ' '.join(df[df['genre'] == 'direct']['message'])
    #
    # direct_tokens = tokenize_only_english(direct_messages)
    # # social_media_tokens = tokenize(social_media_messages)
    # direct_wrd_counter = Counter(direct_tokens).most_common()
    #
    # items, counts = zip(*direct_wrd_counter)
    # word_frequency = pd.Series(counts, index=items) / sum(counts) * 100
    # direct_wrds = word_frequency.index[:50].to_list()
    # direct_wrd_pct = word_frequency[:50].to_list()

    # Top keywords in Direct in percentages
    direct_messages = " ".join(df[df["genre"] == "direct"]["message"])
    direct_tokens = tokenize(direct_messages)
    direct_wrd_counter = Counter(direct_tokens).most_common()
    direct_wrd_cnt = [i[1] for i in direct_wrd_counter]
    direct_wrd_pct = [i / sum(direct_wrd_cnt) * 100 for i in direct_wrd_cnt]
    direct_wrds = [i[0] for i in direct_wrd_counter]
    # create visuals

    graphs = [
        # Histogram of the message genre
        {
            "data": [Bar(x=genre_names, y=genre_counts)],
            "layout": {
                "title": "Distribution of Message Genres",
                "yaxis": {"title": "Count"},
                "xaxis": {"title": "Genre"},
            },
        },
        # histogram of social media messages top 30 keywords
        {
            "data": [Bar(x=social_media_wrds[:50], y=social_media_wrd_pct[:50])],
            "layout": {
                "title": "Top 50 Keywords in Social Media Messages",
                "xaxis": {"tickangle": 60},
                "yaxis": {"title": "% Total Social Media Messages"},
            },
        },
        # histogram of direct messages top 30 keywords
        {
            "data": [Bar(x=direct_wrds[:50], y=direct_wrd_pct[:50])],
            "layout": {
                "title": "Top 50 Keywords in Direct Messages",
                "xaxis": {"tickangle": 60},
                "yaxis": {"title": "% Total Direct Messages"},
            },
        },
        # histogram of messages categories distributions
        {
            "data": [Bar(x=cat_names, y=cat_counts)],
            "layout": {
                "title": "Distribution of Message Categories",
                "xaxis": {"tickangle": 60},
                "yaxis": {"title": "count"},
            },
        },
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template("master.html", ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route("/go")
def go():
    # save user input in query
    query = request.args.get("query", "")

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file.
    return render_template(
        "go.html", query=query, classification_result=classification_results
    )
