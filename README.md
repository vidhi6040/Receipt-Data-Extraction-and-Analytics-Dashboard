# Receipt Data Pipeline and Sales Analysis

## Overview
This project processes raw retail receipt files and converts them into structured JSON data for analysis.
A Python-based ETL pipeline extracts useful information from receipt text files and prepares the dataset for visualization.
The processed data is then analyzed using a Power BI dashboard to generate insights.

## Dataset
The original dataset contains **15,000+ raw receipt files**.
Only a small sample is included in this repository to keep it lightweight.

## Workflow
1. Raw receipt files are stored in the `raw_receipts` folder.
2. Python scripts in `src` extract information using regular expressions.
3. The extracted data is converted into JSON format.
4. The processed data is used for analysis in Power BI.

## Technologies Used
* Python
* Regular Expressions (Regex)
* JSON
* Power BI

## Project Structure
* `src` – Python scripts for data processing
* `raw_receipts` – Sample raw receipt files
* `json_receipts` – Processed receipt data in JSON format
* `dashboard` – Power BI dashboard for visualization
