# HDI Well-Being Predictor

A simple web application that predicts a country’s Human Development Index (HDI) category using four key indicators:

- Life expectancy
- Mean years of schooling
- Expected years of schooling
- GNI per capita (PPP)

The app classifies countries into four tiers:

- Very High
- High
- Medium
- Low

## Project Overview

This project demonstrates how human development can be evaluated using a composite scoring approach inspired by the real-world HDI framework. It combines health, education, and income factors to estimate overall development status.

## Features

- Interactive form for entering HDI-related indicators
- Three built-in scenarios matching the project prompt:
  - Very High human development
  - Medium development level
  - Low development level
- Backend prediction endpoint that returns the HDI score and category
- Clean web interface for viewing prediction results

## Project Files

- app.py — Python server that serves the app and handles prediction requests
- index.html — Main web page layout
- styles.css — Styling for the UI
- script.js — Frontend logic for form handling and scenario loading

## How to Run

1. Open a terminal in the project folder.
2. Start the server:

   ```bash
   python3 app.py
   ```

3. Open your browser and visit:

   ```text
   http://127.0.0.1:8000/
   ```

## Prediction Logic

The predictor uses a simplified scoring model:

- Health is based on life expectancy
- Education combines mean years and expected years of schooling
- Income is derived from GNI per capita using a logarithmic scale

These component scores are combined into an overall score, which is then mapped to a development category.

## Example Use Cases

- Predict a Very High HDI profile for a country with strong health, education, and income indicators
- Identify Medium development gaps in an emerging economy
- Assess Low-development countries needing intervention

## Notes

This is a simplified educational implementation and not a replacement for the official UN HDI methodology.
