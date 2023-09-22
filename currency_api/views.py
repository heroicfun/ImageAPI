from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Currency
from .serializers import CurrencySerializer
from .utils import update_exchange_rates

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyConversionView(APIView):
    def post(self, request):
        from_currency = request.data.get('from_currency')
        to_currency = request.data.get('to_currency')
        value = request.data.get('value')

        # Оновити курси валют перед конвертацією
        if update_exchange_rates():
            try:
                from_currency_rate = Currency.objects.get(currency_code=from_currency).exchange_rate
                to_currency_rate = Currency.objects.get(currency_code=to_currency).exchange_rate

                converted_value = value * (to_currency_rate / from_currency_rate)

                response_data = {
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'value': value,
                    'converted_value': converted_value,
                    'conversion_rate': to_currency_rate / from_currency_rate
                }

                return Response(response_data)
            except Currency.DoesNotExist:
                return Response({'error': 'Invalid currency code'}, status=400)
        else:
            return Response({'error': 'Failed to update exchange rates'}, status=500)