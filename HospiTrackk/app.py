from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load hospital dataset
df = pd.read_csv('hospital_dataset.csv')

# Function to recommend doctors
def recommend_doctor(specialty, location):
    filtered_df = df[(df['Specialty'].str.lower() == specialty.lower()) & (df['Location'].str.lower() == location.lower())]
    
    if filtered_df.empty:
        filtered_df = df[df['Specialty'].str.lower() == specialty.lower()]
        message = f"No doctors found in {location}. Showing doctors from other locations."
    else:
        message = ""

    sorted_df = filtered_df.sort_values(by='Success Rate of Doctor (%)', ascending=False)
    
    return sorted_df.head(5), message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template('patient_dashboard.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app.route('/search', methods=['POST'])
def search():
    specialty = request.form['specialty']
    location = request.form['location']
    
    recommendations, message = recommend_doctor(specialty, location)
    
    return render_template('results.html', doctors=recommendations.to_dict(orient='records'), message=message)
admin_data = {
    "total_appointments": 20,
    "patient_queries": 5,
    "doctors_available": 8
}

# Sample appointment data
appointments = [
    {"id": 1, "patient_name": "John Doe", "doctor_name": "Dr. Smith", "hospital": "City Hospital", "time": "10:00 AM", "status": "Pending"},
    {"id": 2, "patient_name": "Jane Smith", "doctor_name": "Dr. Lee", "hospital": "Metro Hospital", "time": "2:00 PM", "status": "Confirmed"},
    {"id": 3, "patient_name": "Mike Johnson", "doctor_name": "Dr. Patel", "hospital": "Sunrise Clinic", "time": "4:30 PM", "status": "Pending"}
]

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', 
                           total_appointments=admin_data["total_appointments"], 
                           patient_queries=admin_data["patient_queries"], 
                           doctors_available=admin_data["doctors_available"],
                           appointment_status=appointments)

@app.route('/update_appointment_status', methods=['POST'])
def update_appointment_status():
    appointment_id = int(request.form['appointment_id'])
    new_status = request.form['new_status']
    
    for appointment in appointments:
        if appointment['id'] == appointment_id:
            appointment['status'] = new_status
            break

    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
