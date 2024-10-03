# Game Result Prediction Web App using ADW AutoML

This is a Flask web application that predicts the results of NBA games based on various statistical inputs. It utilizes Tailwind CSS for styling and integrates with ADW AutoML Model for predictions.

## Features

- **Flask** as the web framework
- **Tailwind CSS** for responsive and modern design
- **Game result prediction** based on NBA team statistics
- Prepopulated form fields for quicker user interaction


## Technologies Used

- **Flask**: Backend framework for serving the app
- **Tailwind CSS**: A utility-first CSS framework for styling
- **Autonomous Data Warehouse (ADW) AutoML deployed Model as a RESTful API

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Flask installed (`pip install flask`)
- Access to an ADW AutoML deployed Model

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/fr4nc1sj0hn/adw-autoML.git
    cd adw-autoML
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```bash
    flask run
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000/`.

2. Fill out the form with the required attributes for game prediction. The form includes fields such as **Home Game**, **Team Rest Days**, **Allowed Points**, **Offensive Rebounds**, etc.

3. Submit the form. The results will display above the form, showing the classifications and probabilities for different game outcomes.

## File Structure

```bash
├── app.py               # Main Flask app
├── templates
│   └── index.html       # HTML template with Tailwind CSS
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
