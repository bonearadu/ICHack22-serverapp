# Create your views here.
from background_task import background
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json

from . import storage
from common.exception import CustomAPIException, ErrorCodes


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

    body_json = json.loads(request.body.decode("utf-8"))

    uid = body_json.get("uid", "")
    answers = body_json.get("answers", "")

    if uid in storage.all_players:
        raise CustomAPIException("User already created", ErrorCodes.REGISTER_ID_IN_USE)
    storage.Player(uid, 'name', answers)
    return Response({'uid': uid}, status=status.HTTP_200_OK)


@api_view(["POST"])
def login_player(request):
    """
    Registers Player
    :param request: { uid: str }
    :return: status code
    """

    body_json = json.loads(request.body.decode("utf-8"))

    uid = body_json.get("uid", "")

    if uid not in storage.all_players:
        raise CustomAPIException("User not created", ErrorCodes.USER_DOES_NOT_EXIST)
    user = storage.all_players[uid]
    return Response({'uid': uid, 'name': user.name, 'answers': user.answers,
                     'targets': map(lambda x: (storage.questions[x.question], x.answer, x.completed), user.target),
                     'game_started': storage.game_started}, status=status.HTTP_200_OK)


@api_view(["POST"])
def player_get_target(request):
    """
    Get next target for a player
    :param request: { uid: str }
    :return: { question: str, expectedAnswer: str }
    """

    body_json = json.loads(request.body.decode("utf-8"))

    uid = body_json.get("uid", "")

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

    body_json = json.loads(request.body.decode("utf-8"))

    uid = body_json.get("uid", "")
    scannedId = body_json.get("scannedId", "")
    question = body_json.get("question", "")
    answer = body_json.get("answer", "")

    user = storage.all_players[uid]
    return Response({'match': user.verify_answer(question, answer, scannedId), 'scorer': user.score},
                    status=status.HTTP_200_OK)


##########################################
# General endpoints
##########################################


@api_view(["POST"])
def start_game(request):
    """
    Starts a new game:
    - registerTime seconds for registering
    - gameTime seconds for playing
    :param request: { id: str, registerTime: int, gameTime: int }
    :return: status code
    """

    body_json = json.loads(request.body.decode("utf-8"))

    register_time = body_json.get("registerTime", "60")
    game_time = body_json.get("gameTime", "3600")

    storage.register_time = register_time
    storage.game_time = game_time
    storage.game_register = True

    __start_game(game_time, schedule=register_time)

    return Response()


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


##########################################
# Utils
##########################################


@background(schedule=60)
def __start_game(length):
    storage.game_register = False
    storage.game_started = True
    __end_game(schedule=length)


@background(schedule=3600)
def __end_game():
    storage.game_started = False
