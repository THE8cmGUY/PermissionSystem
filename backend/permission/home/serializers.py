from rest_framework import serializers
from .models import *
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    role = serializers.ChoiceField(choices=User.ROLES_CHOICES) # help in validating the choices , the user selects out of the  provided choices not anyother 
    admin_code = serializers.CharField(required = False , allow_blank=True)
    specialization = serializers.CharField(required = False , allow_blank=True)
    license_number = serializers.CharField(required = False , allow_blank = True)
    hospital_name = serializers.CharField(required = False , allow_blank = True)
    medical_history = serializers.CharField(required = False , allow_blank = True)
    insurance_number = serializers.CharField(required = False , allow_blank = True)
    employee_id = serializers.CharField(required = False , allow_blank = True)
    department = serializers.CharField(required = False , allow_blank = True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'admin_code',
            'specialization',
            'license_number',
            'hospital_name',
            'medical_history',
            'insurance_number',
            'employee_id',
            'department',
        ]
    def validate(self, data):
        if data['role'] == 'admin' and not data.get('admin_code'):
            raise serializers.ValidationError("Admin code is required for admin role")
        if data['role'] == 'doctor' and not all([data.get('specialization') , data.get('license_number') , data.get('hospital_name')]):
            raise serializers.ValidationError("Specialization , license number and hospital name are required for doctor")
        if data['role']=='patient' and not all([data.get('medical_history' ), data.get('insurance_number')]):
            raise serializers.ValidationError("Medical history is required for patient")
        if data['role'] == 'staff' and not data.get('employee_id'):
            raise serializers.ValidationError("Employee id is required for staff")
        
        
        return data
    def create(self, validated_data):
        role = validated_data.pop('role')
        profile_data = {
            "admin_code":validated_data.pop('admin_code' , ''),
            "specialization":validated_data.pop('specialization' , ''),
            "license_number":validated_data.pop('license_number' , ''),
            "hospital_name":validated_data.pop('hospital_name' , ''),
            "medical_history":validated_data.pop('medical_history' , ''),
            "insurance_number":validated_data.pop('insurance_number' , ''),
            "employee_id":validated_data.pop('employee_id' , ''),
            "department":validated_data.pop('department' ,'' )

        }
        user = User.objects.create_user(**validated_data , role=role)
        if role =='admin':
            AdminProfile.objects.create(
                user = user,
                admin_code = profile_data['admin_code'],

            )
        elif role == 'doctor':
            DoctorProfile.objects.create(
                user = user,
                specialization = profile_data['specialization'],
                license_number = profile_data['license_number'],
                hospital_name = profile_data['hospital_name'],

            )
        elif role == 'patient':
            PatientProfile.objects.create(
                user = user,
                medical_history = profile_data['medical_history'],
                insurance_number = profile_data['insurance_number'],

            )
        return user


    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username' , 'email' , 'role']
        def to_representation(self , instance):
            data = super.to_representation(instance)
            if instance.role=='admin':
                data['profile']= AdminProfile.objects.filter(user = instance).values().first()
            elif instance.role=='doctor':
                data['profile']= DoctorProfile.objects.filter(user = instance).values().first()
            elif instance.role=='patient':
                data['profile']= PatientProfile.objects.filter(user = instance).values().first()
            elif instance.role=='staff':
                data['profile']= StaffProfile.objects.filter(user = instance).values().first()
            return data
            
            
            
            
            
            
            


