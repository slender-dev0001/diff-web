import json
import os
from copy import deepcopy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIGS_DIR = os.path.join(DATA_DIR, "configs")
TOKEN_FILE = os.path.join(DATA_DIR, "token.txt")
GUILD_FILE = os.path.join(DATA_DIR, "guild.txt")
WEB_SETTINGS_FILE = os.path.join(DATA_DIR, "web_settings.json")


DEFAULT_SETTINGS = {
    "general": {
        "workspace_name": "DIFF Studio",
        "operator_name": "",
        "environment": "localhost",
        "project_notes": "",
    },
    "discord": {
        "bot_token": "",
        "token_note": "",
        "guild_id": "",
        "guild_note": "",
        "prefix": "!",
        "bot_display_name": "DIFF Assistant",
        "activity_text": "Ready on localhost",
    },
    "server": {
        "server_display_name": "",
        "welcome_channel": "welcome",
        "logs_channel": "logs",
        "banner_url": "",
    },
    "channels": {
        "default_channel_name": "general",
        "default_channel_count": "8",
        "category_name": "operations",
        "topic_template": "Workspace channel",
    },
    "roles": {
        "default_role_name": "member",
        "default_role_count": "4",
        "staff_role": "admin",
        "accent_role": "vip",
    },
    "appearance": {
        "brand_color": "#ff7a18",
        "surface_color": "#151726",
        "highlight_color": "#38bdf8",
        "status_label": "Draft setup",
    },
}


class Config:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(CONFIGS_DIR, exist_ok=True)
        self.token_file = TOKEN_FILE
        self.guild_file = GUILD_FILE
        self.web_settings_file = WEB_SETTINGS_FILE
        self.configs_dir = CONFIGS_DIR

    def _read_pairs(self, filename):
        pairs = []
        if not os.path.exists(filename):
            return pairs

        with open(filename, "r", encoding="utf-8") as handle:
            for line in handle:
                raw = line.strip()
                if not raw:
                    continue
                if "|" in raw:
                    key, note = raw.split("|", 1)
                else:
                    key, note = raw, ""
                pairs.append((key.strip(), note.strip()))
        return pairs

    def _write_pairs(self, filename, pairs):
        with open(filename, "w", encoding="utf-8") as handle:
            for key, note in pairs:
                handle.write(f"{key}|{note}\n")

    def _mask_token(self, token):
        if not token:
            return ""
        if len(token) <= 12:
            return token[:3] + "..." + token[-3:]
        return token[:7] + "..." + token[-5:]

    def _deep_merge(self, base, incoming):
        merged = deepcopy(base)
        for key, value in incoming.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = self._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _coerce_payload(self, payload):
        payload = payload or {}

        structured = {section: {} for section in DEFAULT_SETTINGS}

        for section in DEFAULT_SETTINGS:
            if isinstance(payload.get(section), dict):
                structured[section] = payload.get(section, {})

        legacy_map = {
            "prefix": ("discord", "prefix"),
            "channelsname": ("channels", "default_channel_name"),
            "rolename": ("roles", "default_role_name"),
            "num_channels": ("channels", "default_channel_count"),
            "num_roles": ("roles", "default_role_count"),
            "image_url": ("server", "banner_url"),
            "dm_message": ("general", "project_notes"),
            "spammessage": ("discord", "activity_text"),
        }

        for legacy_key, target in legacy_map.items():
            if legacy_key in payload:
                section, field = target
                structured[section][field] = payload[legacy_key]

        return structured

    def _normalize_settings(self, payload):
        merged = self._deep_merge(DEFAULT_SETTINGS, self._coerce_payload(payload))
        normalized = {}
        for section, values in merged.items():
            normalized[section] = {}
            for key, value in values.items():
                normalized[section][key] = "" if value is None else str(value)
        return normalized

    def list_tokens(self):
        return self._read_pairs(self.token_file)

    def list_guilds(self):
        return self._read_pairs(self.guild_file)

    def save_token(self, token, note=""):
        tokens = self.list_tokens()
        if any(existing == token for existing, _ in tokens):
            return
        tokens.append((token, note))
        self._write_pairs(self.token_file, tokens)

    def save_guild(self, guild_id, note=""):
        guilds = self.list_guilds()
        if any(existing == guild_id for existing, _ in guilds):
            return
        guilds.append((guild_id, note))
        self._write_pairs(self.guild_file, guilds)

    def load_web_settings(self):
        if not os.path.exists(self.web_settings_file):
            self.save_web_settings(DEFAULT_SETTINGS)

        with open(self.web_settings_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return self._normalize_settings(data)

    def save_web_settings(self, payload):
        settings = self._normalize_settings(payload)
        with open(self.web_settings_file, "w", encoding="utf-8") as handle:
            json.dump(settings, handle, indent=2, ensure_ascii=False)

    def list_presets(self):
        presets = []
        for name in os.listdir(self.configs_dir):
            if name.lower().endswith(".json"):
                presets.append(name)
        return sorted(presets)

    def save_preset(self, name, settings):
        safe_name = "".join(ch for ch in name if ch.isalnum() or ch in ("-", "_", " ")).strip()
        safe_name = safe_name or "preset"
        filename = safe_name.replace(" ", "_")
        if not filename.lower().endswith(".json"):
            filename += ".json"

        payload = self._normalize_settings(settings)
        with open(os.path.join(self.configs_dir, filename), "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        return filename

    def load_preset(self, name):
        path = os.path.join(self.configs_dir, name)
        if not os.path.exists(path):
            return self.load_web_settings()

        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return self._normalize_settings(data)
