from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        print("✅ CustomTokenObtainPairSerializer.validate()  :", data)
        # 추가 정보도 넣을 수 있음
        return data
