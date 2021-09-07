from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random

from cards.user import User
from cards.game import Game
from cards.encoder import EnhancedJSONEncoder
from cards.constants import MODE_PICK_FROM_HOLD
from cards.constants import MODE_PICK_FROM_HAND
from cards.constants import MODE_LOBBY
from cards.constants import MAX_PLAYERS
from cards.constants import BOT_NAMES
from cards.card_pile import CardPile

active_games = {}


@csrf_exempt
def create_game_view(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)

    characters = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    game_code = ''
    for i in range(5):
        game_code += random.choice(characters)

    data = {'game_code': game_code}
    name = request_object['user_name']
    user = User(name=name,
                hand=CardPile(),
                hold=CardPile(),
                pile1=CardPile(),
                pile2=CardPile(),
                pile3=CardPile(),
                computer=0)
    game = Game(user_list={name: user},
                game_code=game_code,
                mode='Lobby',
                cards=CardPile(),
                discard=CardPile(),
                round=1)
    active_games[game_code] = game

    return JsonResponse(data, safe=False)


def list_games(request):
    data = json.dumps(active_games, cls=EnhancedJSONEncoder)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def get_game_view(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)

    game_code = request_object['game_code']
    game = active_games[game_code]

    data = json.dumps(game, cls=EnhancedJSONEncoder)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def join_game_view(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)

    game_code = request_object['game_code']
    user_name = request_object['user_name']

    if game_code not in active_games:
        data = {'error': 'No such game'}
        return JsonResponse(data, safe=False)

    game = active_games[game_code]

    if len(game.user_list) >= MAX_PLAYERS:
        data = {'error': 'Game filled'}
        return JsonResponse(data, safe=False)

    if game.mode != MODE_LOBBY:
        data = game
        return JsonResponse(data, safe=False)

    user = User(name=user_name,
                hand=CardPile(),
                hold=CardPile(),
                pile1=CardPile(),
                pile2=CardPile(),
                pile3=CardPile(),
                computer=0)

    game.user_list[user_name] = user

    data = json.dumps(game, cls=EnhancedJSONEncoder)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def start_game_view(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)

    game_code = request_object['game_code']
    game = active_games[game_code]
    if game.mode == MODE_LOBBY:
        game.mode = MODE_PICK_FROM_HAND
        result = game
        game.shuffle()
        game.deal()
        game.computer_move()
    else:
        result = game

    data = json.dumps(result, cls=EnhancedJSONEncoder)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def move_to_hold_view(request):
    try:
        my_json = request.body.decode('utf8')
        request_object = json.loads(my_json)
        user_name = request_object['user_name']
        game_code = request_object['game_code']
        card_id = request_object['card']
        game = active_games[game_code]
        user_list = game.user_list
        user = user_list[user_name]
        hold = user.hold

        if game.mode == MODE_PICK_FROM_HAND and len(hold) < 2:
            hand = user.hand
            card = user.hand.get_card_by_id(card_id)
            if card:
                hand.remove(card)
                hold.append(card)

                change_mode = True
                for user_name in game.user_list:
                    user = user_list[user_name]
                    if len(user.hold) != 2:
                        change_mode = False

                if change_mode:
                    game.mode = MODE_PICK_FROM_HOLD

                game.computer_move()
                data = json.dumps(game, cls=EnhancedJSONEncoder)

            else:
                data = {'error': 'No such card'}
                print(f"Error in move_to_hold_view, tried to move card {card_id} for {user_name}, but no such card exists.")

        else:
            data = {'error': 'Invalid move'}

        return HttpResponse(data, content_type="application/json")

    except Exception as e:
        print("ERROR {e}")
        data = {'error': 'Exception '}
        return HttpResponse(data, content_type="application/json")

@csrf_exempt
def move_to_pile_view(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)
    game_code = request_object['game_code']
    user_name = request_object['user_name']
    card_id = request_object['card']
    pile = request_object['pile']

    game = active_games[game_code]

    data = game.move_to_pile(user_name, card_id, pile)

    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_computer_player(request):
    my_json = request.body.decode('utf8')
    request_object = json.loads(my_json)
    game_code = request_object['game_code']
    game = active_games[game_code]

    # Pick a bot name
    success = False
    while not success:
        bot_no = random.randrange(len(BOT_NAMES))
        user_name = BOT_NAMES[bot_no]
        if user_name not in game.user_list:
            success = True

    user = User(name=user_name,
                hand=CardPile(),
                hold=CardPile(),
                pile1=CardPile(),
                pile2=CardPile(),
                pile3=CardPile(),
                computer=1)

    game.user_list[user_name] = user
    data = json.dumps(game, cls=EnhancedJSONEncoder)
    return HttpResponse(data, content_type="application/json")
