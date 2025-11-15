# TODO: Add Summary Length Options and Highlight Key Points

- [x] Edit templates/index.html: Add select dropdown for summary length (short/medium/long) before the submit button.
- [x] Edit static/script.js: Append selected length to formData; change summaryContent.textContent to innerHTML.
- [x] Edit app.py: Update / route to get length from request.form; modify generate_summary to adjust prompt based on length and include highlighting instruction.
- [x] Test the app by running and uploading a file to verify functionality.
- [x] Improve UI/UX for better user interaction: Add unique styling, animations, and interactive elements to the length selector and summary display.
