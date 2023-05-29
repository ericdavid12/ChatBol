from random import randint
import discord
from discord import app_commands

id_do_servidor = 1104784002822443108  # Id do servidor


class client(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild=discord.Object(id=id_do_servidor))
      self.synced = True
    print(f"{self.user} está online.")


aclient = client()
tree = app_commands.CommandTree(aclient)

total_partidas = 8
lista = ["Botafogo", "Palmeiras", "São Paulo", "Atlético-MG", "Grêmio"]
lista_min = [time.lower() for time in lista]

#                        Pts  V  E  D
tabela = [[1, "Botafogo", 21, 7, 0, 1],
          [2, "Palmeiras", 16, 4, 4, 0],
          [3, "São Paulo", 15, 4, 3, 1],
          [4, "Atlético-MG", 14, 4, 2, 2],
          [5, "Grêmio", 14, 4, 2, 2]]

times_results = {'Palmeiras': {
                                'partidas' : total_partidas,
                                'gols_feitos': 2.1 * total_partidas,
                                'gols_sofridos' : 0.9 * total_partidas,
                                'chute_a_gol' : 5.5 * total_partidas,
                                'posse_de_bola' : 0.560
                              },
                 'Botafogo' : {
                                'partidas' : total_partidas,
                                'gols_feitos' : 2.0 * total_partidas,
                                'gols_sofridos' : 0.8 * total_partidas,
                                'chute_a_gol' : 5.0 * total_partidas,
                                'posse_de_bola' : 0.416
                              },
                 'São Paulo' : {   
                                'partidas' : total_partidas,
                                'gols_feitos' : 1.8 * total_partidas,
                                'gols_sofridos' : 0.9 * total_partidas,
                                'chute_a_gol' : 4.9 * total_partidas,
                                'posse_de_bola' : 0.593
                               },
                 'Atlético-Mg' : {
                                  'partidas' : total_partidas,
                                  'gols_feitos' : 1.5 * total_partidas,
                                  'gols_sofridos' : 0.9 * total_partidas,
                                  'chute_a_gol' : 5.6 * total_partidas,
                                  'posse_de_bola' : 0.611
                                 },
                 'Grêmio' : {
                             'partidas' : total_partidas,
                             'gols_feitos' : 1.5 * total_partidas,
                             'gols_sofridos' : 1.4 * total_partidas,
                             'chute_a_gol' : 5.0 * total_partidas,
                             'posse_de_bola' : 0.560
                            }
                }


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='previsão',
              description='Relaciona dois adversários do brasileirão. Informe o nome do time apenas com letras minusculas!')
async def command_0(interaction: discord.Interaction, time: str, timeadv: str):
  time = time.lower()
  timeadv = timeadv.lower()
  
  if time and timeadv in lista_min:
    time = time.title()
    timeadv = timeadv.title()
    
    # TODOS OS VALORES MULTIPLICADOS PELO NÚMERO TOTAL DE PARTIDAS
    # Fórmula time A: ((gols_feitos * chute_a_gol) / gols_sofridos) * posse_de_bola
    chanceTime = ((times_results[time]['gols_feitos'] * times_results[time]['chute_a_gol']) / times_results[time]['gols_sofridos']) * times_results[time]['posse_de_bola']

    chanceTimeAdv = ((times_results[timeadv]['gols_feitos'] * times_results[timeadv]['chute_a_gol']) / times_results[timeadv]['gols_sofridos']) * times_results[timeadv]['posse_de_bola']

    if (chanceTime + chanceTimeAdv) > 100:
      diference = ((chanceTime + chanceTimeAdv) - 100) / 2
      chanceTime -= diference
      chanceTimeAdv -= diference
    
      await interaction.response.send_message(
        f"As chances dos times serão:\n\n{time.title()} - {chanceTime:.2f}%\n\t\tVS\n{timeadv.title()} - {chanceTimeAdv:.2f}%\n\nBoa sorte!",
        ephemeral=False)

    else:
      await interaction.response.send_message(
        f"As chances dos times serão:\n\n{time.title()} - {chanceTime:.2f}%\n\t\tVS\n{timeadv.title()} - {chanceTimeAdv:.2f}%\n\nEmpate - {100 - (chanceTime + chanceTimeAdv):.2f}%\n\nBoa sorte!",
        ephemeral=False)
    
  elif time and timeadv not in lista_min:
    await interaction.response.send_message(f"PUTS! O time {time.capitalize()} e o time {timeadv.capitalize()} não estão relacionados.\nOu, não fazem parte do campeonato.")
    
  elif timeadv not in lista_min:
    await interaction.response.send_message(f"PUTS! O time {timeadv.capitalize()} não está relacionado.\nOu, não faz parte do campeonato.")
    
  else:
    await interaction.response.send_message(f"PUTS! O time {time.capitalize()} não está relacionado.\nOu, não faz parte do campeonato.")


@tree.command(
  guild=discord.Object(id=id_do_servidor),
  name='dado',
  description=
  'Joga um dado com lados informados pelo usuário. [1 - 100] (APENAS UM TESTE)'
)
async def comand_1(interaction: discord.Interaction, lados: int):
  if lados > 100:
    await interaction.response.send_message(
      "O valor deve ser menor ou igual a 100!", ephemeral=True)
    
  elif lados < 0:
    await interaction.response.send_message("O valor deve ser maior do que 0!",
                                            ephemeral=True)
    
  elif lados == 0:
    await interaction.response.send_message(
      "Sério que você quer roletar um dado de 0 lados?\nEsperava que iria sair o que, um valor foda? ._.",
      ephemeral=True)
    
  else:
    dadin = randint(1, lados)
    await interaction.response.send_message(
      f"{interaction.user.name} roletou d{lados} um e tirou: {dadin}",
      ephemeral=False)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='lista-de-times',
              description='Mostra a lista atual de times do Brasileirão.')
async def comand_2(interaction: discord.Interaction):
  message = ''
  for item in lista:
    message += item
    message += "\n"

  await interaction.response.send_message(message)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='tabela',
              description='Tabela de classificação do Brasileirão.')
async def comand_3(interaction: discord.Interaction):
  t = "ㅤㅤ# \t\t\t\t Time \t\t\t\t Pts\t\t\t\t\tVIT\t\t\t\t\tE \t\t\t\t\tDER\n"
  t += '-' * 80
  t += '\n'
  for i in range(len(tabela)):
    for j in range(len(tabela[i])):
      space = 15
      space_left = space - len(str(tabela[i][j]))
      t += "%10s" %str(tabela[i][j])
      t += " " * space_left
    t += "\n"
    
  # Enviar a mensagem de resposta com a tabela de classificação
  await interaction.response.send_message(t)

aclient.run(
  'Token da Aplicação')