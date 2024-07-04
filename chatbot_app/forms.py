from django import forms
from .models import PDFDocument
from PyPDF2 import PdfReader


class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        super(PDFUploadForm, self).__init__(*args, **kwargs)
        # Custom initialization logic
        self.custom_action()

    def custom_action(self):
        # Your custom action logic here
        print("Custom action executed!")

    def process_pdf(self):
        text = self.extract_text_pdf(self.instance.file)
        return text

    @staticmethod
    def extract_text_pdf(pdf_file):
        text = ""
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
        return text


class SummarizeForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Text to Summarize")


class QuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Text")
    question = forms.CharField(max_length=255, label="Question")
