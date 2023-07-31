"""
Risk Analysis Web Application using Flask, Python, and SVG.

This application allows users to perform risk analysis for different countries based on
threat models and weightings. The results are displayed using SVG graphs.
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# Sample data for threat models and weightings
threat_models = {
    "Canada": {"DDoS": 3, "Phishing": 4, "PhysicalAttack": 2, "CloudSecurity": 3},
    "India": {"DDoS": 4, "Phishing": 5, "PhysicalAttack": 3, "CloudSecurity": 2},
    "China": {"DDoS": 5, "Phishing": 5, "PhysicalAttack": 2, "CloudSecurity": 2},
    "Poland": {"DDoS": 2, "Phishing": 3, "PhysicalAttack": 1, "CloudSecurity": 4},
}


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The index route handles the form submission and rendering the initial form display.
    """
    if request.method == "POST":
        country_threat_weights = {}

        # Iterate over the form data to collect the country-specific threat weights
        for country in threat_models:
            # Retrieve the values from the HTML form fields
            ddos_weight_str = request.form[f"{country}_ddos_weight"]
            phishing_weight_str = request.form[f"{country}_phishing_weight"]
            physical_attack_weight_str = request.form[f"{country}_physical_attack_weight"]
            cloud_security_weight_str = request.form[f"{country}_cloud_security_weight"]

            # Validate the country value before proceeding
            if country not in threat_models:
                return render_template("index.html", message="Invalid country selected.")

            # Convert the weights to integers if they are not empty strings
            # You can provide a default value (0 in this case) if the input is empty or invalid
            ddos_weight = int(ddos_weight_str) \
                if ddos_weight_str.isdigit() else 0
            phishing_weight = int(phishing_weight_str) \
                if phishing_weight_str.isdigit() else 0
            physical_attack_weight = int(physical_attack_weight_str) \
                if physical_attack_weight_str.isdigit() else 0
            cloud_security_weight = int(cloud_security_weight_str) \
                if cloud_security_weight_str.isdigit() else 0

            # Store the threat weights in the nested dictionary for the country
            country_threat_weights[country] = {
                "DDoS": ddos_weight,
                "Phishing": phishing_weight,
                "PhysicalAttack": physical_attack_weight,
                "CloudSecurity": cloud_security_weight,
            }

        # Process the collected data, calculate risk scores, and store the results
        result_data = {}
        for country, threat_model in country_threat_weights.items():
            risk_score = calculate_risk_score(threat_model, country)
            result_data[country] = {
                "risk_score": risk_score,
                "threat_weights": threat_model,
                "ui_data": {
                    "DDoS_y": calculate_graph_y_position(threat_model["DDoS"]),
                    "Phishing_y": calculate_graph_y_position(threat_model["Phishing"]),
                    "PhysicalAttack_y": calculate_graph_y_position(threat_model["PhysicalAttack"]),
                    "CloudSecurity_y": calculate_graph_y_position(threat_model["CloudSecurity"]),
                    "main_y": calculate_graph_y_position(risk_score),
                    "DDoS_h": calculate_graph_height(threat_model["DDoS"]),
                    "Phishing_h": calculate_graph_height(threat_model["Phishing"]),
                    "PhysicalAttack_h": calculate_graph_height(threat_model["PhysicalAttack"]),
                    "CloudSecurity_h": calculate_graph_height(threat_model["CloudSecurity"]),
                    "main_h": calculate_graph_height(risk_score)
                },
            }

        # Render the template with the results
        return render_template("result.html", result_data=result_data)

    # Render the index template for initial form display
    return render_template("index.html", countries=list(threat_models.keys()))


def calculate_risk_score(threat_model, country):
    """
    Calculate the risk score based on threat model and weightings.

    Args:
        threat_model (dict): The dictionary containing threat weightings for a specific country.
        country (str): The name of the country.

    Returns:
        float: The calculated risk score rounded to two decimal places.
    """
    total_weight = sum(threat_model.values())
    risk_score = sum(threat_models[country][threat] * threat_model[threat] /
                     total_weight for threat in threat_model)
    return round(risk_score, 2)


def calculate_graph_y_position(weight):
    """
    Calculate the y-position of the threat weight for the graph.

    Args:
        weight (int): The threat weight.

    Returns:
        int: The calculated y-position.
    """
    y_position = 281 - ((weight * 10) / 100 * 281)
    return abs(y_position)


def calculate_graph_height(weight):
    """
    Calculate the height of the threat weight for the graph.

    Args:
        weight (int): The threat weight.

    Returns:
        int: The calculated height.
    """
    height = (weight * 10) / 100 * 281
    return abs(height)


if __name__ == "__main__":
    app.run(debug=True)
