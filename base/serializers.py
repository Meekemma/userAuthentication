
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        
        # Validate the password using Django's built-in validators
        validate_password(password)

        return attrs
    
    def validate_email(self, value):
        # Normalize the email before checking if it exists
        normalized_email = value.lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return normalized_email

    def create(self, validated_data):
        # Ensure the email is stored in lowercase
        validated_data['email'] = validated_data['email'].lower()
        # Remove password2 from validated data
        validated_data.pop('password2')  
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        # Hash the password
        user.set_password(password) 
        user.save()
        return user





# Serializer for changing user password
class changePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')


         # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            raise serializers.ValidationError('Old password is incorrect')

        # check that the new password and confirmation match
        if new_password != confirm_password:
            raise serializers.ValidationError("New Password and Confirm Password don't match")
        

        return attrs
    

        # Set the new password for the user
    def save(self):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']

        # Set the new password for the user
        user.set_password(new_password)
        user.save()
       


# Serializer for resetting user password via email
class resetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True, max_length=50, style={'input_type':'email'}, write_only=True)
