from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import storage
from common.exception import CustomAPIException, ErrorCodes


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

    gm_id = request.POST.get("id", "")
    if id == "":
        return Response({"error": "Game Master ID required."}, status=status.HTTP_400_BAD_REQUEST)
    if storage.gm_id != -1:
        return Response({"error": "Game already started."}, status=status.HTTP_400_BAD_REQUEST)
    storage.gm_id = gm_id
    return Response()


@api_view(["POST"])
def gm_start(request):
    """
    Starts the game if requested by GM
    - if countdown specified, players will see a countdown till the game starts
    - if gameLength specified, players will see a timer till the game ends (after it starts)
    :param request: { id: str, countdown?: int, gameLength?: int }
    :return: True || error :D
    """

    gm_id = request.POST.get("id", "")
    countdown = request.POST.get("countdown", "")
    gameLength = request.POST.get("gameLength", "")

    if gm_id == "":
        return Response({"error": "Game Master ID required."}, status=status.HTTP_400_BAD_REQUEST)

    if countdown != "":
        # send countdown message to players
        pass

    # send start message to players

    if gameLength != "":
        # send gameLength message to players
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
    gm_id = request.POST.get("id", "")
    countdown = request.POST.get("countdown", "")

    if gm_id == "":
        return Response({"error": "Game Master ID required."}, status=status.HTTP_400_BAD_REQUEST)

    if countdown != "":
        # stop game in countdown seconds ...???
        pass

    # send stop message to players


##########################################
# Player endpoints
##########################################


@api_view(["POST"])
def register_player(request):
    """
    Registers Player
    :param request: { uid: str, name: str, answers: [string] }
    :return: status code
    """
    uid = request.POST.get("uid", "")
    name = request.POST.get("name", "")
    answers = request.POST.get("answers", "")

    if uid in storage.all_players:
        raise CustomAPIException("User already created", ErrorCodes.REGISTER_ID_IN_USE)
    storage.Player(uid, name, answers)
    return Response({'uid': uid}, status=status.HTTP_200_OK)


@api_view(["POST"])
def login_player(request):
    """
    Registers Player
    :param request: { uid: str}
    :return: status code
    """
    uid = request.POST.get("uid", "")

    if uid not in storage.all_players:
        raise CustomAPIException("User not created", ErrorCodes.USER_DOES_NOT_EXIST)
    user = storage.all_players[uid]
    return Response({'uid': uid, 'name': user.name, 'answers': user.answers,
                     'targets': map(lambda x: (storage.questions[x.question], x.answer), user.target)},
                    status=status.HTTP_200_OK)


@api_view(["POST"])
def player_get_target(request):
    """
    Get next target for a player
    :param request: { uid: str }
    :return: { question: str, expectedAnswer: str }
    """
    uid = request.POST.get("uid", "")

    user = storage.all_players[uid]
    question, answer = user.create_next_target()
    return Response({'question': question, 'answer': answer}, status=status.HTTP_200_OK)


@api_view(["POST"])
def player_scan(request):
    """
    Process player scanning another player's tag
    :param request: { id: str, scannedId: str, question: str, answer: str }
    :return: True if successful; False otherwise
    """
    uid = request.POST.get("uid", "")
    scannedId = request.POST.get("scannedId", "")
    question = request.POST.get("question", "")
    answer = request.POST.get("answer", "")

    uid = '1'
    user = storage.Player('1', 'r', ['1', '2', 'nu', 'Da', '3', '4'])
    user.target = [storage.Target(1, 'da')]
    scannedId = '1'
    question = 'What is your favourite food?'
    answer = 'da'
    user = storage.all_players[uid]
    return Response({'match': user.verify_answer(question, answer, scannedId), 'scorer': user.score}, status=status.HTTP_200_OK)


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
    return Response({'questions': storage.questions}, status=status.HTTP_200_OK)


@api_view(["GET"])
def score(request):
    """
    Get current game score
    :param request: empty
    :return: [{ id: str, score: int }]
    """
    scores = {}
    for uid in list(storage.all_players.keys()):
        scores[uid] = storage.all_players[uid].score
    return Response({'scores': scores}, status=status.HTTP_200_OK)


@api_view(["GET"])
def reset(request):
    """
    Get current game score
    :param request: empty
    :return: [{ id: str, score: int }]
    """
    storage.all_players = {}
    storage.all_answers = {}
    for i in range(0, len(storage.questions)):
        storage.all_answers[i] = []
    return Response({'ok': 'ok'}, status=status.HTTP_200_OK)
