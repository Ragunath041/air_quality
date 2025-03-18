# Air Quality Index Prediction

This application predicts air quality index based on environmental parameters and provides data exploration tools.

## How to Run the Project

### Prerequisites
- Python 3.8 or higher

### Step 1: Setup the Project

### Step 2: Clone the Repository
```
git clone https://github.com/Ragunath041/Air-Quality-index-Prediction.git
cd Air-Quality-index-Prediction
```

### Step 2: Create a Virtual Environment
```
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- Windows:
```
.\venv\Scripts\activate
```
- macOS/Linux:
```
source venv/bin/activate
```

### Step 4: Install Required Packages
```
pip install streamlit streamlit-lottie numpy pandas scikit-learn matplotlib seaborn requests plotly_express pybase64
```

### Step 5: Copy the Required Dataset
```
copy Data\final_data.csv final_data.csv
```
Or for macOS/Linux:
```
cp Data/final_data.csv final_data.csv
```

### Step 6: Train the Model
```
python retrain_model.py
```

### Step 7: Run the Application
```
streamlit run app_fixed.py
```

### Step 8: Access the Application
Open your browser and go to:
```
http://localhost:8501
```

## Using the Application

### Predict Page
- Input values for PM2.5, NO2, CO, SO2, and O3
- Click "Calculate AQI" to see the predicted air quality index
- The result will indicate if the air quality is Good, Satisfactory, Moderate, Poor, or Severe

### Explore Page
- View and analyze the dataset with various visualizations
- Options include Scatterplots, Boxplots, Histograms, Density Contours, and Heatmaps
- Download the dataset for offline analysis

## Project Structure
- `app_fixed.py`: Main application file
- `retrain_model.py`: Script to train the machine learning model
- `model.pkl`: Trained model file
- `final_data.csv`: Dataset for analysis and prediction
- `Data/`: Directory containing original datasets
