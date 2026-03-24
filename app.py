from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = "https://wcjfkzdaanvvfehksvzh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndjamZremRhYW52dmZlaGtzdnpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNjQxNDMsImV4cCI6MjA4OTk0MDE0M30.VDU7IxifZzmT6sPANxiyURV5YXO3BegiSYfqU5rcPh0"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # Fetch Alumni list from Supabase
    response = supabase.table('alumni').select("*").execute()
    return render_template('index.html', alumni=response.data)

# --- NEW ROUTE: ADD ALUMNI ---
@app.route('/add_alumni', methods=['POST'])
def add_alumni():
    # Collecting data from the "Join the Network" form
    data = {
        "name": request.form.get('name'),
        "batch_year": int(request.form.get('batch_year')),
        "dept": request.form.get('dept'),
        "company": request.form.get('company')
    }
    # Inserting the new alumnus into the Supabase table
    supabase.table('alumni').insert(data).execute()
    return redirect(url_for('index'))

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        # Save donation data
        data = {
            "alumni_id": int(request.form['alumni_id']), # Ensure this is an integer
            "amount": float(request.form['amount']),     # Ensure this is a number
            "purpose": request.form['purpose']
        }
        supabase.table('donations').insert(data).execute()
        return redirect(url_for('index'))
    
    # Load alumni names for the dropdown
    res = supabase.table('alumni').select("id, name").execute()
    return render_template('donate.html', alumni=res.data)

if __name__ == '__main__':
    app.run(debug=True)