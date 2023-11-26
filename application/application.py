# app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for simplicity (replace with database in a real application)
applications = []

@app.route('/applications', methods=['GET'])
def get_all_applications():
    return jsonify(applications)

@app.route('/applications/<application_id>', methods=['GET'])
def get_application(application_id):
    application = next((app for app in applications if app['id'] == application_id), None)
    if application:
        return jsonify(application)
    else:
        return jsonify({"error": "Application not found"}), 404

@app.route('/application', methods=['POST'])
def create_application():
    data = request.json
    new_application = {
        'id': str(len(applications) + 1),
        'details': data.get('details'),
        'status': 'Pending'
    }
    applications.append(new_application)
    return jsonify({"message": "Application created successfully", "application": new_application}), 201

@app.route('/application', methods=['GET'])
def filter_applications():
    # Example filtering logic based on query parameters
    recruiter_email = request.args.get('recruiterEmail')
    applicant_email = request.args.get('applicantEmail')

    filtered_applications = applications

    if recruiter_email:
        filtered_applications = [app for app in filtered_applications if app.get('recruiterEmail') == recruiter_email]

    if applicant_email:
        filtered_applications = [app for app in filtered_applications if app.get('applicantEmail') == applicant_email]

    return jsonify(filtered_applications)

@app.route('/application/<application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    application = next((app for app in applications if app['id'] == application_id), None)
    if application:
        data = request.json
        new_status = data.get('status')
        if new_status:
            application['status'] = new_status
            return jsonify({"message": f"Application status updated to {new_status}"}), 200
        else:
            return jsonify({"error": "Missing 'status' field in the request body"}), 400
    else:
        return jsonify({"error": "Application not found"}), 404

@app.route('/application/<application_id>', methods=['DELETE'])
def withdraw_application(application_id):
    global applications
    applications = [app for app in applications if app['id'] != application_id]
    return jsonify({"message": "Application withdrawn successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
