# views.py
from django.shortcuts import render
from django.http import JsonResponse
import openai
from .forms import PDFUploadForm, SummarizeForm, QuestionForm
from .models import PDFDocument


def unified_view(request):
    pdf_form = PDFUploadForm()
    summarize_form = SummarizeForm()
    question_form = QuestionForm()
    context = {
        "pdf_form": pdf_form,
        "summarize_form": summarize_form,
        "question_form": question_form,
    }
    print(request)

    if request.method == "POST":
        print(request.post)
        if "upload_pdf" in request.POST:
            pdf_form = PDFUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                pdf_doc = pdf_form.save()
                text = pdf_form.process_pdf()
                print(text)
                context.update({"text": text, "pdf_id": pdf_doc.id})

        elif "summarize_text" in request.POST:
            summarize_form = SummarizeForm(request.POST)
            if summarize_form.is_valid():
                text = summarize_form.cleaned_data["text"]
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=f"Summarize the following text:\n\n{text}",
                    max_tokens=150,
                )
                summary = response.choices[0].text.strip()
                context.update({"summary": summary})

        elif "ask_question" in request.POST:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                text = question_form.cleaned_data["text"]
                question = question_form.cleaned_data["question"]
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=f"Based on the following text, answer the question:\n\nText: {text}\n\nQuestion: {question}",
                    max_tokens=150,
                )
                answer = response.choices[0].text.strip()
                context.update({"answer": answer})

    return render(request, "chatbot_app/unified_form.html", context)
