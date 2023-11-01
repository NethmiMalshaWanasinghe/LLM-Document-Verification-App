from flask import Flask, request, jsonify
import PyPDF2
import openai  # Import the OpenAI library

app = Flask("__name__")

# Set your OpenAI API key
openai.api_key = "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"

# Function to read PDF text from the uploaded file
def read_pdf_text(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page_num).extractText()
    return text

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    try:
        # Get the uploaded PDF file from the POST request
        pdf_file = request.files['pdf']
        if not pdf_file:
            return jsonify({'error': 'No PDF file uploaded'}), 400

        # Read text from the PDF
        pdf_text = read_pdf_text(pdf_file)

        # Append custom instructions string
        custom_instructions = "This is a custom instruction."
        modified_text = pdf_text + "\n" + custom_instructions

        # Call the OpenAI ChatGPT API with the "gpt-3.5-turbo" engine
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Choose the engine
            prompt=modified_text,     # Pass the text to the model
            max_tokens=100            # Set the maximum response length
        )

        if response and 'choices' in response:
            # Successfully called the API, return the generated text
            result_text = response['choices'][0]['text']
            return jsonify({'result': result_text})
        else:
            return jsonify({'error': 'API call failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '_main_':
    app.run(debug=True)
