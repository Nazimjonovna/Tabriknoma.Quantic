from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User, ValidatedOtp, Verification


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)


class Otpser(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('otp', 'phone')


class Accaunt(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('name',  'image')
        read_only_fields = ('password',)

class GetUserInfoSerializer(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('id','phone', 'name',  'image')
        read_only_fields = ('password',)


class Validateser(serializers.ModelSerializer):


    class Meta:
        model = ValidatedOtp
        fields = ('phone', 'otp')


class Register(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ("phone", "name", "password")


    # def validate(self, attrs):

    #     if not attrs['phone']:
    #         raise serializers.ValidationError({"Xato":"Siz telefon raqamingizni kiritmadingiz :("})
    #     elif not attrs['name']:
    #         raise serializers.ValidationError({"Xato": "Siz ismingizni kiritmadingiz :("})
    #     elif not attrs['password']:
    #         raise serializers.ValidationError({"Xato": "Siz passwordni kiritmadingiz :("})

    #     return attrs


class Log(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ("phone", "password")


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'password2']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['password2']:
            raise serializers.ValidationError({'passwords': "The two password fields didn't match."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'wrong password'})
        instance.password = validated_data.get('password', instance.password)

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('phone', 'new_password', 're_new_password')

    def validate(self, attrs):
        if not attrs['new_password']:
            raise serializers.ValidationError({'new_password': 'This field is required.'})

        if not attrs['re_new_password']:
            raise serializers.ValidationError({'re_new_password': 'This field is required.'})

        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({'passwords': "The two password fields didn't match."})

        return attrs


class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ('phone', 'verify_code', 'step_change_phone')
        extra_kwargs = {
            'step_change_phone': {'read_only': True}
        }

    def update(self, instance, validated_data):
        verify_code = validated_data['verify_code']
        if instance.verify_code == verify_code:
            instance.is_verified = True
            if instance.step_reset == 'send':
                instance.step_reset = 'confirmed'
            if instance.step_change_phone:
                if instance.step_change_phone == 'send':
                    instance.step_change_phone = 'confirmed'
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'error': 'Phone number or verify code incorrect'})


class SendSmsSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    text = serializers.CharField(max_length=256)