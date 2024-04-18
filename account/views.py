from rest_framework import generics, status, viewsets
from account.models import User, OneTimePassword
from rest_framework.response import Response
from account.utils import generate_otp, send_template_email, delete_instance_after
from account.serializers import UserRegistrationSerializer, UserSerializer,SendOtpSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import MethodNotAllowed
# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        otp = generate_otp(user)
        send_template_email(
            subject="Active your email on Bindu",
            templateName="confirm_email.html", 
            toEmail=user.email, 
            context={"fullName":user.username,
                "otp": otp}
                )
        return user

class SendOtpView(generics.GenericAPIView):
    serializer_class = SendOtpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        if user:
            otp = generate_otp(user)
            send_template_email(
                subject="Active your email on Bindu",
                templateName="confirm_email.html", 
                toEmail=user.email, 
                context={"fullName":user.username,
                    "otp": otp}
                    )
            return Response(
                {
                    "New OTP has been sent to your email. check again."
                }, status=status.HTTP_200_OK
            )
        # if there is no user with the email
        return Response(
            {
                "error": "Invalid Email, Please enter correct email."
            }, status=status.HTTP_404_NOT_FOUND
        )

class VerifyEmailView(generics.GenericAPIView):
    def post(self, request):
        otp = request.data.get('otp')
        try:
            user_otp_instance = OneTimePassword.objects.get(otp=otp)
            validOtp = delete_instance_after(user_otp_instance, 5) # Checking OTP expire period for five minutes
            if(validOtp):
                user = user_otp_instance.user
                user.is_active = True
                user.save()
                return Response(
                    {
                        'message': 'Account email verified successfully.'
                    }, status=status.HTTP_202_ACCEPTED
                )
            return Response(
                {
                    'error': 'Otp expired. Try again.'
                }, status=status.HTTP_204_NO_CONTENT
            )
        except OneTimePassword.DoesNotExist:
            return Response(
                {
                    'error': 'Otp not provided.'
                }, status=status.HTTP_404_NOT_FOUND
            )

        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")
