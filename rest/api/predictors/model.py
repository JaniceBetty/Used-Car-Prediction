import pandas as pd
import joblib
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
MODEL_DIR = os.path.join(BASE_DIR, 'saved_models')

MODEL_NAMES = [
    'LinearRegression',
    'DecisionTreeRegressor',
    'RandomForestRegressor',
    'Ridge',
    'Lasso'
]

def predict_price(input_data: dict) -> dict:
    """
    Accepts raw input data (dict), returns predicted prices.
    """
    # Construct feature vector
    df = pd.DataFrame([{
        'vehicle_age': input_data['vehicle_age'],
        'km_driven': input_data['km_driven'],
        'mileage': input_data['mileage'],
        'engine': input_data['engine'],
        'max_power': input_data['max_power'],
        'seats': input_data['seats'],
        'seller_type_Dealer': 1 if input_data['seller_type'] == 'dealer' else 0,
        'seller_type_Individual': 1 if input_data['seller_type'] == 'individual' else 0,
        'seller_type_Trustmark Dealer': 1 if input_data['seller_type'] == 'trusted' else 0,
        'fuel_type_CNG': 1 if input_data['fuel_type'] == 'cng' else 0,
        'fuel_type_Diesel': 1 if input_data['fuel_type'] == 'diesel' else 0,
        'fuel_type_Electric': 1 if input_data['fuel_type'] == 'electric' else 0,
        'fuel_type_LPG': 1 if input_data['fuel_type'] == 'lpg' else 0,
        'fuel_type_Petrol': 1 if input_data['fuel_type'] == 'petrol' else 0,
        'transmission_type_Automatic': 1 if input_data['transmission_type'] == 'automatic' else 0,
        'transmission_type_Manual': 1 if input_data['transmission_type'] == 'manual' else 0,
    }])

    valid_predictions = {}

    for model_name in MODEL_NAMES:
        model_file = os.path.join(MODEL_DIR, f"{model_name}_model.pkl")
        if os.path.exists(model_file):
            model = joblib.load(model_file)
            try:
                pred = model.predict(df)[0]
                if pred > 0:
                    valid_predictions[model_name] = pred
            except Exception:
                continue

    if valid_predictions:
        optimal = sum(valid_predictions.values()) / len(valid_predictions)
        return {
            "min_price": int(optimal * 0.9),
            "max_price": int(optimal * 1.1),
            "optimal_price": int(optimal),
            "used_models": valid_predictions
        }

    raise ValueError("No valid predictions")