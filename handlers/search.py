from aiogram import Router, F
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InlineQueryResultAudio
from aiogram.filters import CommandStart
from vkpymusic import Service
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from vkpymusic import Playlist

service = Service.parse_config()

router = Router()


# def get_playlists_kb(playlists: list[Playlist]) -> InlineKeyboardMarkup:
#     keyboard = []
#     for playlist in playlists:
#         text = f'{playlist.title} — {playlist.description}'
#         data = f'{song.owner_id}_{song.track_id}'
#         keyboard.append([InlineKeyboardButton(text=text, callback_data=data)])
#     keyboard.append([InlineKeyboardButton(text='◀️', callback_data='back'),
#                      InlineKeyboardButton(text='1/?', callback_data='back'),
#                      InlineKeyboardButton(text='▶️', callback_data='forward'),])
#     return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(CommandStart())
async def search(message: Message):
    await message.answer('Привет! 🎵\n\n'
                         'Я — бот, который поможет тебе найти музыку из ВК в два клика! Просто:\n'
                         '1️⃣ Напиши мой ник в любом чате: @vk_inline_music_bot\n'
                         '2️⃣ Укажи название песни или исполнителя\n'
                         '3️⃣ Выбери нужный трек из списка\n\n'
                         'Нужный трек появится прямо перед тобой! 🔍🎶\n'
                         'Можешь попробовать прямо сейчас! 😊')


@router.inline_query(F.query == '')
async def none_query(query: InlineQuery):
    songs = service.get_popular(count=15)
    results = []
    for song in songs:
        results.append(InlineQueryResultAudio(
            id=song.track_id, audio_url=song.url, title=song.title, performer=song.artist, audio_duration=song.duration,
        ))
    await query.answer(results=results)


@router.inline_query()
async def get_song(query: InlineQuery):
    songs = service.search_songs_by_text(query.query, count=30)
    results = []
    if songs:
        for song in songs:
            results.append(InlineQueryResultAudio(
                id=song.track_id, audio_url=song.url, title=song.title, performer=song.artist, audio_duration=song.duration,
            ))
    else:
        results.append(
            InlineQueryResultArticle(
                type='article', id='404', title='Нет результатов 😨', description='Попробуйте изменить запрос'
            )
        )
    await query.answer(results=results, is_personal=False)
