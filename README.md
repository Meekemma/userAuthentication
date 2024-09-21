# JWT Authentication System

This project demonstrates how to implement secure authentication in a Django application using JWT (JSON Web Token). It covers how to generate, verify, and manage tokens to authenticate and authorize users, ensuring a scalable and stateless authentication process.

### Getting Started
1. Set Up the Django Project and Create the App
First, ensure your Django project is set up. Then, create a new app called base using the following command:

``python manage.py startapp base``


2. Install Django REST Framework
You need Django REST Framework to manage the API endpoints. Install it by running:

``pip install djangorestframework``

3. Configure Installed Apps

Add the following to the INSTALLED_APPS section in your settings.py file:

INSTALLED_APPS = [
    
    'base.apps.BaseConfig',  # Your base app
    'rest_framework',        # Django REST Framework
]


For more details, visit the official Django REST Framework documentation here.

https://www.django-rest-framework.org/





# Getting Started with Simple JWT

**1.Install Simple JWT**

To implement JSON Web Token (JWT) authentication in your Django project, you need to install the djangorestframework-simplejwt package. Run the following command:

``pip install djangorestframework-simplejwt``

you can find more detailed documentation here.

https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

**2.Register Simple JWT in Installed Apps**

After installing, add rest_framework_simplejwt to the INSTALLED_APPS section in your settings.py file:

INSTALLED_APPS = [

    'base.apps.BaseConfig',  # Your base app
    'rest_framework',        # Django REST Framework
    'rest_framework_simplejwt',  # Simple JWT for authentication
]

___
## User Model

Since JWT authentication requires the user model to handle email-based authentication and token management, this project uses a custom user model. Below is an explanation of the key components of the User model:

**Custom UserManager**

The custom UserManager class is used to handle user creation and management. It defines methods for creating users and superusers, ensuring email, first name, and last name are required fields.

**Custom User Model**

The User model inherits from Django's AbstractBaseUser and PermissionsMixin to customize user authentication. It uses email as the unique identifier (USERNAME_FIELD) instead of a username and stores additional fields like first_name, last_name, and auth_provider.

After creating the custom user model, it needs to be Your addition about registering the custom user model and setting the `AUTH_USER_MODEL` in `settings.py` is clear and useful for anyone following the setup. Here’s a slightly refined version to make it more concise and clear:

---

### Register the Custom User Model

After creating the custom `User` model, make sure to:

1. **Register it in `admin.py`**  
   

 
   

2. **Set the Custom User Model in `settings.py`**  
   In your `settings.py` file, specify the custom user model:

   ```python
   AUTH_USER_MODEL = "base.User"
   ```

3. **Apply Migrations**  
   After registering the model and configuring `settings.py`, run the following commands to apply migrations:

   ```bash
   python manage.py makemigrations base
   python manage.py migrate
   ```

---

## Serializers.py

### User Registration & Authentication: Serializers

To handle user registration, password changes, and password resets, the following key serializers are used:

1. **Registration Serializer**  
   This serializer handles user registration, ensuring that the password fields match and that the email is unique.

   ```python
   class RegistrationSerializer(serializers.ModelSerializer):
       password2 = serializers.CharField(write_only=True)

       def validate(self, attrs):
           if attrs['password'] != attrs['password2']:
               raise serializers.ValidationError("Passwords don't match.")
           return attrs

       def create(self, validated_data):
           # Create and return a new user
           validated_data.pop('password2')
           user = User.objects.create_user(**validated_data)
           return user
   ```

2. **Change Password Serializer**  
   This serializer allows users to change their password by validating the old password and ensuring the new passwords match.

   ```python
   class ChangePasswordSerializer(serializers.Serializer):
       old_password = serializers.CharField(write_only=True)
       new_password = serializers.CharField(write_only=True)
       confirm_password = serializers.CharField(write_only=True)

       def validate(self, attrs):
           if attrs['new_password'] != attrs['confirm_password']:
               raise serializers.ValidationError("Passwords don't match.")
           return attrs
   ```

3. **Reset Password via Email Serializer**  
   This serializer collects the user’s email to initiate the password reset process.

   ```python
   class ResetPasswordEmailSerializer(serializers.Serializer):
       email = serializers.EmailField(write_only=True)
   ```

These serializers are integral to user authentication and account management, ensuring secure password handling and user data validation.

---






### User Registration & Authentication: Views

The following views manage user registration, token generation, and password changes:

1. **Registration View**  
   This view handles user registration by validating the provided data through the `RegistrationSerializer`. Upon successful validation, a new user is created.

   ```python
   @api_view(['POST'])
   def registration_view(request):
       serializer = RegistrationSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   ```

2. **Custom Token Obtain Pair Serializer**  
   This serializer extends the functionality of the default JWT token serializer to include additional user information in the token.

   ```python
   class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
       @classmethod
       def get_token(cls, user):
           token = super().get_token(user)
           # Add custom claims
           token['user_id'] = user.id
           token['first_name'] = user.first_name
           token['last_name'] = user.last_name
           token['email'] = user.email
           token['is_verified'] = user.is_verified
           return token
   ```

3. **Custom Token Obtain Pair View**  
   This view uses the custom token serializer to generate JWT tokens with additional user claims.

   ```python
   class MyTokenObtainPairView(TokenObtainPairView):
       serializer_class = MyTokenObtainPairSerializer 
   ```

4. **Change Password View**  
   This view allows authenticated users to change their passwords by validating the provided old and new passwords using the `ChangePasswordSerializer`.

   ```python
   @api_view(['PUT'])
   @permission_classes([IsAuthenticated])
   def changePasswordView(request):
       serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
       return Response({"error": "Failed to change password", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   ```

These views are essential for managing user accounts and handling authentication through JWT.

---




### URL Configuration

The following endpoints are set up for user registration, authentication, and password management:

1. **Registration Endpoint**  
   - **URL:** `/registration/`  
   - **Method:** `POST`  
   - **Description:** Allows new users to register by providing their details.

2. **Login Endpoint**  
   - **URL:** `/login/`  
   - **Method:** `POST`  
   - **Description:** Authenticates users and issues a JWT token using the custom token obtain pair view.

3. **Token Refresh Endpoint**  
   - **URL:** `/token/refresh/`  
   - **Method:** `POST`  
   - **Description:** Allows users to refresh their JWT tokens.

4. **Change Password Endpoint**  
   - **URL:** `/change-password/`  
   - **Method:** `PUT`  
   - **Description:** Enables authenticated users to change their password.

These routes enable essential user account operations and JWT authentication in the application.

---
