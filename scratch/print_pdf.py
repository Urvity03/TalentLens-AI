"""Scratch script to inspect the text of sample_resume.pdf."""

from modules.preprocess import extract_text_from_pdf, normalize_text

text = normalize_text(extract_text_from_pdf('samples/resumes/sample_resume.pdf'))
with open('scratch/resume_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Text saved to scratch/resume_text.txt successfully.")
