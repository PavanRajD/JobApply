from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session
import os
import uuid

from scripts.dice_applier import DiceJobBoard
from scripts.utils import get_user_sent_ids, save_user_sent_ids

app = Flask(__name__)
app.secret_key = "sample_key"  # Set a secret key for sessions

@app.route('/')
def home():
    return render_template('index.html')

# Submit form data (POST request)
@app.route('/submit', methods=['POST'])
def submit_job_data():
    try:
        # Generate a unique session ID for this user if not set
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())

        # Store personal and job info in session
        personal_info = {
            'name': request.form['name'],
            'contact': request.form['contact'],
            'linkedin_url': request.form['LinkedInURL'],
            'email': request.form['email'],
            'password': request.form['password'],
            'skills': request.form['skills'],
            'content': request.form['content'],
        }
        
        job_info = {
            'keywords': request.form['JobTitle'],
            'locations': request.form['Location'],
            'job_type': request.form['JobType'],
            'job_posted': request.form['JobPosted']
        }
        
        resume_file = request.files['resume']
        
        # Generate a unique filename and save the resume
        resume_filename = os.path.join("uploads", f"{session['user_id']}_{resume_file.filename}")
        resume_file.save(resume_filename)

        # Save to session storage
        session['personal_info'] = personal_info
        session['job_info'] = job_info
        session['resume_filename'] = resume_filename

        return jsonify({"message": "Data submitted successfully!"})
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Stream updates (GET request for SSE)
@app.route('/stream')
def stream_updates():
    @stream_with_context
    def generate():
        try:
            # Retrieve the stored info from session
            personal_info = session.get('personal_info')
            job_info = session.get('job_info')
            resume_filename = session.get('resume_filename')
            user_id = session.get('user_id')

            board = DiceJobBoard()
            job_id_list = board.fetch_jobs(job_info)
            sent_ids = get_user_sent_ids(user_id)

            for idx, job_id in enumerate(job_id_list):
                if job_id not in sent_ids:
                    job_details = board.get_job_details(job_id)
                    if job_details:
                        # EmailSender.send_email(job_details, personal_info, resume_filename)
                        sent_ids.add(job_id)
                        save_user_sent_ids(user_id, sent_ids)

                        # Yield real-time update
                        yield f"data: Applied job {idx + 1}/{len(job_id_list)}: {job_id}\n\n"
                
            # Clean up resume file after processing
            os.remove(resume_filename)
            yield "data: Job search completed and emails sent successfully!\n\n"
        
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
