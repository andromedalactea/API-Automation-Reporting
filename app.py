from flask import Flask, request, jsonify
from scripts.main import reports_for_gv
import os

# Initialize Flask application
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_function():
    """
    Endpoint to execute the function. It processes the incoming JSON data,
    calls the reports_for_gv function, and returns the result.
    """
    try:
        # Parse JSON data from the request
        data = request.json
        project_list = data['project_list']
        for_gv = data['for_gv']
    
        # Call the reports_for_gv function with the parsed data
        result, emails_gv = reports_for_gv(project_list, for_gv)

        # Return the result as a JSON response
        return jsonify({"message": result, 'emails_gv': emails_gv}), 200

    except Exception as e:
        # Handle exceptions and return error message
        return jsonify({"error": str(e)}), 500

# Run the Flask application
if __name__ == "__main__":
    # Get the port number from the environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))

    # Start the Flask application with debugging enabled
    app.run(debug=True, host='0.0.0.0', port=port)
