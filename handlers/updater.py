import asyncio
import threading
import logging

from aiogram import types, Dispatcher, Bot
from rest_framework.response import Response
from rest_framework.views import APIView

from loader import dp

loop = asyncio.get_event_loop()


def process_request(request):
    update = types.Update(**request.data)
    Dispatcher.set_current(dp)
    Bot.set_current(dp.bot)
    loop.run_until_complete(dp.process_update(update))


class UpdateBot(APIView):
    def post(self, request):
        try:
            runner = threading.Thread(target=process_request, args=(request,))
            runner.start()
        except Exception as e:
            logging.info(e)
        finally:
            return Response(status=200)
