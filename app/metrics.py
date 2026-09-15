from prometheus_client import Counter

# Tracks every successful prediction, broken down by which species
# was predicted and which API version served the request. This is an
# ML-specific metric the generic instrumentator has no way of knowing
# about on its own.
prediction_counter = Counter(
    
    "ml_predictions_total",
    
    "Total number of successful predictions made",
    
    ["predicted_class", "model_version"],
    
)