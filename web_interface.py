import os
import asyncio
import threading
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from modules.config import Config
from modules.api_functions import APIFunctions
from modules.bot_nuker import setup_bot_commands

# Set working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Global state
config_manager = Config()
active_token = None
active_guild_id = None
api_instance = None
bot_instance = None
bot_thread = None


def log_to_web(message, type='info'):
    socketio.emit('log', {'message': message, 'type': type})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    tokens = config_manager._read_pairs(config_manager.token_file)
    guilds = config_manager._read_pairs(config_manager.guild_file)
    return jsonify({
        'tokens': tokens,
        'guilds': guilds,
        'active_token_masked': config_manager._mask_token(active_token) if active_token else None,
        'active_guild_id': active_guild_id,
    })


@app.route('/api/config/save_token', methods=['POST'])
def save_token():
    data = request.json or {}
    token = (data.get('token') or '').strip()
    name = (data.get('name') or '').strip()
    if not token:
        return jsonify({'status': 'error', 'message': 'Token manquant.'}), 400

    tokens = config_manager._read_pairs(config_manager.token_file)
    if not any(t[0] == token for t in tokens):
        tokens.append((token, name))
        config_manager._write_pairs(config_manager.token_file, tokens)
        log_to_web(f"Token '{name or config_manager._mask_token(token)}' sauvegardé.", 'success')
    return jsonify({'status': 'success'})


@app.route('/api/config/save_guild', methods=['POST'])
def save_guild():
    data = request.json or {}
    guild_id = (data.get('guild_id') or '').strip()
    name = (data.get('name') or '').strip()
    if not guild_id:
        return jsonify({'status': 'error', 'message': 'Guild ID manquant.'}), 400

    guilds = config_manager._read_pairs(config_manager.guild_file)
    if not any(g[0] == guild_id for g in guilds):
        guilds.append((guild_id, name))
        config_manager._write_pairs(config_manager.guild_file, guilds)
        log_to_web(f"Guild '{name or guild_id}' sauvegardée.", 'success')
    return jsonify({'status': 'success'})


@app.route('/api/config/set', methods=['POST'])
def set_config():
    global active_token, active_guild_id, api_instance
    data = request.json or {}
    active_token = (data.get('token') or '').strip()
    active_guild_id = (data.get('guild_id') or '').strip()

    if active_token and active_guild_id:
        api_instance = APIFunctions(active_token, active_guild_id)
        log_to_web(f"Configuration active pour le serveur {active_guild_id}.", 'success')
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Token ou Guild ID manquant.'}), 400


@app.route('/api/action/<action_name>', methods=['POST'])
def trigger_action(action_name):
    if not api_instance:
        return jsonify({'status': 'error', 'message': 'Non configuré'}), 400

    data = request.json or {}

    async def run_action():
        try:
            if action_name == 'delete_channels':
                log_to_web('Suppression des salons...', 'warning')
                chans = await api_instance.get_channels()
                await api_instance.delete_all_channels(chans)
            elif action_name == 'delete_roles':
                log_to_web('Suppression des rôles...', 'warning')
                roles = await api_instance.get_roles()
                await api_instance.delete_all_roles(roles)
            elif action_name == 'ban_members':
                log_to_web('Bannissement des membres...', 'warning')
                members = await api_instance.get_members()
                await api_instance.ban_all_members(members)
            elif action_name == 'delete_emojis':
                log_to_web('Suppression des emojis...', 'warning')
                await api_instance.delete_all_emojis()
            elif action_name == 'delete_stickers':
                log_to_web('Suppression des stickers...', 'warning')
                await api_instance.delete_all_stickers()
            elif action_name == 'create_channels':
                name = data.get('name', 'raid-by-diff')
                amount = int(data.get('amount', 10) or 10)
                log_to_web(f"Création de {amount} salons '{name}'...", 'warning')
                await api_instance.create_multiple_channels(name, amount)
            elif action_name == 'create_roles':
                name = data.get('name', 'diff-role')
                amount = int(data.get('amount', 10) or 10)
                log_to_web(f"Création de {amount} rôles '{name}'...", 'warning')
                await api_instance.create_multiple_roles(name, amount)
            elif action_name == 'spam_webhooks':
                web_name = data.get('name', 'NUKE BY DIFF-TOOL')
                web_msg = data.get('message', 'RAID BY DIFF-TOOL')
                msg_amt = int(data.get('amount', 5) or 5)
                log_to_web('Spam webhooks dans tous les salons...', 'warning')
                await api_instance.spam_all_webhooks(web_name, web_msg, msg_amt)
            elif action_name == 'edit_guild':
                new_name = data.get('name', 'NUKED BY DIFF')
                await api_instance.edit_guild(name=new_name)
            elif action_name == 'rename_bot':
                username = data.get('username', '').strip()
                if not username:
                    log_to_web('Nom de bot manquant.', 'error')
                else:
                    await api_instance.rename_bot(username=username)
            elif action_name == 'spam_direct':
                msg = data.get('message', '@everyone RAID')
                amt = int(data.get('amount', 5) or 5)
                log_to_web('Spam direct dans tous les salons...', 'warning')
                await api_instance.spam_all_channels_direct(msg, amt)
            elif action_name == 'dm_all':
                msg = data.get('message', 'RAIDED BY DIFF-TOOL')
                log_to_web('DM All en cours...', 'warning')
                await api_instance.dm_all_members_action(msg)
            else:
                log_to_web(f"Action inconnue: {action_name}", 'error')
                return
            log_to_web(f"Action {action_name} terminée avec succès.", 'success')
        except Exception as e:
            log_to_web(f"Erreur lors de {action_name}: {e}", 'error')

    threading.Thread(target=lambda: asyncio.run(run_action())).start()
    return jsonify({'status': 'success'})


@app.route('/api/bot/start', methods=['POST'])
def start_bot_nuker():
    global bot_instance, bot_thread
    if not active_token:
        return jsonify({'status': 'error', 'message': 'Token non configuré.'}), 400

    config = request.json or {}

    def run_bot():
        global bot_instance
        try:
            bot_instance = setup_bot_commands(config)
            bot_instance.run(active_token)
        except Exception as e:
            log_to_web(f"Erreur Bot: {e}", 'error')
            bot_instance = None

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    log_to_web('Mode Bot Nuker lancé !', 'success')
    return jsonify({'status': 'success'})


@app.route('/api/guild/stats')
def get_guild_stats():
    if not api_instance: return jsonify({'status': 'error'}), 400
    stats = asyncio.run(api_instance.get_server_stats())
    return jsonify(stats)


@app.route('/api/guild/members')
def get_guild_members():
    if not api_instance: return jsonify([]), 400
    members = asyncio.run(api_instance.get_full_members_list())
    return jsonify(members)


@app.route('/api/guild/roles')
def get_guild_roles():
    if not api_instance: return jsonify([]), 400
    roles = asyncio.run(api_instance.get_full_roles_list())
    return jsonify(roles)


def start_web_server(host='127.0.0.1', port=5000):
    socketio.run(app, port=port, debug=False, host=host)


if __name__ == '__main__':
    start_web_server()
