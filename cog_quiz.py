import discord
from discord.ext import commands
from random import *
from main import prefix


class Quiz(commands.Cog):
    def __init__(self,client):
        self.client = client

        
    @commands.command()
    async def quiz(self,ctx,theme=""):
        if theme == "" or theme == "menu":
            await Quiz.menu(self,ctx)
        elif theme == "add":
            await Quiz.quiz_add(self,ctx)
        else:
            if theme == "random" :
                random = True
                file_hist = open("txt_files/questions_histoire.txt","r",encoding="utf8")
                max_hist = int(len(file_hist.readlines())/10)
                file_hist.close()
                file_geo = open("txt_files/questions_geographie.txt","r",encoding="utf8")
                max_geo = int(len(file_geo.readlines())/10)
                file_geo.close()
                file_sciences = open("txt_files/questions_sciences.txt","r",encoding="utf8")
                max_sciences = int(len(file_sciences.readlines())/10)
                file_sciences.close()
                max_ttl = max_hist + max_geo + max_sciences
                x = randint(0,max_ttl)
                if x <= max_hist :
                    theme = "histoire"
                elif x <= max_hist + max_geo :
                    theme = "geographie"
                else:
                    theme = "sciences"
            else:
                random = False
            if theme == "geographie" :
                title = "**__QUIZ : Géographie__** :map:"
                file = open("txt_files/questions_geographie.txt","r",encoding="utf8")
            elif theme == "histoire" :
                title = "**__QUIZ : Histoire__ :statue_of_liberty:**"
                file = open("txt_files/questions_histoire.txt","r",encoding="utf8")
            elif theme == "sciences" :
                title = "**__QUIZ : Sciences__** :atom:"
                file = open("txt_files/questions_sciences.txt","r",encoding="utf8")
            else:
                await ctx.send(f"Il n'existe pas de catégorie de quiz nommée `{theme}`. Pour voir toutes les catégories de quiz disponibles, faites afficher le menu en tapant `{prefix}quiz`.")
            lines = file.readlines()
            file.close()
            max = int(len(lines)/10)
            x = randint(0,max)
            question = lines[10*x]
            rep_0 = lines[10*x+1]
            rep_1 = lines[10*x+2]
            rep_2 = lines[10*x+3]
            rep_3 = lines[10*x+4]
            exp = lines[10*x+5]
            list = [rep_0,rep_1,rep_2,rep_3]
            shuffle(list)
            if list[0] == rep_0 :
                correct_react = "🇦"
            elif list[1] == rep_0 :
                correct_react = "🇧"
            elif list[2] == rep_0 :
                correct_react = "🇨"
            elif list[3] == rep_0 :
                correct_react = "🇩"
            message = await ctx.send(f">>> {title}\n\n{question} \n :regional_indicator_a: {list[0]} :regional_indicator_b: {list[1]} :regional_indicator_c: {list[2]} :regional_indicator_d: {list[3]}")
            await message.add_reaction("\U0001F1E6")
            await message.add_reaction("\U0001F1E7")
            await message.add_reaction("\U0001F1E8")
            await message.add_reaction("\U0001F1E9")
            @self.client.event
            async def on_reaction_add(reaction,user):
                if user == self.client.user or reaction.message.id != message.id :
                    return ()
                else:
                    if str(reaction.emoji) == correct_react :
                        await message.clear_reactions()
                        congrats = await ctx.send(f"Bonne réponse {user.mention} ! :clap: \n{exp}")
                        await congrats.add_reaction("\U0001F504")
                        @self.client.event
                        async def on_reaction_add(reaction2,user):
                            if user == self.client.user or reaction2.message.id != congrats.id :
                                return ()
                            else:
                                await congrats.clear_reactions()
                                if random:
                                    await Quiz.quiz(self,ctx,"random")
                                else:
                                    await Quiz.quiz(self,ctx,theme)
                    else :
                        await ctx.send(f"Mauvaise réponse {user.mention} ! :no_entry_sign:")
                        await message.remove_reaction(reaction, user)


    async def menu(self,ctx):
        user0 = ctx.author.id
        embed=discord.Embed(title="Quiz - Menu", description="Il existe plusieurs catégories de Quiz différentes. Il est également possible de défier d'autres joueurs. \nQue souhaites-tu faire <@{}> ?".format(user0), color=0x318ec4)
        embed.add_field(name="Catégories", value=":game_die: Aléatoire \n:statue_of_liberty: Histoire \n:map: Géographie \n:atom: Sciences", inline=True)
        embed.add_field(name="Interactions", value=":crossed_swords: Multijoueur \n:satellite: Ajouter des questions", inline=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("\U0001F3B2")
        await message.add_reaction("\U0001F5FD")
        await message.add_reaction("\U0001F5FA")
        await message.add_reaction("\U0000269B")
        await message.add_reaction("\U00002694")
        await message.add_reaction("\U0001F4E1")
        @self.client.event
        async def on_reaction_add(reaction,user):
            if user == self.client.user or reaction.message.id != message.id :
                pass
            else :
                await message.clear_reactions()
                if str(reaction.emoji) == "🎲":   #Aléatoire
                    await Quiz.quiz(self,ctx,"random")
                elif str(reaction.emoji) == "🗽":   #Histoire
                    await Quiz.quiz(self,ctx,"histoire")
                elif str(reaction.emoji) == "🗺":   #Géographie
                    await Quiz.quiz(self,ctx,"geographie")
                elif str(reaction.emoji) == "⚛":    #Sciences
                    await Quiz.quiz(self,ctx,"sciences")
                elif str(reaction.emoji) == "⚔":    #Battle
                    await Quiz.multiplayer(self,ctx)
                elif str(reaction.emoji) == "📡" :    #Ajouter des questions
                    await Quiz.add_questions(self,ctx)


    async def add_questions(self,ctx):
        user0 = ctx.author
        channel = ctx.channel
        msg_cat = await ctx.send(">>> **__QUIZ - Ajouter une question__** (1/7)\n\nDans quelle catégorie souhaites-tu ajouter une question ? \n \n:statue_of_liberty: Histoire \n:map: Géographie \n:atom: Sciences")
        await msg_cat.add_reaction("\U0001F5FD")
        await msg_cat.add_reaction("\U0001F5FA")
        await msg_cat.add_reaction("\U0000269B")
        @commands.Cog.listener()
        async def on_reaction_add(self,reaction, user):
            if user == user0 and reaction.message.id == msg_cat.id:
                await msg_cat.delete()
                if str(reaction.emoji) == "🗽":
                    file = open("txt_files/questions_histoire.txt","a",encoding="utf8")
                    cat = "Histoire"
                    f_name = "questions_histoire.txt"
                elif str(reaction.emoji) == "🗺":
                    file = open("txt_files/questions_geographie.txt","a",encoding="utf8")
                    cat = "Géographie"
                    f_name = "questions_geographie.txt"
                elif str(reaction.emoji) == "⚛":
                    file = open("txt_files/questions_sciences.txt","a",encoding="utf8")
                    cat = "Sciences"
                    f_name = "questions_sciences.txt"
                else :
                    pass
                question = ""
                rep_0 = ""
                rep_1 = ""
                rep_2 = ""
                rep_3 = ""
                exp = ""
                l_var = [question, rep_0, rep_1, rep_2, rep_3, exp]
                msg_0 = '>>> **__QUIZ - Ajouter une question__** (2/7)\n\nÉcris **la question** directement dans le tchat (en la mettant éventuellement en forme si tu le souhaites). {} \nPour  la commande, écris : ``.\n\n```py\ncategorie = "{}"\nquestion = *en attente*\nrep_0 =\nrep_1 =\nrep_2 =\nrep_3 =\nexp =\n```'
                msg_1 = '>>> **__QUIZ - Ajouter une question__** (3/7)\n\nÉcris **LA bonne réponse** à la question dans le tchat. {} \nPour  la commande, écris : ``.\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = *en attente*\nrep_1 =\nrep_2 =\nrep_3 =\nexp =\n```'
                msg_2 = '>>> **__QUIZ - Ajouter une question__** (4/7)\n\nÉcris une 2ème proposition de réponse (fausse) dans le tchat. {}\nPour  la commande, écris : ``.\n\n*(N.B.: L\'ordre dans lequel les réponses sont données n\'a aucune importance)*\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = "{}"\nrep_1 = *en attente*\nrep_2 =\nrep_3 =\nexp =\n```'
                msg_3 = '>>> **__QUIZ - Ajouter une question__** (5/7)\n\nÉcris une 3ème proposition de réponse (fausse) dans le tchat. {}\nPour  la commande, écris : ``.\n\n*(N.B.: L\'ordre dans lequel les réponses sont données n\'a aucune importance)*\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = "{}"\nrep_1 = "{}"\nrep_2 = *en attente*\nrep_3 =\nexp =\n```'
                msg_4 = '>>> **__QUIZ - Ajouter une question__** (6/7)\n\nÉcris une 4ème et dernière proposition de réponse (fausse) dans le tchat. {}\nPour  la commande, écris : ``.\n\n*(N.B.: L\'ordre dans lequel les réponses sont données n\'a aucune importance)*\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = "{}"\nrep_1 = "{}"\nrep_2 = "{}"\nrep_3 = *en attente*\nexp =\n```'
                msg_5 = '>>> **__QUIZ - Ajouter une question__** (7/7)\n\nÉcris une explication, qui s\'affichera si la bonne réponse est trouvée. {} \nPour  la commande, écris : ``.\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = "{}"\nrep_1 = "{}"\nrep_2 = "{}"\nrep_3 = "{}"\nexp = *en attente*\n```'
                l_msg = [msg_0, msg_1, msg_2, msg_3, msg_4, msg_5]
                def check(m):
                    return m.author == user0 and m.channel == channel
                for i in range(6):
                    msg_bot = await ctx.send(l_msg[i].format(user0.mention, cat, l_var[0], l_var[1], l_var[2], l_var[3], l_var[4]))
                    message = await client.wait_for("message", check=check)
                    await msg_bot.delete()
                    await message.delete()
                    if message.content == "cancel":
                        return ()
                    else:
                        l_var[i]=message.content
                file.write("\n{}\n{}\n{}\n{}\n{}\n{}\n\n\n\n".format(l_var[0],l_var[1],l_var[2],l_var[3],l_var[4],l_var[5]))
                file.close()
                file = open(f"txt_files/{f_name}","r",encoding="utf8")
                lines = len(file.readlines())
                file.close()
                line_min = lines - 8
                line_max = lines - 3
                await ctx.send('>>> **__QUIZ - Ajouter une question__**\n\nUne nouvelle question a été ajoutée à `{}` (ligne `{}` à ligne `{}`) ! :smiley:\n<@406755214352318477>\n\n```py\ncategorie = "{}"\nquestion = "{}"\nrep_0 = "{}"\nrep_1 = "{}"\nrep_2 = "{}"\nrep_3 = "{}"\nexp = "{}"\n```'.format(f_name, line_min, line_max, cat, l_var[0], l_var[1], l_var[2], l_var[3], l_var[4], l_var[5]))
            else:
                pass




def setup(client):
    client.add_cog(Quiz(client))
