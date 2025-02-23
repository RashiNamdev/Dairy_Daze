from django.shortcuts import render



'''from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Dairy Daze OTP System!")
'''



# Create your views here.
import random
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import OTP, CustomUser

# Function to Generate OTP
def generate_otp():
    return random.randint(100000, 999999)  # 6-digit OTP

def front_page(request):
    return render(request, 'mhome.html')  # Apna HTML file ka path daalo


@api_view(['POST'])
def send_otp(request):

    
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "Email is required!"}, status=400)

    # Generate OTP
    otp_code = generate_otp()

    # Save OTP to Database (with expiry of 5 minutes)
    OTP.objects.create(email=email, otp_code=otp_code, expires_at=now() + timedelta(minutes=5))

    # Send OTP via Email
    send_mail(
        "Your OTP Code",
        f"Your OTP is: {otp_code}\nThis OTP is valid for 5 minutes.",
        "your_email@gmail.com",
        [email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent successfully!"})


@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp')

    if not email or not otp_code:
        return Response({"error": "Email and OTP are required!"}, status=400)

    try:
        otp_code = int(otp_code)  # Ensure OTP is an integer
    except ValueError:
        return Response({"error": "Invalid OTP format!"}, status=400)

    # Fetch OTP from Database
    otp_entry = OTP.objects.filter(email=email).first()

    if not otp_entry:
        return Response({"error": "OTP not found!"}, status=400)

    # Check if OTP is expired
    if otp_entry.expires_at < now():
        otp_entry.delete()  # Delete expired OTP
        return Response({"error": "OTP expired!"}, status=400)

    if otp_entry.otp_code == otp_code:
        # Mark User as Verified
        user, created = CustomUser.objects.get_or_create(email=email)
        user.is_verified = True
        user.save()

        # Delete OTP after verification
        otp_entry.delete()

        return Response({"message": "OTP Verified, Registration Complete!"})
    else:
        return Response({"error": "Invalid OTP!"}, status=400)
