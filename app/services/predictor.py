from app.models.state import ml_models


def run_inference(features):

    predictions = ml_models["pipeline"].predict(features)

    probabilities = ml_models["pipeline"].predict_proba(features)

    return predictions, probabilities