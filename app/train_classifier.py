import pickle
import sys

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sqlalchemy import create_engine
from utils import tokenize


def load_data(database_filepath):
    """
        Load data from the sqlite database.
    Args:
        database_filepath: the path of the database file
    Returns:
        X (DataFrame): messages
        Y (DataFrame): One-hot encoded categories
        category_names (List)
    """

    # load data from database
    engine = create_engine("sqlite:///" + database_filepath)
    df = pd.read_sql_table("DisasterResponse", engine)
    X = df["message"]
    Y = df.drop(["id", "message", "original", "genre"], axis=1)
    category_names = Y.columns

    return X, Y, category_names


def build_model():
    """
      build NLP pipeline - count words, tf-idf, multiple output classifier
    Returns:
        the pipeline object
    """
    pipeline = Pipeline(
        [
            ("vec", CountVectorizer(tokenizer=tokenize)),
            ("tfidf", TfidfTransformer()),
            (
                "clf",
                MultiOutputClassifier(
                    RandomForestClassifier(n_estimators=100, n_jobs=-1)
                ),
            ),
        ]
    )

    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """
        Evaluate the model performances, in terms of f1-score, precison and recall
    Args:
        model: the model to be evaluated
        X_test: X_test dataframe
        Y_test: Y_test dataframe
        category_names: category names list defined in load data
    Returns:
        perfomances (DataFrame)
    """
    # predict on the X_test
    y_pred = model.predict(X_test)

    # build classification report on every column
    performances_list = []
    for i in range(len(category_names)):
        performances_list.append(
            [
                f1_score(Y_test.iloc[:, i].values, y_pred[:, i], average="micro"),
                precision_score(
                    Y_test.iloc[:, i].values, y_pred[:, i], average="micro"
                ),
                recall_score(Y_test.iloc[:, i].values, y_pred[:, i], average="micro"),
            ]
        )
    # build dataframe
    performances = pd.DataFrame(
        performances_list,
        columns=["f1 score", "precision", "recall"],
        index=category_names,
    )
    return performances


def save_model(model, model_filepath):
    """
    Save model to pickle
    """
    pickle.dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print("Loading data...\n    DATABASE: {}".format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print("Building model...")
        model = build_model()

        print("Training model...")
        model.fit(X_train, Y_train)

        print("Evaluating model...")
        print(evaluate_model(model, X_test, Y_test, category_names))

        print("Saving model...\n    MODEL: {}".format(model_filepath))
        save_model(model, model_filepath)

        print("Trained model saved!")

    else:
        print(
            "Please provide the filepath of the disaster messages database "
            "as the first argument and the filepath of the pickle file to "
            "save the model to as the second argument."
        )


if __name__ == "__main__":
    main()
