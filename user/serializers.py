from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from post.storage import S3Storage

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


# 비밀번호 확인
class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['password']):
            raise serializers.ValidationError({'detail': '비밀번호가 올바르지 않습니다.'})
        return data


# 프로필 조회
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'image_url')


# 프로필 수정
class ProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'image_url', 'password', 'current_password')
        extra_kwargs = {
            'username': {
                'required': False,
            },
            'password': {
                'write_only': True,
                'required': False,
                'validators': [validate_password],
            },
            'current_password': {
                'write_only': True,
                'required': True,
            },
        }

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError({'password': '비밀번호가 올바르지 않습니다.'})
        return data

    def update(self, instance, validated_data):
        validated_data.pop('current_password', None)

        instance.username = validated_data.get("username", instance.username)
        password = validated_data.get("password", instance.password)
        instance.set_password(password)
        image_data = self.context["request"].FILES

        if "image_url" not in image_data:
            image_data = None

        if image_data is not None:
            s = S3Storage()
            image = User.objects.get(email=instance.email)
            s.image_delete(image)
            for data in image_data.getlist('image_url'):
                s.upload(instance.email, data)
                instance.image_url = s.getUrl()

        instance.save()
        return instance