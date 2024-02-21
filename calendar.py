from flask import Flask, request, jsonify
from google.oauth2 import service_account
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask_cors import CORS
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)
# Function to create a service for interacting with the Google Calendar API
def create_calendar_service(credentials_path):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    return service

# Function to get calendar events
def get_calendar_events(calendar_id, service):
    events_result = service.events().list(calendarId=calendar_id, singleEvents=True).execute()
    events = events_result.get('items', [])
    return events

# Function to send reminder email
def send_reminder_email(event, attendee_email):
    # Email Configuration
    sender_email = 'mareedusritha@gmail.com'
    sender_password = 'dkjcfvrkuvrklvsw'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = attendee_email
    msg['Subject'] = 'Reminder: ' + event.get('summary')

    start_date = event['start'].get('dateTime', 'No start date')

    body = f"""\
    Hello,

    This is a reminder for the event:
    {event.get('summary')}

    Date: {start_date}
    Location: {event.get('location')}

    Regards,
    Your Name
    """
    msg.attach(MIMEText(body, 'plain'))

    # Send Email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# API endpoint to get calendar events
@app.route('/events')
def get_calendar_events_api():
    credentials_path = 'C:/Users/maree/Downloads/sritha2001-7be0510ce251.json'  # Update with your JSON key file path
    calendar_id = 'mareedusritha@gmail.com'  # Update with your calendar ID
    service = create_calendar_service(credentials_path)
    events = get_calendar_events(calendar_id, service)
    return jsonify(events)

# API endpoint to send reminder emails for upcoming events
@app.route('/send_reminder_emails')
def send_reminder_emails_api():
    credentials_path = 'C:/Users/maree/Downloads/sritha2001-7be0510ce251.json'  # Update with your JSON key file path
    calendar_id = 'mareedusritha@gmail.com'  # Update with your calendar ID
    service = create_calendar_service(credentials_path)
    events = get_calendar_events(calendar_id, service)
    for event in events:
        cst = pytz.timezone('America/Chicago')
        current_time_cst = datetime.now(cst)
        formatted_current_time = current_time_cst.strftime('%Y-%m-%dT%H:%M:%S%z')
        starttime_str = event['start'].get('dateTime', 'No start time specified')
        starttime = datetime.strptime(starttime_str, "%Y-%m-%dT%H:%M:%S%z")
        time_difference = starttime - current_time_cst
        time_difference_minutes = time_difference.total_seconds() / 60
        if current_time_cst<starttime:
            for attendee in event.get('attendees', []):
                send_reminder_email(event, attendee.get('email', 'No email'))
    return jsonify({'message': 'Reminder emails sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)