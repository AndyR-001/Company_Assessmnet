#!C:\Users\Andyr\AppData\Local\Programs\Python\Python311\python.exe
print("Content-Type: text/html\n")

import mysql.connector
from flask import Flask, request, redirect, render_template, url_for, session

app = Flask(__name__)

conn = mysql.connector.connect(
        host="localhost", 
        port="3306", 
        user="root", 
        password="", 
        database="assessment_results"
    )
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('WebsiteDevelopment.html') #render_template('WebsiteDevelopment.html')

@app.route("/submit", methods=["POST"])
def submit():
    form_data = request.form

    query = """
        INSERT INTO survey_data (
            company_name, industry, employee_count, num_security_employees, securityBreach, 
            password_Requirements, accessRemoval, multifactorCredentials, logicalAccess, disasterRecoveryPlan, 
            incidentResponseTeam, incidentResponsePlanTesting, securityTools, cyberInsurance, dataBackups, 
            dataRemoval, externalDevices, cybersecurityArchitecture, assetInventory, networkProtection, 
            confidentialDataEncryption, leastFunctionality, securityApplications, vulnerability_assessments, 
            cyber_risk_management, risk_management_program, risk_mitigation_strategies, vendor_management, 
            humanResourcePolicy, secureCoding, securityAwareness, backgroundChecks, cybersecurityResponsibilities, 
            thirdPartyAssessment, physicalAccessControls, changeManagementProcess, 
            documentedSecurityPolicies, policiesReviewed, physicalAccessRevoked, gdprCompliant
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = tuple(form_data.values())
    
    cursor.execute(query, values)
    conn.commit()

    return redirect(url_for('results', companyName = request.form['company_name']))


@app.route('/results', methods=['GET'])
def results():
     # Define the SQL query to retrieve the answers from the survey results
    query = "SELECT * FROM survey_data WHERE company_name = %s"

    # Execute the query
    cursor.execute(query, (request.args.get('companyName'),))

    # Initialize the answers dictionary
    answers = {}

    # Fetch the rows one by one
    row = cursor.fetchone()
    while row is not None:
        # Iterate through the row and add the answers to the dictionary
        for i in range(len(row)):
            column_name = cursor.column_names[i]
            answer = row[i]
            answers[column_name] = answer

        # Fetch the next row
        row = cursor.fetchone()

    # Define the risk score variable
    risk_score = 0

        # Define the questions and corresponding points
    questions = {
        "securityBreach": 5,
        "password_Requirements": 0, 
        "accessRemoval": 2,
        "multifactorCredentials": 3,
        "logicalAccess": 3,
        "disasterRecoveryPlan": 3,
        "incidentResponseTeam": 1,
        "incidentResponsePlanTesting": 1,
        "securityTools": 3,
        "cyberInsurance": 3,
        "dataBackups": 4,
        "dataRemoval": 2,
        "externalDevices": 1,
        "cybersecurityArchitecture": 2,
        "assetInventory": 4,
        "networkProtection": 2,
        "confidentialDataEncryption": 4,
        "leastFunctionality": 3,
        "securityApplications": 3,
        "vulnerability_assessments": 2,
        "cyber_risk_management": 3,
        "risk_management_program": 3,
        "risk_mitigation_strategies": 3,
        "vendor_management": 1,
        "humanResourcePolicy": 3,
        "secureCoding": 3,
        "securityAwareness": 3,
        "backgroundChecks": 4,
        "cybersecurityResponsibilities": 3,
        "physicalAccessControls": 3,
        "changeManagementProcess": 2,
        "documentedSecurityPolicies": 4,
        "policiesReviewed": 1,
        "physicalAccessRevoked": 2,
        "gdprCompliant": 5
        }

# Iterate through the answers and add the corresponding weights to the risk score
    for question, answer in answers.items():
        if answer == "no":
            risk_score += questions[question]
    
    # Calculate the percentage risk score
    total_possible_risk_score = sum(questions.values())
    percentage_risk_score = risk_score / total_possible_risk_score
    percentage_risk_score = risk_score / total_possible_risk_score * 100
    percentage_risk_score = int(percentage_risk_score)

    
# Initialize the recommendations variable
    recommendations = []  
    
    companyName = request.args.get('companyName')
      # Define the SQL query to retrieve the dataEncryption value from the survey results
    query = "SELECT confidentialDataEncryption FROM survey_data WHERE company_name = %s"

    # Execute the query
    cursor.execute(query, (companyName,))

   # Fetch the rows one by one
    row = cursor.fetchone()
    while row is not None:
    # Check if the company has data encryption in place
        if row[0] == "no":
            recommendations.append("It is recommended that your company implement data encryption to protect sensitive data in transit and at rest.")

    # Fetch the next row
        row = cursor.fetchone()
    
    return render_template('results.html', companyName=companyName, recommendations=recommendations,percentage_risk_score=percentage_risk_score)
    cursor.close()
    conn.close()
    
   
if __name__ == '__main__':
    app.debug = True
    app.run()
