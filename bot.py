from telegram.ext import Updater, CommandHandler
from pathlib import Path
from dotenv import load_dotenv
from fplanalyzer.fpl_api import get_league_users, get_player_gameweek_interval
from fplanalyzer.definitions import ERROR_MSG_GW, SCORING_COMMAND_PROMPT, ERROR_PLAYERS_LEAGUE, ERROR_FPL_API_GENERIC

import os, logging

def get_rankings_over_last_gameweeks(update, context):
    args = context.args
    if not (isinstance(args, list)) or len(args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=SCORING_COMMAND_PROMPT)
        return
    start, end = args
    if not start.isdigit() or not end.isdigit():
        context.bot.send_message(chat_id=update.effective_chat.id, text=SCORING_COMMAND_PROMPT)
        return

    try:
        users = get_league_users(os.getenv("LEAGUE_ID"))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_PLAYERS_LEAGUE)
        return

    user_scores = []
    try:
        user_scores = [(user.player_name, get_player_gameweek_interval(user.entry, int(start), int(end))) for user in users]
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_MSG_GW)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_FPL_API_GENERIC)

    user_scores.sort(key=lambda x:x[1], reverse=True)
    user_scores_msgs = [f"{idx + 1}. {tup[1]} ({tup[0]})" for idx, tup in enumerate(user_scores)]
    context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(user_scores_msgs))

def main():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('scoring', get_rankings_over_last_gameweeks))
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()
