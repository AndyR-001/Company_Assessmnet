#!C:\Users\Andyr\AppData\Local\Programs\Python\Python310\python.exe
# Import the Flask and request libraries
from flask import Flask, request, redirect

# Define the Flask app
app = Flask(__name__)

# Define the route for the form submission
@app.route("/submit", methods=["POST"])
def submit():
    # Get the company name from the form
    companyName = request.form.get("companyName")

    # Connect to the database
    conn = mysql.connect(host="localhost",port="3306", user="root", password="mysql", database="assessment_results")
    cursor = conn.cursor()

    # Define the SQL query to retrieve the dataEncryption value from the survey results
    query = "SELECT dataEncryption FROM survey_data WHERE companyName = %s"

    # Execute the query
    cursor.execute(query, (companyName,))

    # Fetch the result
    result = cursor.fetchone()
    print("companyName")

    # Define the recommendations to be sent to the user
    recommendations = []

    # Check if the company has data encryption in place
    if result[0] == "No":
        recommendations.append("It is recommended that your company implement data encryption to protect sensitive data in transit and at rest.")

    # Define the URL of the output page
    url = "http://localhost/output"

    # Redirect the user to the output page
    return redirect(url)

# Run the app
if __name__ == "__main__":
    app.run()
