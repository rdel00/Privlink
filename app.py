from flask import Flask, request, render_template, redirect, flash
import string
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory dictionary to store the URL mappings
url_mappings = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    expiration_time = None

    if request.method == 'POST':
        long_url = request.form['long_url'].strip()
        validity_minutes = request.form.get('validity_minutes', '').strip()

        if not long_url or not validity_minutes.isdigit() or int(validity_minutes) <= 0:
            flash('Please enter a valid URL and number of minutes.', 'danger')
            return redirect('/')

        short_code = generate_short_code()
        expiration_time = datetime.now() + timedelta(minutes=int(validity_minutes))
        url_mappings[short_code] = {'long_url': long_url, 'expiration_time': expiration_time}

        short_url = request.host_url + short_code
        flash(f'Success! Your short URL is: <a href="{short_url}" target="_blank">{short_url}</a>. It will expire in {validity_minutes} minutes.', 'success')

    return render_template("index.html", short_url=short_url, expiration_time=expiration_time)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url_mapping = url_mappings.get(short_code)
    
    if url_mapping:
        long_url = url_mapping['long_url']
        expiration_time = url_mapping['expiration_time']

        if datetime.now() < expiration_time:
            return redirect(long_url)
        else:
            del url_mappings[short_code]  # Remove expired mapping
            return redirect('/')  # Redirect to homepage without notification

    flash('Short URL not found.', 'danger')
    return redirect('/')

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

if __name__ == '__main__':
    app.run(debug=True)
