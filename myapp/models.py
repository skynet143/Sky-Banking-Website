from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import datetime

class BaseRegistration(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    address1 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    initial_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    card_type = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    gender = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True, default=datetime.date.today)
    phone_number = models.CharField(max_length=15, null=True)
    otp = models.CharField(max_length=6, null=True)
    marital_status = models.CharField(max_length=20, null=True)

    class Meta:
        abstract = True

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Money Transfer', 'Money Transfer'),
        ('Loan Disbursement','Loan Disbursement'),
    ]

    account_number = models.CharField(max_length=8)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, null=True, blank=True)
    recipient_account = models.CharField(max_length=8, null=True, blank=True)
    deposit_details = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"

class BankRegistrations(BaseRegistration):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100, null=True)
    confirm_password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ApprovedRegistrations(BaseRegistration):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    account_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DeclinedRegistrations(BaseRegistration):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HomeBannerMain(models.Model):
    main_banner = models.ImageField(upload_to='images/', null=True, blank=True)
    banner_title = models.CharField(max_length=100, default="First Line<br>Second Line", blank=True)
    banner_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.banner_title

class SubBanner(models.Model):
    sub_banner = models.ImageField(upload_to='images/', null=True, blank=True)
    sub_banner_title = models.CharField(max_length=100, null=True)
    sub_banner_description = models.TextField(null=True)

    def __str__(self):
        return self.sub_banner_title

class TrustedSecure(models.Model):
    trusted_secure = models.ImageField(upload_to='images/', null=True, blank=True)
    trusted_secure_title = models.CharField(max_length=100, null=True)
    trusted_secure_description = models.TextField(null=True)

    def __str__(self):
        return self.trusted_secure_title

class LatestNews(models.Model):
    news1 = models.ImageField(upload_to='images/', null=True, blank=True)
    news1_title = models.CharField(max_length=100, null=True)
    news1_description = models.TextField(null=True)

    def __str__(self):
        return self.news1_title

class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=100, null=True)
    card_number = models.CharField(max_length=16)
    card_expiry = models.DateField(null=True)
    card_cvv = models.IntegerField(null=True)
    card_pin = models.IntegerField(null=True)
    card_background = models.ImageField(upload_to='images/', null=True, blank=True)


    def __str__(self):
        return str(f"{self.user.first_name} {self.user.last_name}")

class Feedback(models.Model):
    description = models.TextField(null=True)
    user_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.user_name

class Email(models.Model):
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)
    def __str__(self):
        return self.subject


class LoanApplication(models.Model):
    LOAN_TYPES = [
        ('Personal Loan', 'Personal Loan'),
        ('Home Loan', 'Home Loan'),
        ('Car Loan', 'Car Loan'),
    ]
    STATUS=[
        ('Pending','Pending'),
        ('Declined','Declined'),
        ('In Progress','In Progress'),
        ('Paid','Paid')
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    loan_type = models.CharField(max_length=250, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    loan_tenure = models.IntegerField(null=True)
    monthly_emi = models.IntegerField( blank=True, null=True)
    employment_status = models.CharField(max_length=20)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    account_number = models.CharField(max_length=20,null=True)
    additional_info = models.TextField(blank=True, null=True)
    application_date = models.DateTimeField(auto_now_add=True)
    total_amount_due = models.IntegerField( blank=True, null=True)
    calculated_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status=models.CharField(max_length=20,choices=STATUS)

    def __str__(self):
        return f"{self.user.username} - {self.loan_type} - {self.application_date}"

class ApprovedLoans(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Declined', 'Declined'),
        ('In Progress', 'In Progress'),
        ('Paid', 'Paid')
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=250, choices=LOAN_TYPES,null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    loan_tenure = models.IntegerField(null=True)
    monthly_emi = models.IntegerField( blank=True, null=True)
    total_amount_due = models.IntegerField( blank=True, null=True)
    calculated_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return f"{self.user.username}"


class HelpTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    CATEGORY_CHOICES = [
        ('transaction_complaint', 'Transaction Complaint'),
        ('loan_assistance', 'Loan Assistance'),
        ('other', 'Other'),
        ('loan_application', 'Loan Application'),
    ]

    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('car', 'Car Loan'),
        ('home', 'Home Loan'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('transfer', 'Money Transfer'),
        ('deposit', 'Deposit'),
        ('emi', 'EMI'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('failed', 'Payment Failed'),
        ('complete_not_received', 'Payment Complete but Not Received'),
        ('pending', 'Payment Pending'),
        ('refunded', 'Payment Refunded'),
        ('processing', 'Payment Processing'),
        ('cancelled', 'Payment Cancelled'),
    ]

    LOAN_STATUS_CHOICES = [
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    ]

    EMI_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial Payment'),
        ('late', 'Late Payment'),
        ('defaulted', 'Defaulted'),
    ]

    ALL_CHOICES = LOAN_TYPE_CHOICES + PAYMENT_TYPE_CHOICES
    ALL_CHOICES_2 = LOAN_STATUS_CHOICES + PAYMENT_STATUS_CHOICES + EMI_STATUS_CHOICES

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sub_category_1 = models.CharField(max_length=50, choices=ALL_CHOICES, null=True, blank=True)
    sub_category_2 = models.CharField(max_length=50, choices=ALL_CHOICES_2, null=True, blank=True)
    recent_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)

    message = models.TextField()

    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ticket #{self.pk} - {self.category} - {self.status}'


class AdminDashboard(models.Model):
    total_transactions = models.IntegerField()
    total_transactions_amount = models.IntegerField()
    total_loan_amount = models.IntegerField()
    total_income=models.IntegerField()
    total_loan_applications = models.IntegerField(null=True)
    total_registrations = models.IntegerField()
    total_approved_users = models.IntegerField()
    total_declined_users = models.IntegerField()

    def __str__(self):
        return str(self.total_transactions)


class Beneficiary(models.Model):
    BANK_CHOICES = [
        ('SkyBank', 'SkyBank'),
        ('OtherBank', 'Other Bank'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=255, choices=BANK_CHOICES)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)


    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.account_number} ({self.bank_name})"