from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from ml_models import PlantDiseaseModel, CropRecommender
import io
import json
import numpy as np
from PIL import Image
import imghdr
from datetime import datetime

app = FastAPI(title="AI Agriculture Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
plant_disease_model = PlantDiseaseModel()
crop_recommender = CropRecommender()

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agriculture Platform API"}

@app.post("/detect-disease")
async def detect_disease(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG or PNG)"
            )
        
        # Read image file
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )
        
        # Get prediction from model
        try:
            image = Image.open(io.BytesIO(contents))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            result = plant_disease_model.predict(image)
            return result
        except ValueError as ve:
            raise HTTPException(
                status_code=400,
                detail=str(ve)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing image: {str(e)}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )

@app.post("/recommend-crop")
async def recommend_crop(
    nitrogen: float = Form(...),
    phosphorus: float = Form(...),
    potassium: float = Form(...),
    ph: float = Form(...),
    rainfall: float = Form(...)
):
    try:
        # Validate input ranges
        if not (0 <= nitrogen <= 200):
            raise HTTPException(status_code=400, detail="Nitrogen should be between 0 and 200")
        if not (0 <= phosphorus <= 200):
            raise HTTPException(status_code=400, detail="Phosphorus should be between 0 and 200")
        if not (0 <= potassium <= 200):
            raise HTTPException(status_code=400, detail="Potassium should be between 0 and 200")
        if not (0 <= ph <= 14):
            raise HTTPException(status_code=400, detail="pH should be between 0 and 14")
        if not (0 <= rainfall <= 500):
            raise HTTPException(status_code=400, detail="Rainfall should be between 0 and 500")

        # Create soil data dictionary
        soil_data = {
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph,
            "rainfall": rainfall
        }
        
        # Get recommendation from model
        result = crop_recommender.predict(soil_data)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in recommend_crop: {str(e)}")  # Add debugging
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/soil-health-tips")
async def get_soil_health_tips():
    tips = [
        "Maintain proper soil pH between 6.0 and 7.0 for most crops",
        "Add organic matter to improve soil structure and fertility",
        "Practice crop rotation to prevent nutrient depletion",
        "Use cover crops to protect soil during off-seasons",
        "Test soil regularly to monitor nutrient levels",
        "Avoid over-tilling to maintain soil structure",
        "Implement proper drainage to prevent waterlogging",
        "Use mulch to retain moisture and suppress weeds",
        "Apply balanced fertilizers based on soil test results",
        "Maintain adequate soil moisture through proper irrigation"
    ]
    return {"tips": tips}

@app.get("/crop-calendar")
async def get_crop_calendar():
    calendar_data = {
        "current_season": "Kharif" if datetime.now().month in [6,7,8,9,10] else "Rabi" if datetime.now().month in [11,12,1,2,3] else "Zaid",
        "seasons": [
            {
                "name": "Kharif",
                "months": "June-October",
                "crops": ["Rice", "Maize", "Soybean", "Cotton"],
                "rainfall_requirement": "High"
            },
            {
                "name": "Rabi",
                "months": "November-March",
                "crops": ["Wheat", "Barley", "Peas", "Mustard"],
                "rainfall_requirement": "Moderate"
            },
            {
                "name": "Zaid",
                "months": "March-June",
                "crops": ["Watermelon", "Muskmelon", "Cucumber"],
                "rainfall_requirement": "Low"
            }
        ]
    }
    return calendar_data
