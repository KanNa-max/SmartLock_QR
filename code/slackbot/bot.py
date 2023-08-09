from slackbot.bot import Bot

# SlackBot起動

def main():
    doorlock_bot = Bot()
    doorlock_bot.run()

if __name__ == "__main__":
    print('start slackbot')
    main()