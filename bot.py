import discord
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı yasaklamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanıcı {member.name} banlandı.")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Botun kendi mesajlarını işlememesi için

    if "https://" in message.content or "http://" in message.content:
        try:
            await message.channel.send(f"{message.author.mention}, bu sunucuda bağlantı paylaşmak yasaktır! 🚫")
            await message.author.ban(reason="Link paylaşımı yasak!")
        except discord.Forbidden:
            await message.channel.send("Kullanıcıyı banlamak için yetkim yok.")
        except discord.HTTPException:
            await message.channel.send("Kullanıcıyı banlarken bir hata oluştu.")

    await bot.process_commands(message)  # Diğer komutların çalışmasını sağlar

bot.run(token)
