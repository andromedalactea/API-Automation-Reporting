# API-Automation-Reporting

## Overview
This API provides an automated solution for generating and distributing reports. Designed primarily for GreenVestors (GV), it integrates data from a MongoDB database to create comprehensive reports, complete with text and links to Google Drive folders containing relevant images. The system also utilizes Google and Amazon APIs for additional functionalities.

## Features
- **API-Based Automation**: Automates the entire process of report generation.
- **Data Integration**: Pulls data from a MongoDB database based on API call parameters.
- **Image and Link Embedding**: Incorporates images and links from Google Drive into reports.
- **Email Distribution**: Utilizes Amazon SES for email distribution of reports.
- **Archiving**: Saves reports in a designated Google Drive folder and logs their links in a Google Sheet.
- **Flask API Design**: The API is implemented using Flask and deployed via Docker on Google Cloud Run.
- **Scheduled Triggers**: Set to automatically execute at predetermined intervals.

## Main Logic
The `reports_for_gv` function in the API handles the core logic:

- **Parameters**: 
  - `project_list`: A list of project IDs to be included in the report.
  - `for_gv`: A boolean flag to determine if the report is intended for GreenVestors.

- **Process Flow**:
  - Extracts data and filters relevant documents based on project IDs.
  - Downloads and processes images from Google Drive.
  - Generates different types of reports based on project criteria (e.g., bar graphs, pie charts).
  - Fills PDF templates with images, graphs, and text data.
  - Converts images to PDF format for final report generation.
  - Distributes reports via email and updates Google Drive and Sheets for tracking.

- **Tech Stack**: 
  - Languages and Libraries: Python, Flask.
  - Database: MongoDB.
  - Cloud and Deployment: Docker, Google Cloud Run.
  - APIs: Google APIs, Amazon SES.

## Usage
To utilize this API, pass a list of project IDs and a flag indicating if the report is for GV. The API then processes this data, generating and distributing reports accordingly.

## Contributions
Feel free to contribute to this project by submitting pull requests or suggesting improvements via issues.

## License
The intellectual property of this project belongs to ClickGreen. Licensing details, please visit the [official ClickGreen website](https://clickgreenapp.com).

## Contact
For more information, please contact `bry3639@gmail.com`.