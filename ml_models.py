import torch
import torch.nn as nn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from torchvision import models, transforms
import joblib
import os
from PIL import Image
import io

class PlantDiseaseModel:
    def __init__(self):
        self.classes = [
            "Healthy",
            "Early Blight",
            "Late Blight",
            "Leaf Spot",
            "Powdery Mildew"
        ]

    def predict(self, image_data):
        try:
            # Open and validate the image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            elif isinstance(image_data, Image.Image):
                image = image_data
            else:
                raise ValueError("Invalid image format")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to standard size
            image = image.resize((224, 224))
            
            # Mock model prediction
            disease_idx = np.random.randint(0, len(self.classes))
            confidence = np.random.uniform(0.7, 0.99)
            
            # Get recommendations
            disease = self.classes[disease_idx]
            recommendations = self.get_recommendations(disease)
            
            return {
                "disease": disease,
                "confidence": float(confidence),
                "recommendations": recommendations,
                "image_info": {
                    "size": image.size,
                    "mode": image.mode,
                    "format": image.format or "Unknown"
                }
            }
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

    def get_recommendations(self, disease):
        recommendations = {
            "Healthy": [
                "Continue current practices",
                "Monitor regularly for any signs of disease",
                "Maintain good air circulation"
            ],
            "Early Blight": [
                "Remove infected leaves",
                "Apply fungicide",
                "Improve air circulation",
                "Avoid overhead watering"
            ],
            "Late Blight": [
                "Remove and destroy infected plants",
                "Apply copper-based fungicide",
                "Improve drainage",
                "Space plants properly"
            ],
            "Leaf Spot": [
                "Remove infected leaves",
                "Apply appropriate fungicide",
                "Avoid overhead watering",
                "Maintain proper spacing"
            ],
            "Powdery Mildew": [
                "Improve air circulation",
                "Apply sulfur-based fungicide",
                "Remove infected parts",
                "Water at base of plants"
            ]
        }
        return recommendations.get(disease, ["Consult a local agricultural expert"])

class CropRecommender:
    def __init__(self):
        self.crops = [
            "Rice", "Wheat", "Maize", "Sugarcane", "Cotton",
            "Groundnut", "Pulses", "Potato", "Tomato", "Soybean"
        ]
        
        # Optimal ranges for each parameter
        self.optimal_ranges = {
            "Rice": {"nitrogen": (60, 100), "phosphorus": (40, 80), "potassium": (40, 80), "ph": (5.5, 6.5), "rainfall": (150, 300)},
            "Wheat": {"nitrogen": (100, 140), "phosphorus": (50, 90), "potassium": (50, 90), "ph": (6.0, 7.0), "rainfall": (75, 150)},
            "Maize": {"nitrogen": (80, 120), "phosphorus": (40, 70), "potassium": (30, 60), "ph": (5.8, 7.0), "rainfall": (100, 200)},
            "Sugarcane": {"nitrogen": (120, 160), "phosphorus": (60, 100), "potassium": (60, 100), "ph": (6.0, 7.5), "rainfall": (150, 250)},
            "Cotton": {"nitrogen": (80, 120), "phosphorus": (30, 60), "potassium": (40, 80), "ph": (6.0, 7.5), "rainfall": (100, 180)},
            "Groundnut": {"nitrogen": (40, 80), "phosphorus": (30, 60), "potassium": (30, 60), "ph": (6.0, 6.5), "rainfall": (80, 120)},
            "Pulses": {"nitrogen": (30, 60), "phosphorus": (40, 70), "potassium": (30, 50), "ph": (6.0, 7.0), "rainfall": (80, 150)},
            "Potato": {"nitrogen": (100, 140), "phosphorus": (50, 80), "potassium": (50, 90), "ph": (5.5, 6.5), "rainfall": (100, 180)},
            "Tomato": {"nitrogen": (80, 120), "phosphorus": (40, 80), "potassium": (40, 80), "ph": (6.0, 7.0), "rainfall": (80, 150)},
            "Soybean": {"nitrogen": (50, 90), "phosphorus": (40, 70), "potassium": (40, 70), "ph": (6.0, 7.0), "rainfall": (100, 180)}
        }

    def calculate_crop_score(self, soil_data, crop):
        ranges = self.optimal_ranges[crop]
        scores = []
        
        # Calculate score for each parameter
        for param, (min_val, max_val) in ranges.items():
            value = float(soil_data[param])  # Use the exact parameter name
            if min_val <= value <= max_val:
                score = 1.0
            else:
                # Calculate distance from optimal range
                distance = min(abs(value - min_val), abs(value - max_val))
                max_distance = (max_val - min_val)
                score = max(0, 1 - (distance / max_distance))
            scores.append(score)
        
        # Return average score
        return np.mean(scores)

    def predict(self, soil_data):
        try:
            crop_scores = []
            for crop in self.crops:
                score = self.calculate_crop_score(soil_data, crop)
                crop_scores.append((crop, score))
            
            # Sort by score in descending order
            crop_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get best crop and its confidence
            best_crop, best_score = crop_scores[0]
            
            # Get alternative crops (next 3 best options)
            alternative_crops = [
                {"crop": crop, "confidence": float(score)}
                for crop, score in crop_scores[1:4]
            ]
            
            # Calculate soil health scores
            parameter_scores = self.calculate_soil_health_scores(soil_data)
            
            return {
                "recommended_crop": best_crop,
                "confidence": float(best_score),
                "alternative_crops": alternative_crops,
                "soil_health": {
                    "overall_score": int(np.mean(list(parameter_scores.values()))),
                    "parameter_scores": parameter_scores,
                    "recommendations": self.get_soil_recommendations(parameter_scores)
                }
            }
        except Exception as e:
            print(f"Error in predict: {str(e)}")
            raise

    def calculate_soil_health_scores(self, soil_data):
        scores = {}
        
        # Nitrogen (N) score
        n_value = float(soil_data["nitrogen"])
        if n_value < 30:
            scores["nitrogen"] = int(n_value / 30 * 100)
        elif n_value > 160:
            scores["nitrogen"] = int(100 - ((n_value - 160) / 160 * 100))
        else:
            scores["nitrogen"] = 100
            
        # Phosphorus (P) score
        p_value = float(soil_data["phosphorus"])
        if p_value < 30:
            scores["phosphorus"] = int(p_value / 30 * 100)
        elif p_value > 100:
            scores["phosphorus"] = int(100 - ((p_value - 100) / 100 * 100))
        else:
            scores["phosphorus"] = 100
            
        # Potassium (K) score
        k_value = float(soil_data["potassium"])
        if k_value < 30:
            scores["potassium"] = int(k_value / 30 * 100)
        elif k_value > 100:
            scores["potassium"] = int(100 - ((k_value - 100) / 100 * 100))
        else:
            scores["potassium"] = 100
            
        # pH score
        ph_value = float(soil_data["ph"])
        if ph_value < 5.5:
            scores["ph"] = int((ph_value / 5.5) * 100)
        elif ph_value > 7.5:
            scores["ph"] = int((1 - (ph_value - 7.5) / 7.5) * 100)
        else:
            scores["ph"] = 100
            
        # Rainfall score
        rainfall = float(soil_data["rainfall"])
        if rainfall < 75:
            scores["rainfall"] = int(rainfall / 75 * 100)
        elif rainfall > 300:
            scores["rainfall"] = int(100 - ((rainfall - 300) / 300 * 100))
        else:
            scores["rainfall"] = 100
            
        return scores

    def get_soil_recommendations(self, parameter_scores):
        recommendations = []
        
        if parameter_scores["nitrogen"] < 70:
            recommendations.append("Add nitrogen-rich fertilizers or organic matter like manure")
            
        if parameter_scores["phosphorus"] < 70:
            recommendations.append("Apply phosphate fertilizers or bone meal")
            
        if parameter_scores["potassium"] < 70:
            recommendations.append("Use potash fertilizers or add wood ash")
            
        if parameter_scores["ph"] < 70:
            recommendations.append("Adjust soil pH using lime (if acidic) or sulfur (if alkaline)")
            
        if parameter_scores["rainfall"] < 70:
            recommendations.append("Consider irrigation or drought-resistant crops")
            
        return recommendations

def get_soil_health_score(soil_data):
    """Calculate soil health score based on parameters"""
    try:
        n, p, k, ph, rainfall = soil_data[0]
        
        # Define ideal ranges
        ideal_ranges = {
            'N': (50, 100),
            'P': (40, 80),
            'K': (35, 70),
            'pH': (6.0, 7.5),
            'rainfall': (750, 1500)
        }
        
        # Calculate scores for each parameter
        scores = {
            'N': 1 - min(abs(n - np.mean(ideal_ranges['N'])) / (ideal_ranges['N'][1] - ideal_ranges['N'][0]), 1),
            'P': 1 - min(abs(p - np.mean(ideal_ranges['P'])) / (ideal_ranges['P'][1] - ideal_ranges['P'][0]), 1),
            'K': 1 - min(abs(k - np.mean(ideal_ranges['K'])) / (ideal_ranges['K'][1] - ideal_ranges['K'][0]), 1),
            'pH': 1 - min(abs(ph - np.mean(ideal_ranges['pH'])) / (ideal_ranges['pH'][1] - ideal_ranges['pH'][0]), 1),
            'rainfall': 1 - min(abs(rainfall - np.mean(ideal_ranges['rainfall'])) / (ideal_ranges['rainfall'][1] - ideal_ranges['rainfall'][0]), 1)
        }
        
        # Calculate overall score
        overall_score = np.mean(list(scores.values())) * 100
        
        return {
            "overall_score": round(overall_score, 2),
            "parameter_scores": {k: round(v * 100, 2) for k, v in scores.items()},
            "recommendations": get_recommendations(scores)
        }
    except Exception as e:
        return {"error": str(e)}

def get_recommendations(scores):
    """Generate recommendations based on soil parameter scores"""
    recommendations = []
    
    if scores['N'] < 0.6:
        recommendations.append("Add nitrogen-rich fertilizers or plant nitrogen-fixing cover crops")
    if scores['P'] < 0.6:
        recommendations.append("Incorporate phosphorus-rich organic matter or rock phosphate")
    if scores['K'] < 0.6:
        recommendations.append("Add potassium-rich compost or wood ash")
    if scores['pH'] < 0.6:
        recommendations.append("Adjust soil pH using lime or sulfur based on specific needs")
    if scores['rainfall'] < 0.6:
        recommendations.append("Consider irrigation systems or drought-resistant crops")
        
    return recommendations