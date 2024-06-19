# from flask import Blueprint, request, jsonify,current_app, send_from_directory
# from werkzeug.utils import secure_filename
# import os
# import mimetypes

# create_positions = Blueprint('_create_positions', __name__)

# @create_positions.route('/create_positions', methods=['POST'])
# def create_positions_index():
#     mysql = current_app.extensions['mysql']

#     try:
#         # position = request.form['position']
#         # cgpa_criteria = request.form['cgpa_criteria']
#         # fee = request.form['fee']
#         # program = request.form['program_code']
#         # election = request.form['election_id']
#         # start_time = request.form['start_time']
#         # end_time = request.form['end_time']
#         # form = request.form['']

#         # Extract uploaded file
#         if 'file' not in request.files:
#             return jsonify({'Error': 'No file part'}), 400
        
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'Error': 'No selected file'}), 400
        
#         if file:
#             filename = secure_filename(file.filename)

#             # Check if the file is a PDF
#             if not file_content_type_is_pdf(file):
#                 return jsonify({'Error': 'Only PDF files are allowed'}), 400

#             # Get the upload directory from the app config
#             upload_folder = current_app.config.get('UPLOAD_FOLDER', '/uploads')
            
#             # Ensure the upload directory exists
#             if not os.path.exists(upload_folder):
#                 os.makedirs(upload_folder)
            
#             # Save the file to the upload directory
#             file_path = os.path.join(upload_folder, filename)
#             file.save(file_path)

#             print(f"Original file name: {file.filename}")
#             return send_from_directory(upload_folder, filename, as_attachment=True)


#             # file_data = file.read()
#             # cursor = mysql.connection.cursor()
#             # cursor.execute('INSERT INTO file_upload (id, file) VALUES (%s, %s)',
#             #                (None, file_data))
#             # mysql.connection.commit()
            
#             # return jsonify({'message': 'File has been saved successfully'})

#     except Exception as e:
#         return jsonify({'Error': str(e)}), 400



# def file_content_type_is_pdf(file):
#     # First, check the Content-Type header
#     content_type = file.content_type
#     if content_type!= 'application/pdf':
#         # If the Content-Type is not PDF, check the file extension
#         _, ext = os.path.splitext(file.filename)
#         if ext.lower()!= '.pdf':
#             return False
#     return True