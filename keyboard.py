from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/start'), KeyboardButton('/help'))
# kb.add(KeyboardButton('/help'))
kb.add(KeyboardButton('/zilliqa'),KeyboardButton('/rockx'), KeyboardButton('/ezil.me'))
kb.add(KeyboardButton('/wave'),KeyboardButton('/shardpool.io'), KeyboardButton('/valkyrie2'))
kb.add(KeyboardButton('/huobi staking'), KeyboardButton('/zilliqa2'), KeyboardButton('/moonlet.io'))
kb.add(KeyboardButton('/bountyblok'), KeyboardButton('/everstake.one'), KeyboardButton('/stakin'))
kb.add(KeyboardButton('/nodamatics.com'), KeyboardButton('/zilpay'), KeyboardButton('/avely finance'))
kb.add(KeyboardButton('/viewblock'), KeyboardButton('/atomicwallet'), KeyboardButton('/binance staking'))
kb.add(KeyboardButton('/luganodes'),KeyboardButton('/cex.io'),KeyboardButton('/blox-sdk staking'))
kb.add(KeyboardButton('/valkyrie investments'), KeyboardButton('/ignite dao'), KeyboardButton('/zillet'), )
kb.add(KeyboardButton('/staked'), KeyboardButton('/kucoin'), KeyboardButton('/hashquark'))

node_track_kb = ReplyKeyboardMarkup(resize_keyboard=True)
node_track_kb.add(KeyboardButton('/track'), KeyboardButton('/stop'))