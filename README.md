# 🛠️ Installation Guide — Pin aionanoleaf Fork

This guide explains how to install and use the **Pin aionanoleaf Fork** custom integration for Home Assistant.

> **Backup Reminder**: Before proceeding, it's recommended to back up your Home Assistant configuration.

---

## 1. 📂 Copy the integration files

On your Home Assistant instance, create this folder:

`/config/custom_components/pin_aionanoleaf`

Inside it, place:

- `manifest.json`
- `__init__.py`

---

## 2. ✏️ Update your configuration.yaml

Add this entry at the **top level** (same indentation as `logger`, `http`, etc.):

```yaml
pin_aionanoleaf:
```

---

## 3. 🔄 Restart Home Assistant

Restart Home Assistant to apply the changes. You can do this from the UI by navigating to "Settings → System → Restart" or via the command line.

---

## 4. 🔍 Verify Installation

After restarting, check the Home Assistant logs under "Settings → System → Logs" to ensure the custom integration loaded correctly.
patch_aionanoleaf: module imported

---

## 5. 🔄 Re-add Nanoleaf Devices

If your Nanoleaf entities still show as “entity no longer provided”:
1. Remove the Nanoleaf integration (Settings → Devices & Services → Nanoleaf → ⋮ → Delete).
2. Remove orphaned entities (Settings → Devices & Services → Entities → filter by Integration: Nanoleaf).
3. Re-add the Nanoleaf integration from the UI.

---

## 🛠️ Troubleshooting

- Ensure the custom components directory is correctly set up.
- Check network connectivity to the Nanoleaf devices.
- Verify that the `aionanoleaf` package is correctly installed.
