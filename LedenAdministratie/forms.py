from datetime import date

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from tinymce.widgets import TinyMCE

from LedenAdministratie.models import Member, MemberType, Note, Invoice, Stripcard
from LedenAdministratie.invoice import INVOICE_TYPES


class MemberForm(forms.ModelForm):
    foto = forms.FileField(required=False)
    gebdat = forms.DateField(
        widget=forms.DateInput(format="%d-%m-%Y"),
        input_formats=settings.DATETIME_INPUT_FORMATS,
    )
    aanmeld_datum = forms.DateField(
        widget=forms.DateInput(format="%d-%m-%Y"),
        input_formats=settings.DATETIME_INPUT_FORMATS,
        initial=date.today(),
    )
    afmeld_datum = forms.DateField(
        widget=forms.DateInput(format="%d-%m-%Y"),
        input_formats=settings.DATETIME_INPUT_FORMATS,
        required=False,
    )

    class Meta:
        model = Member
        exclude = ["thumbnail", "user"]

    def save(self, commit=True):
        if "foto" in self.changed_data:
            data = self.cleaned_data["foto"]
            if isinstance(data, UploadedFile):
                data = data.file.read()
            self.instance.foto = data
            # Force re-gen of thumbnail
            self.instance.thumbnail = None
        return super().save(commit)


class ExportForm(forms.Form):
    filter_slug = forms.ModelChoiceField(
        label="Filter",
        required=False,
        empty_label="Alles",
        queryset=MemberType.objects.all(),
    )


class LidNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text", "done"]


class InvoiceCreateForm(forms.Form):
    invoice_types = forms.ChoiceField(choices=INVOICE_TYPES)
    members = forms.ModelMultipleChoiceField(queryset=Member.objects.all(), widget=forms.CheckboxSelectMultiple)


class InvoiceLineForm(forms.Form):
    description = forms.CharField(max_length=200, required=False)
    count = forms.IntegerField()
    amount = forms.DecimalField(max_digits=7, decimal_places=2)


class InvoicePartialPaymentForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["amount_payed"]


class InvoiceSelectionForm(forms.Form):
    invoices = forms.ModelMultipleChoiceField(queryset=Invoice.objects.all(), widget=forms.CheckboxSelectMultiple)


class EmailSendForm(forms.Form):
    VALID_RECIPIENTS = (
        ("members", "Leden"),
        ("parents", "Ouders"),
        ("begeleiders", "Begeleiders"),
        ("ondersteuning", "Ondersteuning"),
        ("self", "Mezelf"),
    )
    REPLY_TO = (
        ("info", settings.EMAIL_SENDER),
        ("lanparty", settings.EMAIL_LANPARTY),
        ("personal", "Persoonlijke Mail"),
    )
    reply_to = forms.ChoiceField(choices=REPLY_TO)
    recipients = forms.MultipleChoiceField(choices=VALID_RECIPIENTS, widget=forms.CheckboxSelectMultiple)
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=TinyMCE(mce_attrs={"cols": 80, "height": 500}))
    attachment = forms.FileField(required=False)


class SettingsForm(forms.Form):
    invoice_amount_year = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=True,
        initial=175.00,
        label="Factuurbedrag voor 1 jaar",
    )
    invoice_amount_year_senior = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=True,
        initial=215.00,
        label="Factuurbedrag voor 1 jaar, Senior lid",
    )
    invoice_amount_day = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=True,
        initial=6.00,
        label="Factuurbedrag per dag (strippenkaart)",
    )
    invoice_amount_month = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=True,
        initial=14.50,
        label="Kortingsbedrag per maand na 1 maart",
    )
    invoice_amount_sponsor = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=True,
        initial=150.00,
        label="Factuurbedrag voor 1 jaar, Sponsor",
    )
    welcome_pdf_location = forms.CharField(
        max_length=1024,
        required=True,
        label="Locatie van DJO Welkom PDF",
        initial="https://",
    )


class StripcardForm(forms.ModelForm):
    class Meta:
        model = Stripcard
        fields = ["issue_date", "count", "create_invoice"]
    create_invoice = forms.BooleanField(required=False, initial=True)

    def get_initial_for_field(self, field, field_name):
        if field_name == 'issue_date':
            return timezone.now()
        return super().get_initial_for_field(field, field_name)
