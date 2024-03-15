from django.contrib import admin
from .models import User, ValidatedOtp, PhoneOtp, Verification

# class ValidatedOtpAdmin(admin.ModelAdmin):
#     list_display = (
#         'phone', 'otp'
#     )

admin.site.register(User)
# admin.site.register(ValidatedOtp, ValidatedOtpAdmin)
admin.site.register(ValidatedOtp)
admin.site.register(PhoneOtp)
admin.site.register(Verification)