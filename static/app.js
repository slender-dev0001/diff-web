const SECTION_FIELDS = {
    general: ["workspace_name", "operator_name", "environment", "project_notes"],
    discord: ["bot_token", "token_note", "guild_id", "guild_note", "prefix", "bot_display_name", "activity_text"],
    server: ["server_display_name", "welcome_channel", "logs_channel", "banner_url"],
    channels: ["default_channel_name", "default_channel_count", "category_name", "topic_template"],
    roles: ["default_role_name", "default_role_count", "staff_role", "accent_role"],
    appearance: ["brand_color", "surface_color", "highlight_color", "status_label"],
};

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.add("show");
    window.clearTimeout(showToast._timer);
    showToast._timer = window.setTimeout(() => {
        toast.classList.remove("show");
    }, 2400);
}

function getSettingsFromForm() {
    const settings = {};
    for (const [section, fields] of Object.entries(SECTION_FIELDS)) {
        settings[section] = {};
        for (const field of fields) {
            const element = document.getElementById(field);
            settings[section][field] = element ? element.value : "";
        }
    }
    return settings;
}

function applySettingsToForm(settings) {
    for (const [section, fields] of Object.entries(SECTION_FIELDS)) {
        const values = settings[section] || {};
        for (const field of fields) {
            const element = document.getElementById(field);
            if (element) {
                element.value = values[field] ?? "";
            }
        }
    }
    updatePreview();
}

function updateCounters(tokens, guilds, presets) {
    document.getElementById("tokens-count").textContent = tokens.length;
    document.getElementById("guilds-count").textContent = guilds.length;
    document.getElementById("presets-count").textContent = presets.length;
}

function populateSelect(selectId, items, label) {
    const select = document.getElementById(selectId);
    select.innerHTML = "";

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = label;
    select.appendChild(placeholder);

    items.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.label;
        select.appendChild(option);
    });
}

function renderPresets(presets) {
    const wrapper = document.getElementById("preset-list");
    wrapper.innerHTML = "";

    if (!presets.length) {
        const empty = document.createElement("div");
        empty.className = "preset-chip";
        empty.textContent = "Aucun preset pour le moment";
        wrapper.appendChild(empty);
        return;
    }

    presets.forEach((name) => {
        const item = document.createElement("div");
        item.className = "preset-chip";

        const label = document.createElement("span");
        label.textContent = name;

        const button = document.createElement("button");
        button.type = "button";
        button.textContent = "Charger";
        button.addEventListener("click", () => loadPreset(name));

        item.appendChild(label);
        item.appendChild(button);
        wrapper.appendChild(item);
    });
}

function updatePreview() {
    const settings = getSettingsFromForm();
    const appearance = settings.appearance;

    document.documentElement.style.setProperty("--brand", appearance.brand_color || "#ff7a18");
    document.documentElement.style.setProperty("--surface", appearance.surface_color || "#151726");
    document.documentElement.style.setProperty("--highlight", appearance.highlight_color || "#38bdf8");

    document.getElementById("preview-status").textContent = appearance.status_label || "Draft setup";
    document.getElementById("preview-title").textContent = settings.general.workspace_name || "DIFF Studio";
    document.getElementById("preview-subtitle").textContent = settings.discord.activity_text || "Ready on localhost";
    document.getElementById("preview-server").textContent = settings.server.server_display_name || "Serveur non defini";
    document.getElementById("preview-prefix").textContent = `Prefix ${settings.discord.prefix || "!"}`;
    document.getElementById("preview-channel").textContent = `#${settings.channels.default_channel_name || "general"}`;
    document.getElementById("preview-role").textContent = `@${settings.roles.default_role_name || "member"}`;
    document.getElementById("preview-staff").textContent = `@${settings.roles.staff_role || "admin"}`;
}

async function refreshBootstrap() {
    const response = await fetch("/api/bootstrap");
    const data = await response.json();

    populateSelect("saved_token", data.tokens, "Selectionner un token");
    populateSelect("saved_guild", data.guilds, "Selectionner un guild");
    renderPresets(data.presets);
    updateCounters(data.tokens, data.guilds, data.presets);
    applySettingsToForm(data.settings);
}

async function saveWorkspace() {
    const response = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(getSettingsFromForm()),
    });
    const data = await response.json();
    showToast(data.message || "Configuration sauvegardee.");
}

async function saveToken() {
    const token = document.getElementById("bot_token").value.trim();
    const note = document.getElementById("token_note").value.trim();
    if (!token) {
        showToast("Ajoute un token avant de sauvegarder.");
        return;
    }

    const response = await fetch("/api/tokens", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, note }),
    });
    const data = await response.json();
    if (!response.ok) {
        showToast(data.message || "Erreur token.");
        return;
    }

    populateSelect("saved_token", data.tokens, "Selectionner un token");
    showToast("Token ajoute.");
}

async function saveGuild() {
    const guildId = document.getElementById("guild_id").value.trim();
    const note = document.getElementById("guild_note").value.trim();
    if (!guildId) {
        showToast("Ajoute un guild ID avant de sauvegarder.");
        return;
    }

    const response = await fetch("/api/guilds", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guild_id: guildId, note }),
    });
    const data = await response.json();
    if (!response.ok) {
        showToast(data.message || "Erreur guild.");
        return;
    }

    populateSelect("saved_guild", data.guilds, "Selectionner un guild");
    showToast("Guild ajoute.");
}

async function savePreset() {
    const name = document.getElementById("preset_name").value.trim();
    if (!name) {
        showToast("Choisis un nom de preset.");
        return;
    }

    const response = await fetch("/api/presets/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, settings: getSettingsFromForm() }),
    });
    const data = await response.json();
    if (!response.ok) {
        showToast(data.message || "Erreur preset.");
        return;
    }

    renderPresets(data.presets);
    document.getElementById("presets-count").textContent = data.presets.length;
    showToast(data.message || "Preset sauve.");
}

async function loadPreset(name) {
    const response = await fetch("/api/presets/load", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
    });
    const data = await response.json();
    if (!response.ok) {
        showToast(data.message || "Impossible de charger le preset.");
        return;
    }

    applySettingsToForm(data.settings);
    showToast(`Preset charge: ${name}`);
}

function bindSelectors() {
    document.getElementById("saved_token").addEventListener("change", (event) => {
        if (event.target.value) {
            document.getElementById("bot_token").value = event.target.value;
        }
    });

    document.getElementById("saved_guild").addEventListener("change", (event) => {
        if (event.target.value) {
            document.getElementById("guild_id").value = event.target.value;
        }
    });
}

function bindPreviewEvents() {
    Object.values(SECTION_FIELDS).flat().forEach((field) => {
        const element = document.getElementById(field);
        if (element) {
            element.addEventListener("input", updatePreview);
        }
    });
}

window.addEventListener("DOMContentLoaded", async () => {
    bindSelectors();
    bindPreviewEvents();

    document.getElementById("save-workspace").addEventListener("click", saveWorkspace);
    document.getElementById("save-token").addEventListener("click", saveToken);
    document.getElementById("save-guild").addEventListener("click", saveGuild);
    document.getElementById("save-preset").addEventListener("click", savePreset);

    await refreshBootstrap();
});
