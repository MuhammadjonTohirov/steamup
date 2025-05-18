from django.utils.translation import gettext as _

def get_email_templates(purpose, otp_code):
    """
    Get email templates for the given purpose and OTP code.
    Templates are translated using the current active language.
    
    Args:
        purpose: The purpose of the email ('verify' or 'reset')
        otp_code: The OTP code to include in the email
        
    Returns:
        A tuple of (subject, body) with translated content
    """
    if purpose == 'verify':
        subject = _("SteamUp - Your OTP for email verification")
        body = _("""
        Hello,
        
        Your one-time password (OTP) for email verification is: {otp}
        
        This OTP will expire in 5 minutes.
        
        Best regards,
        The SteamUp Team
        """).format(otp=otp_code)
    else:  # purpose == 'reset'
        subject = _("SteamUp - Your OTP for password reset")
        body = _("""
        Hello,
        
        Your one-time password (OTP) for password reset is: {otp}
        
        This OTP will expire in 5 minutes.
        
        Best regards,
        The SteamUp Team
        """).format(otp=otp_code)
    
    return subject, body