# Generated by Django 5.0 on 2024-02-11 17:19

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_transactions', models.IntegerField()),
                ('total_transactions_amount', models.IntegerField()),
                ('total_loan_amount', models.IntegerField()),
                ('total_income', models.IntegerField()),
                ('total_loan_applications', models.IntegerField(null=True)),
                ('total_registrations', models.IntegerField()),
                ('total_approved_users', models.IntegerField()),
                ('total_declined_users', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BankRegistrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('initial_deposit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('card_type', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('signature', models.ImageField(blank=True, null=True, upload_to='signatures/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('gender', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(default=datetime.date.today, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('otp', models.CharField(max_length=6, null=True)),
                ('marital_status', models.CharField(max_length=20, null=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100, null=True)),
                ('confirm_password', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeclinedRegistrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('initial_deposit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('card_type', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('signature', models.ImageField(blank=True, null=True, upload_to='signatures/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('gender', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(default=datetime.date.today, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('otp', models.CharField(max_length=6, null=True)),
                ('marital_status', models.CharField(max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, null=True)),
                ('message', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('user_name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomeBannerMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_banner', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('banner_title', models.CharField(blank=True, default='First Line<br>Second Line', max_length=100)),
                ('banner_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LatestNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('news1_title', models.CharField(max_length=100, null=True)),
                ('news1_description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_banner', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('sub_banner_title', models.CharField(max_length=100, null=True)),
                ('sub_banner_description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=8)),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Money Transfer', 'Money Transfer'), ('Loan Disbursement', 'Loan Disbursement')], max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(blank=True, max_length=20, null=True)),
                ('recipient_account', models.CharField(blank=True, max_length=8, null=True)),
                ('deposit_details', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrustedSecure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trusted_secure', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('trusted_secure_title', models.CharField(max_length=100, null=True)),
                ('trusted_secure_description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovedLoans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.CharField(choices=[('personal', 'Personal Loan'), ('home', 'Home Loan'), ('car', 'Car Loan')], max_length=250, null=True)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('loan_tenure', models.IntegerField(null=True)),
                ('monthly_emi', models.IntegerField(blank=True, null=True)),
                ('total_amount_due', models.IntegerField(blank=True, null=True)),
                ('calculated_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Declined', 'Declined'), ('In Progress', 'In Progress'), ('Paid', 'Paid')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovedRegistrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('initial_deposit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('card_type', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('signature', models.ImageField(blank=True, null=True, upload_to='signatures/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('gender', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(default=datetime.date.today, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('otp', models.CharField(max_length=6, null=True)),
                ('marital_status', models.CharField(max_length=20, null=True)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('account_number', models.IntegerField(unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=20)),
                ('bank_name', models.CharField(choices=[('SkyBank', 'SkyBank'), ('OtherBank', 'Other Bank')], max_length=255)),
                ('ifsc_code', models.CharField(blank=True, max_length=20, null=True)),
                ('transfer_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(max_length=100, null=True)),
                ('card_number', models.CharField(max_length=16)),
                ('card_expiry', models.DateField(null=True)),
                ('card_cvv', models.IntegerField(null=True)),
                ('card_pin', models.IntegerField(null=True)),
                ('card_background', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('loan_type', models.CharField(choices=[('Personal Loan', 'Personal Loan'), ('Home Loan', 'Home Loan'), ('Car Loan', 'Car Loan')], max_length=250)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('loan_tenure', models.IntegerField(null=True)),
                ('monthly_emi', models.IntegerField(blank=True, null=True)),
                ('employment_status', models.CharField(max_length=20)),
                ('annual_income', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('account_number', models.CharField(max_length=20, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount_due', models.IntegerField(blank=True, null=True)),
                ('calculated_interest', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Declined', 'Declined'), ('In Progress', 'In Progress'), ('Paid', 'Paid')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HelpTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('category', models.CharField(choices=[('transaction_complaint', 'Transaction Complaint'), ('loan_assistance', 'Loan Assistance'), ('other', 'Other'), ('loan_application', 'Loan Application')], max_length=50)),
                ('sub_category_1', models.CharField(blank=True, choices=[('personal', 'Personal Loan'), ('car', 'Car Loan'), ('home', 'Home Loan'), ('transfer', 'Money Transfer'), ('deposit', 'Deposit'), ('emi', 'EMI')], max_length=50, null=True)),
                ('sub_category_2', models.CharField(blank=True, choices=[('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('disbursed', 'Disbursed'), ('repaid', 'Repaid'), ('defaulted', 'Defaulted'), ('failed', 'Payment Failed'), ('complete_not_received', 'Payment Complete but Not Received'), ('pending', 'Payment Pending'), ('refunded', 'Payment Refunded'), ('processing', 'Payment Processing'), ('cancelled', 'Payment Cancelled'), ('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partial Payment'), ('late', 'Late Payment'), ('defaulted', 'Defaulted')], max_length=50, null=True)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recent_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.transaction')),
            ],
        ),
    ]
