import html
import json

from typing import Optional, List

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram.error import BadRequest
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters, MessageHandler
from telegram.utils.helpers import mention_markdown, mention_html, escape_markdown

import Dingdi.modules.sql.welcome_sql as sql
from Dingdi import dispatcher, LOGGER
from Dingdi.modules.helper_funcs.chat_status import user_admin, can_delete
from Dingdi.modules.log_channel import loggable


@run_async
@user_admin
@loggable
def rem_cmds(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]

    if not args:
        del_pref = sql.get_cmd_pref(chat.id)
        if del_pref:
            update.effective_message.reply_text("Currently @bluetextbot commands are not deleted.")
        else:
            update.effective_message.reply_text("Currently @bluetextbot commands are not deleted.")
        return ""

    if args[0].lower() in ("on", "yes"):
        sql.set_cmd_joined(str(chat.id), True)
        update.effective_message.reply_text("Awle, @DingdiNews hmingin a dik eğğ!")
        return "<b>{}:</b>" \
               "\n#ANTI_COMMAND" \
               "\n<b>Admin:</b> {}" \
               "\nHas toggled @AntiCommandBot to <code>ON</code>.".format(html.escape(chat.title),
                                                                         mention_html(user.id, user.first_name))
    elif args[0].lower() in ("off", "no"):
        sql.set_cmd_joined(str(chat.id), False)
        update.effective_message.reply_text("Group Command, @DingdiSupport hmingin a in off e.!")
        return "<b>{}:</b>" \
               "\n#ANTI_COMMAND" \
               "\n<b>Admin:</b> {}" \
               "\nHas toggled @AntiCommandBot to <code>OFF</code>.".format(html.escape(chat.title),
                                                                          mention_html(user.id, user.first_name))
    else:
        # idek what you're writing, say yes or no
        update.effective_message.reply_text("AntiCommand i dah duh chuan... 'on/yes' i dah duh loh chuan 'off/no' tiin lo thawn rawh!")
        return ""

@run_async
def rem_slash_commands(bot: Bot, update: Update) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]
    del_pref = sql.get_cmd_pref(chat.id)

    if del_pref:
        try:
            msg.delete()
        except BadRequest as excp:
            LOGGER.info(excp)


__help__ = """
I remove messages starting with a /command in groups and supergroups.
- /rmcmd <on/off>: when someone tries to send a @BlueTextBot message, I will try to delete that!
"""

__mod_name__ = "Anticommand"

DEL_REM_COMMANDS = CommandHandler("rmcmd", rem_cmds, pass_args=True, filters=Filters.group)
REM_SLASH_COMMANDS = MessageHandler(Filters.command & Filters.group, rem_slash_commands)

dispatcher.add_handler(DEL_REM_COMMANDS)
dispatcher.add_handler(REM_SLASH_COMMANDS)
