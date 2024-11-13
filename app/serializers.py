from rest_framework import serializers

from .models import *


class AstronautSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, astronaut):
        if astronaut.image:
            return astronaut.image.url.replace("minio", "localhost", 1)

    class Meta:
        model = Astronaut
        fields = "__all__"


class AstronautItemSerializer(serializers.ModelSerializer):  # Для передачи в полете
    image = serializers.SerializerMethodField()
    captain = serializers.SerializerMethodField()

    def get_image(self, astronaut):
        if astronaut.image:
            return astronaut.image.url.replace("minio", "localhost", 1)

        return "http://localhost:9000/images/default.png"

    def get_captain(self, astronaut):
        return self.context.get("captain")

    class Meta:
        model = Astronaut
        fields = ("id", "name", "image", "captain")


class FlightSerializer(serializers.ModelSerializer):  # Полет просмотр
    astronauts = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    def get_astronauts(self, flight):
        items = AstronautFlight.objects.filter(flight=flight)
        return [AstronautItemSerializer(item.astronaut, context={"captain": item.captain}).data for item in items]

    class Meta:
        model = Flight
        fields = '__all__'


class FlightsSerializer(serializers.ModelSerializer):  # Список полетов
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Flight
        fields = "__all__"


class AstronautFlightSerializer(serializers.ModelSerializer):  # М-М
    class Meta:
        model = AstronautFlight
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):  # User
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
