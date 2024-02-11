# admin.py
from django.contrib import admin
from .models import (
    ApprovedRegistrations,
    BankRegistrations,
    DeclinedRegistrations,
    Transaction,
    HomeBannerMain,
    SubBanner,
    TrustedSecure,
    LatestNews,
    Card,
    Feedback,
    Email,
    AdminDashboard,
    LoanApplication,
    ApprovedLoans,
    Beneficiary,
)

admin.site.register(ApprovedRegistrations)
admin.site.register(BankRegistrations)
admin.site.register(DeclinedRegistrations)
admin.site.register(Transaction)
admin.site.register(HomeBannerMain)
admin.site.register(SubBanner)
admin.site.register(TrustedSecure)
admin.site.register(LatestNews)
admin.site.register(Card)
admin.site.register(Feedback)
admin.site.register(Email)
admin.site.register(AdminDashboard)
admin.site.register(LoanApplication)
admin.site.register(ApprovedLoans)
admin.site.register(Beneficiary)

