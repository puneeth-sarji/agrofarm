# AgroFarm - Smart Agriculture Platform

AgroFarm is an AI-powered agriculture platform that helps farmers make data-driven decisions about crop selection and plant disease management.

## Quick Start Guide 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/agrofarm.git
cd agrofarm
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

#### Backend Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

#### Frontend Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install
```

### 4. Start the Application

#### Start Backend Server
```bash
# In the root directory
uvicorn main:app --reload --port 8000
```
The backend will be running at: http://localhost:8000

#### Start Frontend Development Server
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start the development server
npm start
```
The frontend will automatically open in your browser at: http://localhost:3001

### 5. Using the Application

1. **Disease Detection**:
   - Go to the Disease Detection tab
   - Upload a plant image (JPEG/PNG, max 5MB)
   - View disease detection results and recommendations

2. **Crop Recommendation**:
   - Navigate to Crop Recommendation tab
   - Enter soil parameters:
     - Nitrogen (0-200)
     - Phosphorus (0-200)
     - Potassium (0-200)
     - pH (0-14)
     - Rainfall (0-500)
   - Click "Get Recommendation"
   - View recommended crops and alternatives

3. **Soil Health Tips**:
   - Check the Soil Health tab
   - Browse expert tips and best practices

4. **Crop Calendar**:
   - View the Crop Calendar tab
   - See seasonal crop information

### 6. Troubleshooting

1. **Backend Issues**:
   ```bash
   # Check if port 8000 is in use
   lsof -i :8000
   # Kill process if needed
   kill -9 <PID>
   ```

2. **Frontend Issues**:
   ```bash
   # Clear npm cache
   npm cache clean --force
   # Reinstall dependencies
   rm -rf node_modules
   npm install
   ```

3. **Image Upload Issues**:
   - Ensure image is JPEG/PNG
   - Check file size (max 5MB)
   - Verify backend server is running

4. **Database Issues**:
   - Check database connection
   - Verify environment variables

### 7. Development Mode

For development, run both servers in development mode:

```bash
# Terminal 1 - Backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

This enables:
- Hot reloading for both frontend and backend
- Debug logging
- Development error messages

## Features

### 1. Disease Detection 
- Upload plant images to detect diseases
- Supports common plant diseases:
  - Early Blight
  - Late Blight
  - Leaf Spot
  - Powdery Mildew
- Get confidence scores and treatment recommendations
- Supports JPEG and PNG images up to 5MB

### 2. Crop Recommendation 
- Input soil parameters:
  - Nitrogen (0-200)
  - Phosphorus (0-200)
  - Potassium (0-200)
  - pH (0-14)
  - Rainfall (0-500)
- Get personalized crop recommendations
- View alternative crop suggestions
- Receive soil health analysis

### 3. Soil Health Tips 
- Access expert agricultural advice
- Learn best practices for soil maintenance
- Get seasonal farming tips

### 4. Crop Calendar 
- View seasonal crop information
- Three main seasons:
  - Kharif (June-October)
  - Rabi (November-March)
  - Zaid (March-June)
- Rainfall requirement guidance

## Technology Stack

### Frontend
- React.js
- Material-UI
- Axios for API calls
- Responsive design

### Backend
- FastAPI
- Python 3.8+
- PIL for image processing
- NumPy for numerical operations

## Setup

### Prerequisites
```bash
# Python 3.8+ required
python -m pip install --upgrade pip
```

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## API Endpoints

### Disease Detection
```
POST /detect-disease
Content-Type: multipart/form-data
```

### Crop Recommendation
```
POST /recommend-crop
Content-Type: application/x-www-form-urlencoded
```

### Soil Health Tips
```
GET /soil-health-tips
```

### Crop Calendar
```
GET /crop-calendar
```

## Development

### File Structure
```
├── main.py           # FastAPI application
├── ml_models.py      # ML model implementations
├── requirements.txt  # Python dependencies
└── frontend/        # React frontend
    ├── src/
    ├── public/
    └── package.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - Feel free to use and modify for your needs.

## Support

For support, please open an issue in the repository or contact the development team.
