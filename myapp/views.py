from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
import vonage
import random
import string
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import (
    BankRegistrations,
    ApprovedRegistrations,
    DeclinedRegistrations,
    Transaction,
    HomeBannerMain,
    SubBanner,
    TrustedSecure,
    LatestNews,
    Card,
    Feedback,
    Email,
    LoanApplication,
    AdminDashboard,
    ApprovedLoans,
    Beneficiary,
)


def home(request):
    mainbanner = HomeBannerMain.objects.all()
    subbanner = SubBanner.objects.all()
    trusted = TrustedSecure.objects.all()
    latestnews = LatestNews.objects.all()
    reviews = Feedback.objects.all()[0:3]
    return render(
        request,
        'home.html',
        {
            'mainbanner': mainbanner,
            'subbanner': subbanner,
            'trusted': trusted,
            'latestnews': latestnews,
            'reviews': reviews,
        },
    )


def registration_form(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        mail = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        add1 = request.POST.get('address1')
        city1 = request.POST.get('city')
        state1 = request.POST.get('state')
        zip1 = request.POST.get('zip_code')
        deposit = request.POST.get('initial_deposit')
        image = request.FILES.get('image')
        signature = request.FILES.get('signature')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        phone = request.POST.get('phone_number')
        marital_status = request.POST.get('marital_status')
        otp = str(random.randint(100000, 999999))
        print(otp)

        if User.objects.filter(email=mail).exists() or ApprovedRegistrations.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Email or phone number already exists. Please use a different email or phone.')
            return render(request, 'registrationform.html')

        request.session['first_name'] = fname
        request.session['last_name'] = lname
        request.session['email'] = mail
        request.session['password'] = pass1
        request.session['confirm_password'] = pass2
        request.session['address1'] = add1
        request.session['city'] = city1
        request.session['state'] = state1
        request.session['zip_code'] = zip1
        request.session['initial_deposit'] = deposit
        request.session['gender'] = gender
        request.session['date_of_birth'] = dob
        request.session['marital_status'] = marital_status

        try:
            client = vonage.Client(key="d7c1e0c2", secret="EgbsRnVTYjew5p2y")
            sms = vonage.Sms(client)
            subject = "Sky Bank OTP Verification"
            message = f'''Dear Customer,
            

To ensure the security of your Sky Bank account, please use the following OTP for verification: {otp}. Use this code for your login or transaction. Do not share this code with anyone.

Thank you,
Sky Bank'''
            print(message)
            mail_from = settings.EMAIL_HOST_USER
            recipient_list = [request.session.get('email')]
            print(recipient_list)
            send_mail(subject, message, mail_from, recipient_list)

            responseData = sms.send_message(
                {
                    "from": "Vonage APIs",
                    "to": phone,
                    "text": f"Your OTP for Registration is: {otp}",
                }
            )

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
                raise Exception("Failed to send OTP via SMS.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messages.error(request, 'Failed to send OTP via SMS.')

        request.session['phone_number'] = phone
        request.session['otp'] = otp
        request.session.set_expiry(60)
        return redirect('otpverification')

    return render(request, 'registrationform.html')


def otp_verification(request):
    try:
        if request.method == 'POST':
            otp = request.POST['otp']
            fname = request.session['first_name']
            lname = request.session['last_name']
            mail = request.session['email']
            pass1 = request.session['password']
            pass2 = request.session['confirm_password']
            add1 = request.session['address1']
            city1 = request.session['city']
            state1 = request.session['state']
            zip1 = request.session['zip_code']
            deposit = request.session['initial_deposit']
            gender = request.session['gender']
            dob = request.session['date_of_birth']
            phone = request.session['phone_number']
            marital_status = request.session['marital_status']
            image = request.FILES.get('image')
            signature = request.FILES.get('signature')

            if otp == request.session['otp']:
                registration = BankRegistrations.objects.create(
                    first_name=fname,
                    last_name=lname,
                    email=mail,
                    password=pass1,
                    confirm_password=pass2,
                    address1=add1,
                    city=city1,
                    state=state1,
                    zip_code=zip1,
                    initial_deposit=deposit,
                    gender=gender,
                    date_of_birth=dob,
                    phone_number=phone,
                    marital_status=marital_status,
                    image=image,
                    signature=signature,
                    otp=otp,
                )

                registration.save()
                admin_dashboard = AdminDashboard.objects.first()
                admin_dashboard.total_registrations += 1
                admin_dashboard.save()

                request.session.pop('otp')
                request.session.pop('first_name')
                request.session.pop('last_name')
                request.session.pop('email')
                request.session.pop('password')
                request.session.pop('confirm_password')
                request.session.pop('address1')
                request.session.pop('city')
                request.session.pop('state')
                request.session.pop('zip_code')
                request.session.pop('initial_deposit')
                request.session.pop('gender')
                request.session.pop('date_of_birth')
                request.session.pop('phone_number')
                request.session.pop('marital_status')

                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'otpverification.html', {'phone': request.session['phone_number']})

        phone = request.session['phone_number']
    except KeyError:
        messages.error(request, 'Session expired. Please retry the registration process.')
        return redirect('register')

    return render(request, 'otpverification.html', {'phone': phone})




@user_passes_test(lambda u: u.is_superuser)
def applications(request):
    data = BankRegistrations.objects.all()
    return render(request, 'applications.html', {'data': data})


def approve_registration(request, registration_id):
    try:
        registration = get_object_or_404(BankRegistrations, id=registration_id)
        account_number = generate_account_number()
        user = User.objects.create_user(
            username=registration.email,
            first_name=registration.first_name,
            last_name=registration.last_name,
            email=registration.email,
            password=registration.password,

        )
        approved_registration = ApprovedRegistrations.objects.create(
            user=user,
            first_name=registration.first_name,
            last_name=registration.last_name,
            username=registration.username,
            email=registration.email,
            address1=registration.address1,
            city=registration.city,
            state=registration.state,
            zip_code=registration.zip_code,
            initial_deposit=registration.initial_deposit,
            image=registration.image,
            signature=registration.signature,
            gender=registration.gender,
            date_of_birth=registration.date_of_birth,
            phone_number=registration.phone_number,
            marital_status=registration.marital_status,
            account_number=account_number,
        )
        Card.objects.create(
            card_type="Debit Card",
            card_number=generate_card_number(),
            card_expiry=generate_expiry_date(),
            card_cvv=generate_cvv(),
            card_pin=generate_pin(),
            user=approved_registration.user,
        )
        subject = Email.objects.get(id=1).subject
        message = Email.objects.get(id=1).message
        mail_from = settings.EMAIL_HOST_USER
        recipient_list = [approved_registration.email]
        send_mail(subject, message, mail_from, recipient_list)
        admin_dashboard = AdminDashboard.objects.first()
        admin_dashboard.total_approved_users += 1
        admin_dashboard.save()
        registration.delete()

        messages.success(request,
                         f'Registration of {approved_registration.first_name} {approved_registration.last_name} approved. Debit card information sent.')
        return redirect('applications')

    except IntegrityError as e:
        messages.error(request, f'Error approving registration: {str(e)}')
        return redirect('applications')


def decline_registration(request, registration_id):
    registration = get_object_or_404(BankRegistrations, id=registration_id)
    DeclinedRegistrations.objects.create(
        first_name=registration.first_name,
        last_name=registration.last_name,
        email=registration.email,
        address1=registration.address1,
        city=registration.city,
        state=registration.state,
        zip_code=registration.zip_code,
        initial_deposit=registration.initial_deposit,
        image=registration.image,
        signature=registration.signature,
        gender=registration.gender,
        date_of_birth=registration.date_of_birth,
        phone_number=registration.phone_number,
        marital_status=registration.marital_status,
    )
    admin_dashboard = AdminDashboard.objects.first()
    admin_dashboard.total_declined_users += 1
    admin_dashboard.save()
    registration.delete()
    messages.warning(request, f'Registration of {registration.first_name} {registration.last_name} declined.')
    return redirect('applications')


def onlinebanking(request):
    return render(request, 'onlinebanking.html')


def money_transfer(request):
    user = request.user

    if request.method == 'POST':
        form = request.POST
        recipient_account_number = form.get('beneficiary')
        transfer_amount = str(form.get('transfer_amount', 0))
        transfer_type = form.get('transfer_type')
        remarks = form.get('remarks')

        try:
            beneficiary = Beneficiary.objects.get(user=user, account_number=recipient_account_number)

            request.session['recipient_account_number'] = recipient_account_number
            request.session['recipient_name'] = beneficiary.name
            request.session['transfer_amount'] = transfer_amount
            request.session['transfer_type'] = transfer_type
            request.session['remarks'] = remarks

            return redirect('moneytransferconfirm')

        except Beneficiary.DoesNotExist:
            messages.error(request, 'Recipient account not found in your beneficiaries.')
        except Exception as e:
            messages.error(request, f'An error occurred during the transfer: {str(e)}')

    beneficiary_list = Beneficiary.objects.filter(user=user)
    return render(request, 'moneytransfer.html', {'user': user, 'beneficiary_list': beneficiary_list})


def transfer_confirmation(request):
    recipient_account_number = request.session.get('recipient_account_number')
    recipient_name = request.session.get('recipient_name')
    transfer_amount = request.session.get('transfer_amount')
    transfer_type = request.session.get('transfer_type')
    remarks = request.session.get('remarks')

    context = {
        'recipient_account_number': recipient_account_number,
        'recipient_name': recipient_name,
        'transfer_amount': transfer_amount,
        'transfer_type': transfer_type,
        'remarks': remarks
    }
    return render(request, 'moneytransferconfirm.html', context)

def send_otp_email(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        otp = str(random.randint(100000, 999999))

        print(otp)
        request.session['otp'] = otp

        subject = "Sky Bank OTP Verification"
        message = f'''Dear Customer,

To ensure the security of your Sky Bank account, please use the following OTP for verification: {otp}. Use this code for your login or transaction. Do not share this code with anyone.

Thank you,
Sky Bank'''

        mail_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        try:
            send_mail(subject, message, mail_from, recipient_list)
        except Exception as e:
            print(f"Error sending OTP email: {e}")


        return HttpResponseRedirect(reverse('moneytransferconfirm'))

    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='login')
def confirm_otp_transfer(request):
    user = request.user
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp == request.session.get('otp'):
            recipient_account_number = request.session.get('recipient_account_number')
            transfer_amount = request.session.get('transfer_amount')
            transfer_type = request.session.get('transfer_type')

            try:
                if transfer_type == 'internal':
                    # Logic for transferring to a Sky Bank account
                    sender = ApprovedRegistrations.objects.get(user=request.user)
                    recipient = ApprovedRegistrations.objects.get(account_number=recipient_account_number)

                    # Deduct from sender's initial deposit
                    sender.initial_deposit -= Decimal(transfer_amount)
                    sender.save()

                    # Increase recipient's initial deposit
                    recipient.initial_deposit += Decimal(transfer_amount)

                    recipient.save()

                elif transfer_type == 'external':
                    # Logic for transferring to an account in another bank
                    sender = ApprovedRegistrations.objects.get(user=request.user)
                    recipient = Beneficiary.objects.get(account_number=recipient_account_number)
                    print(recipient)

                    # Deduct from sender's initial deposit
                    sender.initial_deposit -= Decimal(transfer_amount)
                    sender.save()

                    # Increase recipient's transfer_amount
                    recipient.transfer_amount += Decimal(transfer_amount)
                    print(recipient.transfer_amount)
                    recipient.save()

                admin_dashboard = AdminDashboard.objects.first()
                admin_dashboard.total_transactions_amount += transfer_amount
                admin_dashboard.total_transactions += 1
                admin_dashboard.save()

                Transaction.objects.create(
                    account_number=user.account_number,
                    transaction_type='Money Transfer',
                    amount=transfer_amount,
                    recipient_account=recipient.recipient_account_number,
                )
                print(Transaction)
                del request.session['otp']

                messages.success(request, 'Money transfer successful!')
                return redirect('home')

            except ApprovedRegistrations.DoesNotExist:
                messages.error(request, 'Recipient account not found.')
            except Beneficiary.DoesNotExist:
                messages.error(request, 'Recipient account not found.')
            except Exception as e:
                messages.error(request, f'Error during transfer: {str(e)}')

        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request,'success.html')

def success(request):
    transfer_amount = request.session.get('transfer_amount')
    recipient_account_number = request.session.get('recipient_account_number')
    recipient_name = request.session.get('recipient_name')
    transfer_type = request.session.get('transfer_type')
    remarks = request.session.get('remarks')

    del request.session['recipient_account_number']
    del request.session['transfer_amount']
    del request.session['transfer_type']
    del request.session['remarks']

    return render(request, 'success.html',{'transfer_amount':transfer_amount,'recipient_acount_number':recipient_account_number,'recipient_name':recipient_name,'transfer_type':transfer_type})

@login_required(login_url='login')
def deposit(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')
        deposit_amount = Decimal(request.POST.get('deposit_amount', 0))
        payment_method = request.POST.get('payment_method')
        signature_file = request.FILES.get('signature_file')

        try:
            # Authenticate the user
            authenticated_user = authenticate(request, account_number=account_number, password=password)

            if authenticated_user is not None:
                # Log in the user
                login(request, authenticated_user)

                # User authentication successful
                user = ApprovedRegistrations.objects.get(account_number=account_number)

                # Perform deposit logic
                user.initial_deposit += deposit_amount
                user.save()

                # Update admin dashboard
                admin_dashboard = AdminDashboard.objects.first()
                admin_dashboard.total_transactions_amount += deposit_amount
                admin_dashboard.total_transactions += 1
                admin_dashboard.save()

                # Create a transaction record
                Transaction.objects.create(
                    account_number=user.account_number,
                    transaction_type='Deposit',
                    amount=deposit_amount,
                    payment_type=payment_method,
                )

                messages.success(request, 'Deposit successful.')
                return redirect('profile')
            else:

                messages.error(request, 'Invalid credentials. Please check your account number and password.')
        except ApprovedRegistrations.DoesNotExist:
            messages.error(request, 'Invalid account number.')
        except Exception as e:
            messages.error(request, f'An error occurred during deposit: {str(e)}')

    return render(request, 'depositamount.html')


@login_required
def manage_beneficiaries(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account_number = request.POST.get('account_number')
        bank_name = request.POST.get('bank_name')
        ifsc_code = request.POST.get('ifsc_code') if bank_name == 'OtherBank' else None

        if bank_name == 'SkyBank':

            is_skybank_account = ApprovedRegistrations.objects.filter(account_number=account_number).exists()

            if not is_skybank_account:
                messages.warning(request, 'This user is not present in Sky Bank.')
                return render(request, 'manage_beneficiaries.html')


        beneficiary = Beneficiary.objects.create(
            user=request.user,
            name=name,
            account_number=account_number,
            bank_name=bank_name,
            ifsc_code=ifsc_code
        )
        beneficiary.save()

        return redirect('manage_beneficiaries')

    elif request.method == 'GET':
        beneficiary_list = Beneficiary.objects.filter(user=request.user)
        return render(request, 'manage_beneficiaries.html', {'beneficiary_list': beneficiary_list})

    return render(request, 'manage_beneficiaries.html')

@login_required
def delete_beneficiary(request, beneficiary_id):
    if request.method == 'POST':
        beneficiary = Beneficiary.objects.get(id=beneficiary_id)
        beneficiary.delete()
    return redirect('manage_beneficiaries')


def fetch_user_details(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number', '')

        try:
            user = ApprovedRegistrations.objects.get(account_number=account_number)
            data = {
                'success': True,
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'account_number': user.account_number,
                    'profile_image': user.image.url if user.image else None,
                },
            }
        except ApprovedRegistrations.DoesNotExist:
            data = {'success': False}
        return JsonResponse(data)

def logout_on_unload(request):
    logout(request)
    return JsonResponse({'message': 'User logged out successfully'})

@login_required(login_url='login')
def applyforloan(request):
    user = request.user

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        loan_type = request.POST.get('loanType')
        loan_amount = float(request.POST.get('loanAmount', 0))
        loan_tenure = request.POST.get('loanTenure')
        employment_status = request.POST.get('employmentStatus')
        annual_income = float(request.POST.get('annualIncome', 0))
        account_number = request.POST.get('accountNumber')
        additional_info = request.POST.get('message')

        interest_rates = {
            'Personal Loan': 10.50,
            'Home Loan': 8.45,
            'Car Loan': 8.82,
        }

        eligibility_criteria = {
            'Personal Loan': [
                {'min_amount': 5000, 'max_amount': 10000, 'min_income': 30000},
                {'min_amount': 10001, 'max_amount': 30000, 'min_income': 40000},
                {'min_amount': 30001, 'max_amount': None, 'min_income': 50000},
            ],
            'Home Loan': [
                {'min_amount': 10000, 'max_amount': 50000, 'min_income': 50000},
                {'min_amount': 50001, 'max_amount': 100000, 'min_income': 70000},
                {'min_amount': 100001, 'max_amount': None, 'min_income': 90000},
            ],
            'Car Loan': [
                {'min_amount': 8000, 'max_amount': 15000, 'min_income': 35000},
                {'min_amount': 15001, 'max_amount': 25000, 'min_income': 45000},
                {'min_amount': 25001, 'max_amount': None, 'min_income': 55000},
            ],
        }

        try:
            ranges = eligibility_criteria.get(loan_type, [])

            for criteria in ranges:
                if (
                        loan_amount >= criteria['min_amount'] and
                        (criteria['max_amount'] is None or loan_amount <= criteria['max_amount']) and
                        annual_income >= criteria['min_income']
                ):
                    interest_rate = interest_rates.get(loan_type, 0.0)
                    calculated_interest = (loan_amount * interest_rate * criteria.get('max_tenure', 1)) / 100
                    total_amount_due = loan_amount + calculated_interest

                    monthly_emi = float(total_amount_due) / float(loan_tenure)
                    print(monthly_emi)

                    LoanApplication.objects.create(
                        user=request.user,
                        full_name=full_name,
                        email=email,
                        phone_number=phone_number,
                        loan_type=loan_type,
                        loan_amount=loan_amount,
                        loan_tenure=loan_tenure,
                        employment_status=employment_status,
                        annual_income=annual_income,
                        account_number=account_number,
                        additional_info=additional_info,
                        interest_rate=interest_rate,
                        calculated_interest=calculated_interest,
                        total_amount_due=total_amount_due,
                        monthly_emi=monthly_emi,
                        status='Pending'
                    )

                    admin_dashboard = AdminDashboard.objects.first()
                    admin_dashboard.total_income += calculated_interest
                    admin_dashboard.total_loan_amount += loan_amount
                    admin_dashboard.total_loan_applications += 1
                    admin_dashboard.save()

                    messages.success(request, 'Loan application submitted successfully! We will contact you soon.')
                    return redirect('applyforloan')

            messages.warning(request, 'Loan eligibility criteria not met. Please review your details.')

        except KeyError:
            messages.error(request, 'Invalid loan type selected.')

    return render(request, 'applyforloan.html')


def approve_loan_application(request, loan_id):
    try:
        loan_application = get_object_or_404(LoanApplication, id=loan_id)
        loan_application.status = 'In Progress'
        loan_application.save()
        user = loan_application.user
        approved_registration = ApprovedRegistrations.objects.get(user=user)
        total_amount = approved_registration.initial_deposit + loan_application.loan_amount
        approved_registration.initial_deposit = total_amount
        approved_registration.save()

        Transaction.objects.create(
            transaction_type='Loan Amount',
            account_number=approved_registration.account_number,
            amount=total_amount,
        )
        ApprovedLoans.objects.create(
            user=user,
            loan_type=loan_application.loan_type,
            loan_amount=loan_application.loan_amount,
            interest_rate=loan_application.interest_rate,
            loan_tenure=loan_application.loan_tenure,
            total_amount_due=loan_application.total_amount_due,
            calculated_interest=loan_application.calculated_interest,
            monthly_emi=loan_application.monthly_emi,
            status='In Progress',
        )

        loan_application.delete()
        messages.success(request,
                         f'Loan disbursement of {loan_application.loan_amount}₹ successful for {loan_application.full_name}.')
        return redirect('loanapplications')

    except LoanApplication.DoesNotExist:
        messages.error(request, 'Loan application not found.')
    except ApprovedRegistrations.DoesNotExist:
        messages.error(request, 'User not found.')
    except Exception as e:
        messages.error(request, f'Error approving loan application: {str(e)}')

    return redirect('loanapplications')


def declined_loan_application(request, loan_id):
    try:
        loan_application = get_object_or_404(LoanApplication, id=loan_id)
        loan_application.status = 'Declined'
        loan_application.save()
        user = loan_application.user
        loan_application.delete()

        messages.success(request, 'Loan Application Declined Successfully')
        return redirect('loanapplications')

    except LoanApplication.DoesNotExist:
        messages.error(request, 'Loan Application Not Found')
        return redirect('loanapplications')

    except Exception as e:
        messages.error(request, f'Error declining loan application: {str(e)}')
        return redirect('loanapplications')


def loan_application(request):
    data = LoanApplication.objects.all()
    return render(request, 'loanapplications.html', {'data': data})


@login_required(login_url='login')
def pay_emi(request, loan_id):
    try:
        loan = ApprovedLoans.objects.get(id=loan_id, user=request.user, status='In Progress')
        emi_amount = loan.monthly_emi

        if request.method == 'POST':
            payment_amount = Decimal(request.POST.get('payment_amount', 0))

            if loan.total_amount_due > 0:
                main_account = ApprovedRegistrations.objects.get(user=request.user)

                if main_account.initial_deposit >= emi_amount or payment_amount >= emi_amount:
                    if payment_amount <= loan.total_amount_due:
                        main_account.initial_deposit -= payment_amount
                        loan.total_amount_due -= payment_amount
                        loan.save()
                        main_account.save()

                    Transaction.objects.create(
                        account_number=main_account.account_number,
                        transaction_type='EMI Payment',
                        amount=emi_amount,
                    )

                    messages.success(request, f'EMI payment of {payment_amount} ₹ successful.')

                    if loan.total_amount_due == 0:
                        loan.status = 'Paid'
                        loan.save()
                        main_account.status = 'Paid'
                        main_account.save()

                else:
                    messages.error(request, 'Insufficient funds or payment amount less than the EMI amount.')
            else:
                messages.error(request, 'No EMI payment is required as you have paid your complete loan amount.')

    except ApprovedLoans.DoesNotExist:
        messages.error(request, 'Loan already paid.')
    except Exception as e:
        messages.error(request, f'Error processing EMI payment: {str(e)}')

    return redirect('profile')


@login_required(login_url='login')
def statement(request):
    user = request.user

    try:
        approved_registration = ApprovedRegistrations.objects.get(user=user)
        transactions = Transaction.objects.filter(account_number=approved_registration.account_number)
        count = transactions.count()
        print(count)
        return render(request, 'statement.html', {'user': user, 'transactions': transactions, 'count': count})
    except ApprovedRegistrations.DoesNotExist:
        return render(request, 'statement.html', {'user': user, 'transactions': None})


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        mail_subject = 'Subject'
        mail_from = settings.EMAIL_HOST_USER
        recipient_list = ['chaitanya.gaikar143@gmail.com']

        send_mail(mail_subject, message, mail_from, recipient_list)

        Feedback.objects.create(
            user_name=name,
            email=email,
            description=message,
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contactus')

    return render(request, 'contactus.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        approved_registration = ApprovedRegistrations.objects.get(user=user)
        loan_info = ApprovedLoans.objects.filter(user=user)[0:1]
        card_info = Card.objects.filter(user=user).first()
        loan_status = LoanApplication.objects.filter(user=user)
        return render(
            request,
            'profile.html',
            {
                'user': user,
                'pvt_info': approved_registration,
                'card_info': card_info,
                'loan_info': loan_info,
                'loan_status': loan_status,
            },
        )
    except ApprovedRegistrations.DoesNotExist:
        return render(
            request, 'profile.html',
            {'user': user, 'pvt_info': None, 'card_info': None, 'loan_info': None, 'loan_status': None}
        )


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    approved_registration = get_object_or_404(ApprovedRegistrations, user=user)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        address1 = request.POST['address1']
        city = request.POST['city']
        state = request.POST['state']
        image = request.FILES.get('image')
        signature = request.FILES.get('signature')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        approved_registration.first_name = first_name
        approved_registration.last_name = last_name
        approved_registration.phone_number = phone_number
        approved_registration.address1 = address1
        approved_registration.city = city
        approved_registration.state = state
        approved_registration.image = image
        approved_registration.signature = signature
        approved_registration.password = password
        approved_registration.confirm_password = confirm_password
        approved_registration.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'updateprofile.html', {'user': user, 'approved_registration': approved_registration})


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    admin_dashboard = AdminDashboard.objects.all()
    transactions = Transaction.objects.order_by('-timestamp')[:10]
    return render(request, 'dashboard.html', {'admin_dashboard': admin_dashboard, 'transactions': transactions})


def reports(request):
    return render(request, 'adminreports.html')


def total_users(request):
    query = request.GET.get('q', '')
    search_fields = ['first_name', 'last_name', 'email', 'address1', 'city', 'state', 'zip_code', 'gender',
                     'date_of_birth', 'phone_number', 'marital_status']
    search_filter = Q()
    for field in search_fields:
        search_filter |= Q(**{f'{field}__icontains': query})
    data = ApprovedRegistrations.objects.filter(search_filter)

    return render(request, 'totalusers.html', {'data': data, 'query': query})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(1800)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(1800)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'adminlogin.html')

    return render(request, 'adminlogin.html')


def logout_admin(request):
    logout(request)
    return redirect('adminlogin')


def help(request):
    user = request.user
    approved_registration = ApprovedRegistrations.objects.get(user=user)
    transactions = Transaction.objects.filter(account_number=approved_registration.account_number)

    return render(request, 'help.html', {'user': user, 'transactions': transactions})


def generate_account_number():
    return ''.join(random.choices(string.digits, k=8))


def generate_card_number():
    return ''.join(random.choices(string.digits, k=16))


def generate_cvv():
    return ''.join(random.choices(string.digits, k=3))


def generate_pin():
    return ''.join(random.choices(string.digits, k=4))


def generate_expiry_date():
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=1095)
    formatted_expiry_date = expiry_date.strftime("%Y-%m-%d")
    return formatted_expiry_date
