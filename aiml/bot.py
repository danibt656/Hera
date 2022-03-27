import aiml
import os

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

# kernel now ready for use
while True:
    message = input("Enter your message to the bot: ")
    if message.lower() == "quit":
        exit()
    elif message.lower() == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message)
        print(bot_response)