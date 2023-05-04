__all__ = ['register_user_comands', 'bot_commands']
from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.filters.command import Command
from commands.bot_commands import bot_commands
from commands.start import start
from commands.help import help_comand



def register_user_comands(router: Router):
    #router.message.register(start, Command(commands=['start'])) - another variant
    router.message.register(start, CommandStart())
    router.message.register(help_comand, Command(commands=['help']))