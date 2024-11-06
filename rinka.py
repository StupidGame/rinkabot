# main
#import
import discord
import os
import openai
import signal

import datetime

dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

 #langchain import
from langchain.prompts import (
  ChatPromptTemplate, 
  MessagesPlaceholder, 
  SystemMessagePromptTemplate, 
  HumanMessagePromptTemplate,
  AIMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

 #Discord initial
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#token and API seting
token = os.environ['TOKEN_RINKA']
openai.api_key = os.environ['OPENAI_API_KEY']

 #Discord event
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await client.change_presence(activity=discord.Game(name="!rinkaで呼べるよ"))

@client.event
async def on_message(message):
    if message.author.bot == True:
        return
    elif message.content.startswith('!rinka ') or message.content.startswith('!rinka　'):
      async with message.channel.typing():
        if(not os.path.isfile("settings.txt")):
          open("settings.txt", 'w', encoding="utf-8")
        f = open("settings.txt", 'r', encoding="utf-8").format(username=message.author.display_name, nowtime=dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
        system_settings = f.read()
        f.close()
        prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_settings),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}")
              ])

        use_model = "gpt-4o"
        S_conversation = ConversationChain(
        memory=ConversationSummaryBufferMemory(
                return_messages=True,
                llm=ChatOpenAI(model_name=use_model, temperature=0.75),
                max_token_limit=1000
                ),

          prompt=prompt,
          llm=ChatOpenAI(model_name=use_model),
          verbose=True
          )

# buffer load
        if(not os.path.isfile("." + os.sep + "memories" + os.sep + 'memory-' + str(message.author.id) + ".txt")):
          open("." + os.sep + "memories" + os.sep + 'memory-' + str(message.author.id) + ".txt", 'w', encoding="utf-8")
        f = open("." + os.sep + "memories" + os.sep + 'memory-' + str(message.author.id) + ".txt", 'r', encoding="utf-8")
        memory_text = f.read()
        f.close()
        S_conversation.predict(input=memory_text) 
        text = message.content[7::]
        S_text = S_conversation.predict(input=text) 
        await message.reply(S_text, mention_author=True)

        S_memory_text = S_conversation.memory.load_memory_variables({})
        Sf = open("." + os.sep + "memories" + os.sep + 'memory-' + str(message.author.id) + ".txt", 'w', encoding="utf-8")
        Sf.write(str(S_memory_text))
        Sf.close()
    
client.run(token)
