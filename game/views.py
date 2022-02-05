from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import questions


##########################################
# Game Master endpoints
##########################################


@api_view(["POST"])
def register_gm(request):
    """
    Registers GM
    :param request: { id: str }
    :return: status code
    """
    pass


@api_view(["POST"])
def gm_start(request):
    """
    Starts the game if requested by GM
    - if countdown specified, players will see a countdown till the game starts
    - if gameLength specified, players will see a timer till the game ends (after it starts)
    :param request: { id: str, countdown?: int, gameLength?: int }
    :return: True || error :D
    """
    pass


@api_view(["POST"])
def gm_stop(request):
    """
    Stops the game if requested by the GM
    - if countdown specified, update remaining game time to the countdown time
    - otherwise, end instantly
    :param request: { id: str, countdown?: int }
    :return: True || error :D
    """
    pass


##########################################
# Player endpoints
##########################################


@api_view(["POST"])
def register_Player(request):
    """
    Registers Player
    :param request: { id: str, name: str, questions-answers: [(string, string)] }
    :return: status code
    """
    pass


@api_view(["POST"])
def player_get_target(request):
    """
    Get next target for a player
    :param request: { id: str }
    :return: { question: str, expectedAnswer: str }
    """
    pass


@api_view(["POST"])
def player_scan(request):
    """
    Process player scanning another player's tag
    :param request: { id: str, scannedId: str }
    :return: True if successful; False otherwise
    """
    pass


##########################################
# General endpoints
##########################################


@api_view(["GET"])
def get_questions(request):
    """
    Get all questions
    :param request: empty
    :return: {questions: [str]}
    """
    return Response({'questions': questions.questions}, status=status.HTTP_200_OK)


@api_view(["GET"])
def score(request):
    """
    Get current game score
    :param request: empty
    :return: [{ id: str, score: int }]
    """
    pass
