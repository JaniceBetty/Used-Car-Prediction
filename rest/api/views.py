from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CarPricePredictionRequestSerializer,
    CarPricePredictionResponseSerializer
)
from .predictors.model import predict_price

class PredictPriceView(APIView):
    def post(self, request):
        serializer = CarPricePredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prediction = predict_price(serializer.validated_data)

                if not prediction:
                    return Response({"error": "No valid predictions found"}, status=status.HTTP_404_NOT_FOUND)
                
                response_serializer = CarPricePredictionResponseSerializer(data={
                    "min_price": prediction["min_price"],
                    "max_price": prediction["max_price"],
                    "optimal_price": prediction["optimal_price"]
                })
                
                if response_serializer.is_valid():
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
