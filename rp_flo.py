import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import random
import re

# init bot
bot = telegram.Bot(token='273885113:AAHZkBtjHeoQw8a6-pWGgVL3jkVeBU5-2ok')
updates = bot.getUpdates()
updater = Updater(token='273885113:AAHZkBtjHeoQw8a6-pWGgVL3jkVeBU5-2ok')
dispatcher = updater.dispatcher

# utils

def GetUserName(User):
    user_fname = User.first_name
    user_lname = User.last_name
    user_name = user_fname + " " + user_lname

    if User.username != "":
        user_name = User.username

    return user_name

# X or DX or NDX or DX+Y or NDX+Y
def ParserDice(arg):
    # NDX+Y
    m = re.search(r"^(?P<N>\d+)[dD](?P<X>\d+)\+(?P<Y>\d+)$", arg)
    if m is not None:
        return [m.group('N'), m.group('X'), m.group('Y')]

    # NDX
    m = re.search(r"^(?P<N>\d+)[dD](?P<X>\d+)$", arg)
    if m is not None:
        return [m.group('N'), m.group('X'), -1]

    #DX+Y
    m = re.search(r"^[dD](?P<X>\d+)\+(?P<Y>\d+)$", arg)
    if m is not None:
        return [-1, m.group('X'), m.group('Y')]

    #DX
    m = re.search(r"^[dD](?P<X>\d+)$", arg)
    if m is not None:
        return [-1, m.group('X'), -1]

    #X
    m = re.search(r"^(?P<X>\d+)$", arg)
    if m is not None:
        return [-1, m.group('X'), -1]

    return [-1,-1,-1]

# command
def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Commands :\n\t* /help or /h : display this message.\n\t* /link_rp or /l : give the link to the google sheet.\n\t* /roll X [true|t|1] or /r X [true|t|1] : give a number (X or DX or NDX or DX+Y or NDX+Y) between 1 and X. . If true, t or 1, the command display all dices.")

def roll(bot, update, args):
    if len(args) < 1:
        bot.sendMessage(chat_id=update.message.chat_id, text="I need 1 or 2 arguments to roll a dice !")
        return

    if len(args) > 2:
        bot.sendMessage(chat_id=update.message.chat_id, text="I need 1 or 2 arguments to roll a dice ! No more please !")
        return

    User = update.message.from_user
    user_name = GetUserName(User)


    list_NXY = ParserDice(args[0])

    if list_NXY[1] == -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="I don't understand you ! You speak infernal ? (use /help)")
        return

    list_dice = []
    if list_NXY[0] != -1:
        rand = 0;
        for i in range(0,int(list_NXY[0])):
            tmp = random.randint(1, int(list_NXY[1]))
            list_dice.append(tmp)
            #list_dice[len(list_dice):] = [tmp]
            rand = rand + tmp
    else:
        rand = random.randint(1, int(list_NXY[1]))

    if list_NXY[0] == -1 and list_NXY[2] == -1:
        res = "for<b> " + user_name + "</b>  >> Dice(d" + str( list_NXY[1]) + ") : <b>" + str(rand) + "</b>"
    elif list_NXY[0] == -1 and list_NXY[2] != -1:
        res = "for<b> " + user_name + "</b>  >> Dice(d" + str( list_NXY[1]) + "+"+str(list_NXY[2])+") : <b>" + str(rand+int(list_NXY[2])) + "</b>"
    elif list_NXY[0] != -1 and list_NXY[2] == -1:
        res = "for<b> " + user_name + "</b>  >> Dice(" + str( list_NXY[0]) + "d" + str( list_NXY[1]) +") : <b>" + str(rand) + "</b>"
    elif list_NXY[0] != -1 and list_NXY[2] != -1:
        res = "for<b> " + user_name + "</b>  >> Dice(" + str( list_NXY[0]) + "d" + str( list_NXY[1])  + "+"+str(list_NXY[2])+") : <b>" + str(rand+int(list_NXY[2])) + "</b>"
    else:
        res = "Er..... WTF ???"

    if len(args) == 2 and (args[1] == "true" or args[1] == "t" or args[1] == "1"):
        res = res + "\nList of dices : ["
        for i in range(0, len(list_dice) - 1):
            res = res + str(list_dice[i]) +", "

        res = res + str(list_dice[len(list_dice) - 1]) + "]"

    bot.sendMessage(chat_id=update.message.chat_id, text=res, parse_mode=telegram.ParseMode.HTML)

def link_ggSheet(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="<b>Lien :</b> <a href='https://docs.google.com/spreadsheets/d/1J-gHN2BR3FM2tqnaIP5ExBzsXnMahFrCOG7xsRucGuY/edit#gid=0'>here</a>", parse_mode=telegram.ParseMode.HTML)
    #custom_keyboard = [[ "Yes","No"  ]]
    #reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    #bot.sendMessage(chat_id=update.message.chat_id, text="Stay here, I'll be back.", reply_markup=reply_markup)
    #reply_markup = telegram.ReplyKeyboardHide()
    #bot.sendMessage(chat_id=update.message.chat_id, text="I'm back.", reply_markup=reply_markup)

# vote system

list_vote = {}
b_vote = False

#"/vote descript c1 c2 c3 c4"
def createVote(bot, update, args):
    #print(b_vote)
    #if b_vote == True:
    bot.sendMessage(chat_id=update.message.chat_id, text="Keep focus, they are already a vote !")
    #    return

    if len(args) < 1:
        bot.sendMessage(chat_id=update.message.chat_id, text="I need 1 argument to create Vote !")
        return

    b_vote = True
    custom_keyboard = [[]]

    for i in range(1, len(args)):
        custom_keyboard.append(args[i])

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id,text="<b>Vote for </b> :\n" + args[0], parse_mode=telegram.ParseMode.HTML)
    bot.sendMessage(chat_id=update.message.chat_id, text="dkdkd", reply_markup=reply_markup)

def endVote(bot, update):
    b_vote = False;
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id, text="Vote finished.", reply_markup=reply_markup)

# setup CommandHandler

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

help_handler_short = CommandHandler('h', help)
dispatcher.add_handler(help_handler_short)

roll_handler = CommandHandler('roll', roll, pass_args=True)
dispatcher.add_handler(roll_handler)
roll_handler_short = CommandHandler('r', roll, pass_args=True)
dispatcher.add_handler(roll_handler_short)

linkGGS_handler = CommandHandler('link_rp', link_ggSheet)
dispatcher.add_handler(linkGGS_handler)
linkGGS_handler_short = CommandHandler('l', link_ggSheet)
dispatcher.add_handler(linkGGS_handler_short)

vote_handler = CommandHandler('vote', createVote, pass_args=True)
dispatcher.add_handler(vote_handler)

evote_handler = CommandHandler('vote_end', endVote)
dispatcher.add_handler(evote_handler)

updater.start_polling()
