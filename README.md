# Project Title: predict_pm2.5

## Description
This repository contains a machine learning pipeline for predicting PM2.5 air quality using historical data. It includes code for data preprocessing, model training, and a Dash application for visualizing predictions.

## Getting Started
1. **Clone the repository:**
    ```bash
    git clone https://github.com/jayjiratta/predict_pm2.5.git
    ```
2. **Install dependencies:**
    Create a virtual environment (recommended) and install the required packages using the provided requirements.txt file:
    ```bash
    pip install -r requirements.txt
    ```

3. **Preprocess data and train model:**
    Run the provided Jupyter Notebook (`predict_PM10.ipynb`) and (`predict_PM25.ipynb`) to preprocess data, train the machine learning model, and save it to a file (`pkl`). This step might take some time depending on your dataset size and computing resources.

    Note: Due to file size limitations on GitHub, the pre-trained model is not included. Running the notebook is necessary to generate the model.

4. **Run the Dash app:**
    Navigate to the project directory and execute the Python script:
    ```bash
    python app.py
    ```
    This will launch the Dash application in your web browser, typically at http://127.0.0.1:8050/.

## Usage
The Dash application allows you to visualize PM2.5 predictions for Trang and date start at 2024-01-01 to 2024-03-09

## Additional Notes
- The machine learning model used in this project 'Extra Trees Regressor' is chosen for its effectiveness in PM2.5 prediction. You can explore other models or fine-tune the current model for potentially better results.
- Consider adding documentation within the Jupyter Notebook and Python script to explain the code, data sources, and assumptions made.
- If you have a public dataset used for training, feel free to include a link or instructions on how to access it.

## Contribution
Pull requests and suggestions are welcome! Feel free to fork the repository and contribute.


