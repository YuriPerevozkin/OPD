import os
import json
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = os.getenv("TOKEN")
SUBJECTS = ["Математика", "Русский", "Физика", "История"]
ADMIN_IDS = [6722685620]

logging.basicConfig(level=logging.INFO)

session = AiohttpSession(proxy="socks5://127.0.0.1:9150")

dp = Dispatcher()
bot = Bot(token=TOKEN, session=session)


@dp.message(Command("add_student"))
async def add_student(message: Message, command: Command):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Эта команда только для админов")
        return

    if command.args is None:
        await message.answer("Необходимо указать ФИО студента через пробел")
        return

    args = command.args.split()

    if len(args) < 3:
        await message.answer("Необходимо указать ФИО студента через пробел")
        return

    full_name = f"{args[0]} {args[1]} {args[2]}"

    with open("stats.json", "r") as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            stats = []

        subjects_item = {}
        for i in SUBJECTS:
            subjects_item[i] = []

        stats.append({"name": full_name, "grades": subjects_item})

    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)


@dp.message(Command("get_means"))
async def get_means(message: Message, command: Command):
    if command.args is None:
        await message.answer("Укажите ФИО студента полность")

    args = command.args.split()

    if len(args) < 3:
        await message.answer("Укажите ФИО студента полность")
        return

    full_name = f"{args[0]} {args[1]} {args[2]}"

    with open("stats.json", "r") as f:
        stats = json.load(f)

    found = False
    for i in stats:
        if i["name"].lower() == full_name.lower():
            found = True
            msg = ""
            for j in SUBJECTS:
                try:
                    mean_grade = sum(i['grades'][j]) / len(i["grades"][j])
                except ZeroDivisionError:
                    mean_grade = 0
                msg += f"Средняя оценка ({j}): {mean_grade}\n"
            await message.answer(msg)
    if not found:
        await message.answer("Ученик не найден")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
