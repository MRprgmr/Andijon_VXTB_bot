import asyncio

from aiogram import types, Bot
from rest_framework.response import Response
from rest_framework.views import APIView

from loader import dp

loop = asyncio.get_event_loop()


class UpdateBot(APIView):
    def post(self, request):
        try:
            Bot.set_current(dp.bot)
            update = types.Update(**request.data)
            loop.run_until_complete(dp.process_update(update))
        except Exception as e:
            print(e)
        finally:
            return Response(status=200)
