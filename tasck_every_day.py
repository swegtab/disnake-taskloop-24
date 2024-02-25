import disnake
from disnake.ext import tasks

import asyncio
import datetime


SERVER_ID = id
CHANNEL_ID = id


class COG_Tasks(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.every_day.start()

	def cog_unload(self):
		self.every_day.cancel()

	@tasks.loop(hours = 24)
	async def every_day(self):
		try:
			now = datetime.datetime.now()
			future = datetime.datetime.now().replace(hour = 0, minute = 0)
			if now > future:
				future += datetime.timedelta(days = 1)
			await asyncio.sleep((future-now).total_seconds())


			guild = self.bot.get_guild(SERVER_ID)

			embed = disnake.Embed(title = f"Новый день начался - {guild.name}", color = 0xffffff)
			embed.set_image(url = f"https://media1.tenor.com/m/tw_h0SuqGz0AAAAC/crying-cry.gif")
			await self.bot.get_channel(CHANNEL_ID).send(embed = embed)

		except Exception as e:
			with open(r'logs.txt', 'a', encoding = 'utf-8') as file:
				file.write(f'LOG BOT ERROR < every_day > - {datetime.datetime.now()}\n{e}\n')

	@every_day.before_loop
	async def before_every_day(self):
		await self.bot.wait_until_ready()

def setup(bot):
	bot.add_cog(COG_Tasks(bot))
