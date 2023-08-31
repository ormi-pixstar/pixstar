from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


# 회원가입
class SignupSerializer(serializers.ModelSerializer):
    # 임시 데이터 필드 생성
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'validators': [validate_password],
            },
            'confirm_password': {
                'write_only': True,
                'required': True,
            },
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'detail': 'Password fields didn\'t match.'}
            )
        return attrs

    def create(self, validated_data):
        # confirm_password 제거
        confirm_password = validated_data.pop('confirm_password', None)

        user = User.objects.create(
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


# 로그인
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError({'detail': '이메일, 비밀번호를 확인해 주세요.'})


# 회원탈퇴
class SignoutSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['password']):
            raise serializers.ValidationError({'detail': '비밀번호가 올바르지 않습니다.'})
        return data


### User 프로필 조회
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'last_login']


### User 프로필 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

        def validate(self, data):
            email = data.get("email")

            user = self.context['user']
            name = user.name
