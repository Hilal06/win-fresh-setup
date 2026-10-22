# Application Catalog

This document lists all default applications pre-configured in `apps.json` for **win-fresh-setup**. Each application maps to an official [Microsoft Winget](https://github.com/microsoft/winget-pkgs) package identifier or Microsoft Store 12-character ID.

---

## Catalog by Category

### Web Browsers
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| Mozilla Firefox | `Mozilla.Firefox` | Fast, private, and open-source web browser | Yes |
| Google Chrome | `Google.Chrome` | Fast and secure web browser by Google | Yes |
| Brave Browser | `Brave.Brave` | Privacy-focused browser with built-in ad blocker | No |

### Media & Audio
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| VLC Media Player | `VideoLAN.VLC` | Open-source multimedia player that plays most codecs | Yes |
| FxSound | `FxSound.FxSound` | Audio booster and equalizer for Windows | Yes |
| Spotify | `Spotify.Spotify` | Digital music and podcast streaming service | No |
| OBS Studio | `OBSProject.OBSStudio` | Free and open-source software for video recording and live streaming | Yes |

### Productivity & Documents
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| PDFgear | `PDFgear.PDFgear` | All-in-one free PDF reader, editor, and converter with AI | Yes |
| Notepad++ | `Notepad++.Notepad++` | Lightweight text and source code editor | No |
| 7-Zip | `7zip.7zip` | High-compression file archiver utility | Yes |
| Obsidian | `Obsidian.Obsidian` | Private and flexible Markdown note-taking and knowledge base | Yes |

### Communication & Social
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| Discord | `Discord.Discord` | Voice, video, and text communication service | Yes |
| WhatsApp | `9NKSQGP7F2NH` | Official WhatsApp desktop messaging app (Microsoft Store) | Yes |
| Telegram Desktop | `Telegram.TelegramDesktop` | Fast and secure desktop messaging app | No |

### File Sharing & Remote Access
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| Quick Share (Google) | `Google.QuickShare` | Wireless file sharing between Windows and Android devices | Yes |
| LocalSend | `LocalSend.LocalSend` | Open-source cross-platform local network file sharing | Yes |
| RustDesk | `RustDesk.RustDesk` | Open-source virtual / remote desktop software | Yes |
| Tailscale | `Tailscale.Tailscale` | Zero-config VPN for secure mesh network connectivity | Yes |

### Developer Tools
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| Visual Studio Code | `Microsoft.VisualStudioCode` | Code editor redefined and optimized for building modern apps | Yes |
| Windows Terminal | `Microsoft.WindowsTerminal` | Modern, fast, and powerful tabbed terminal for command-line tools | Yes |
| PowerShell | `Microsoft.PowerShell` | Modern cross-platform PowerShell 7 command-line shell | Yes |
| Starship | `Starship.Starship` | Fast, minimal, and customizable prompt for any shell | Yes |
| Node.js (LTS) | `OpenJS.NodeJS.LTS` | Asynchronous event-driven JavaScript runtime environment | Yes |
| Git | `Git.Git` | Distributed version control system | No |
| Arduino IDE | `ArduinoSA.IDE.stable` | Open-source IDE for Arduino microcontroller programming | Yes |

### Gaming & Peripherals
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| Steam | `Valve.Steam` | Digital distribution platform for PC gaming | Yes |
| NVIDIA App | `XP8CLZL93F5Z4P` | Unified GPU control center, driver updates, and game optimization | Yes |
| DS4Windows | `Ryochan7.DS4Windows` | PlayStation DualShock & DualSense controller mapper for Windows | Yes |

### System & Customization
| Application | Package ID | Description | Default Selected |
|---|---|---|---|
| UniGetUI | `Devolutions.UniGetUI` | Intuitive GUI for Winget, Scoop, Chocolatey & Pip package managers | Yes |
| Bulk Crap Uninstaller | `Klocman.BulkCrapUninstaller` | Powerful program uninstaller that removes leftovers and bloatware | Yes |
| Winaero Tweaker | `winaero.tweaker` | All-in-one Windows customization and tweaking tool | Yes |
| Windhawk | `RamenSoftware.Windhawk` | Customization marketplace and engine for Windows programs | Yes |
| Wise Disk Cleaner | `WiseCleaner.WiseDiskCleaner` | Disk cleanup and defragmentation utility to free up space | Yes |
| Microsoft PowerToys | `Microsoft.PowerToys` | System utilities for Windows power users | No |

---

## Modifying the Application List

You can add, edit, or remove entries by opening `apps.json` directly or using the in-app option **"➕ Add New App to apps.json"**.

Each entry in `apps.json` requires five fields:

```json
{
  "category": "Developer Tools",
  "name": "Neovim",
  "id": "Neovim.Neovim",
  "description": "Vim-fork focused on extensibility and usability",
  "default": false
}
```

* `category` *(string)*: Display category header in the TUI.
* `name` *(string)*: Application display title.
* `id` *(string)*: Exact Winget package ID or 12-character Microsoft Store ID.
* `description` *(string)*: Short functional description.
* `default` *(boolean)*: Pre-checked state when the selection menu opens.

