# Create your views here.
import pika
from background_task import background
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json

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

    body_json = json.loads(request.body.decode("utf-8"))

    gm_id = body_json.get("id", "")

    if id == "":
        raise CustomAPIException("Game Master ID required.", ErrorCodes.MISSING_ID)

    if storage.gm_id != -1:
        raise CustomAPIException("Game already started.", ErrorCodes.GAME_STARTED)
    storage.gm_id = gm_id

    return Response()


def __amqp_connect():
    connection = pika.BlockingConnection(
        pika.URLParameters(
            url="amqps://qgiyzrhi:UwJqIh9NWbDnScUqY3LSzQSAAx_VYjam@rattlesnake.rmq.cloudamqp.com/qgiyzrhi")
    )
    channel = connection.channel()
    channel.exchange_declare("broadcast", exchange_type="fanout")

    return connection, channel


@background(schedule=60)
def start():
    connection, channel = __amqp_connect()
    print("Broadcasting start message...")
    channel.basic_publish(exchange="broadcast", routing_key="", body="start")
    connection.close()


@background(schedule=60)
def stop():
    connection, channel = __amqp_connect()
    print("Broadcasting stop message...")
    channel.basic_publish(exchange="broadcast", routing_key="", body="stop")
    connection.close()


@api_view(["POST"])
def gm_start(request):
    """
    Starts the game if requested by GM
    - if countdown specified, players will see a countdown till the game starts
    - if gameLength specified, players will see a timer till the game ends (after it starts)
    :param request: { id: str, countdown?: int, gameLength?: int }
    :return: True || error :D
    """

    body_json = json.loads(request.body.decode("utf-8"))

    gm_id = body_json.get("id", "")
    countdown = body_json.get("countdown", "0")
    gameLength = body_json.get("gameLength", "")

    if gm_id == "":
        raise CustomAPIException("Game Master ID required.", ErrorCodes.MISSING_ID)

    if gm_id != storage.gm_id:
        raise CustomAPIException("ID does not belong to Game Master.", ErrorCodes.ID_NOT_GM)

    connection, channel = __amqp_connect()

    # send start message to players
    print("Broadcasting countdown message...")
    channel.basic_publish(exchange="broadcast", routing_key="", body="countdown {0}".format(countdown))
    start(schedule=int(countdown))

    if gameLength != "":
        # send stop message to players
        print("Broadcasting countndown message...")
        channel.basic_publish(exchange="broadcast", routing_key="", body="countdown {0}".format(gameLength))
        stop(schedule=int(gameLength))

    connection.close()
    return Response()


@api_view(["POST"])
def gm_stop(request):
    """
    Stops the game if requested by the GM
    - if countdown specified, update remaining game time to the countdown time
    - otherwise, end instantly
    :param request: { id: str, countdown?: int }
    :return: True || error :D
    """
    body_json = json.loads(request.body.decode("utf-8"))

    gm_id = body_json.get("id", "")
    countdown = body_json.get("countdown", "0")

    if gm_id == "":
        raise CustomAPIException("Game Master ID required.", ErrorCodes.MISSING_ID)

    connection, channel = __amqp_connect()

    print("Broadcasting countdown message...")
    channel.basic_publish(exchange="broadcast", routing_key="", body="countdown {0}".format(countdown))
    stop(schedule=int(countdown))

    connection.close()
    return Response()


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
                     'targets': map(lambda x: (storage.questions[x.question], x.answer), user.target),
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
