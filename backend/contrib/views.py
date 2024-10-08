from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Consignataria, Servidor, ConsultaMargemAthenas, Reserva
from .serializers import ConsignatariaSerializer, ServidorSerializer, ConsultaMargemAthenasSerializer, ReservaSerializer, ConsignatariaSerializerV2, ServidorSerializerV2, ConsultaMargemAthenasSerializerV2, ReservaSerializerV2
import requests

class ConsignatariaViewSet(viewsets.ModelViewSet):
    queryset = Consignataria.objects.all()
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConsignatariaSerializer  # Default serializer class

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ConsignatariaSerializerV2
        return self.serializer_class

class ServidorViewSet(viewsets.ModelViewSet):
    queryset = Servidor.objects.all()
    serializer_class = ServidorSerializer  # Default serializer class

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ServidorSerializerV2
        return self.serializer_class

class ConsultaMargemAthenasViewSet(viewsets.ModelViewSet):
    queryset = ConsultaMargemAthenas.objects.all()
    serializer_class = ConsultaMargemAthenasSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        servidor_id = request.data.get('servidor')
        consignataria_id = request.data.get('consignataria')

        if not servidor_id or not consignataria_id:
            return Response({"error": "IDs de servidor e consignataria são necessários."}, status=status.HTTP_400_BAD_REQUEST)

        servidor = get_object_or_404(Servidor, id=servidor_id)

        headers = {
            "Authorization": "Token 682770e6bbe57c2736138619840a564bd0775486"
        }

        response = requests.get(
            f"https://athenas.defensoria.ro.def.br/api/consignado/?matricula={servidor.matricula}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data['count'] > 0:
                resultado = data['results'][0]
                margem_total = resultado['margem_consignada_total']
                margem_disponivel = resultado['margem_consignada_livre']

                consignataria = get_object_or_404(Consignataria, id=consignataria_id)

                consulta = ConsultaMargemAthenas.objects.create(
                    margem_total=margem_total,
                    margem_disponivel=margem_disponivel,
                    servidor=servidor,
                    consignataria=consignataria,
                    cadastrado_por=request.user
                )

                serializer = self.get_serializer(consulta)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Nenhum resultado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Erro ao consultar a API externa"}, status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        matricula = request.query_params.get('matricula')

        if not matricula:
            return Response({"error": "Matrícula não fornecida."}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": "Token 682770e6bbe57c2736138619840a564bd0775486"
        }

        response = requests.get(
            f"https://athenas.defensoria.ro.def.br/api/consignado/?matricula={matricula}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data['count'] > 0:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Nenhum resultado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Erro ao consultar a API externa"}, status=response.status_code)

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ConsultaMargemAthenasSerializerV2
        return self.serializer_class

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['cadastrado_por'] = request.user.pk  # Usando o ID do usuário autenticado
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data['modificado_por'] = request.user.pk  # Usando o ID do usuário autenticado
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.desativar(request.user)  # Passando o usuário atual para o método desativar
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ReservaSerializerV2
        return self.serializer_class
