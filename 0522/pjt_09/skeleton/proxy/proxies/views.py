"""
교육생 구현 영역: 각 뷰에서 serializer로 검증 후 services 함수를 호출하고,
결과를 적절한 HTTP 상태 코드와 함께 반환하세요.
chat_response 는 예시로 구현되어 있습니다. 나머지는 pass 를 채워 구현하세요.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from proxies.serializers import ChatRequestSerializer, ChatResponseSerializer
from proxies.services import get_chat_response


@api_view(["POST"])
def chat_response(request):
    """예시: 채팅 완성 요청을 중간 서버가 모델 서버로 전달합니다."""
    serializer = ChatRequestSerializer(data=request.data)

    if serializer.is_valid():
        result = get_chat_response(serializer.validated_data)

        if result is None:
            return Response(
                {"detail": "Chat response failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(ChatResponseSerializer(result).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def chat_guardrail_response(request):
    # TODO: ChatGuardrailRequestSerializer 검증 후 get_chat_guardrail_response 호출
    # 적절하면 201, 부적절하면 403
    pass


@api_view(["POST"])
def chat_score_response(request):
    # TODO: ChatScoreRequestSerializer 검증 후 get_chat_score_response 호출
    pass


@api_view(["POST"])
def image_generation_response(request):
    # TODO: ImageGenerationRequestSerializer 검증 후 get_image_generation_response 호출
    pass


@api_view(["POST"])
def image_score_response_for_url(request):
    # TODO: ImageScoreRequestForImageURLSerializer 검증 후 get_image_score_response_for_url 호출
    pass


@api_view(["POST"])
def decide_route_response(request):
    # TODO: DecideRouteRequestSerializer 검증 후 get_decide_route_response 호출
    pass


@api_view(["POST"])
def tts_response(request):
    # TODO: GenerateSpeechRequestSerializer 검증 후 get_tts_response 호출
    pass
