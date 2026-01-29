from fastapi import APIRouter
from pyexpat import features
import joblib
from mysite.database.schema import HousePredictSchema


scaler = joblib.load('scaler.pkl')
model = joblib.load('model.pkl')

predict_router = APIRouter(prefix='/predict', tags=['Predict'])

@predict_router.post('/')
async def predict(data: HousePredictSchema):
    data = data.dict()
    new_nei = data.pop('Neighborhood')

    nei = [
        1 if new_nei == 'Blueste' else 0,
        1 if new_nei == 'BrDale' else 0,
        1 if new_nei == 'BrkSide' else 0,
        1 if new_nei == 'ClearCr' else 0,
        1 if new_nei == 'CollgCr' else 0,
        1 if new_nei == 'Crawfor' else 0,
        1 if new_nei == 'Edwards' else 0,
        1 if new_nei == 'Gilbert' else 0,
        1 if new_nei == 'IDOTRR' else 0,
        1 if new_nei == 'MeadowV' else 0,
        1 if new_nei == 'Mitchel' else 0,
        1 if new_nei == 'NAmes' else 0,
        1 if new_nei == 'NPkVill' else 0,
        1 if new_nei == 'NWAmes' else 0,
        1 if new_nei == 'NoRidge' else 0,
        1 if new_nei == 'NridgHt' else 0,
        1 if new_nei == 'OldTown' else 0,
        1 if new_nei == 'SWISU' else 0,
        1 if new_nei == 'Sawyer' else 0,
        1 if new_nei == 'SawyerW' else 0,
        1 if new_nei == 'Somerst' else 0,
        1 if new_nei == 'StoneBr' else 0,
        1 if new_nei == 'Timber' else 0,
        1 if new_nei == 'Veenker' else 0,
    ]

    something = list(data.values()) + nei
    scaled_data = scaler.transform([something])
    prediction = model.predict(scaled_data)[0]

    return {'Price': round(prediction,2)}