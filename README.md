# CISA KEV Discord Alert Monitor

A Python automation tool that monitors the Cybersecurity and Infrastructure Security Agency (CISA) Known Exploited Vulnerabilities (KEV) Catalog and sends alerts to a Discord channel whenever new vulnerabilities are added.

The tool keeps track of previously reported CVEs to ensure alerts are only sent once.

## Features

- Monitors the CISA KEV Catalog
- Detects newly added CVEs
- Sends formatted alerts to Discord via webhooks
- Prevents duplicate notifications
- Simple to automate with Windows Task Scheduler or cron

## Requirements

- Python 3.10+
- requests

Install dependencies:

```bash
pip install requests
```

## Configuration

Store your Discord webhook as an environment variable.

### Windows (PowerShell)

```powershell
$env:DISCORD_WEBHOOK="https://discord.com/api/webhooks/your_webhook"
```

## Usage

Run the script:

```bash
python cisa_notifier.py
```

On the first run, the tool creates a local database file named:

```
processed_alerts.txt
```

## Automation

### Windows Task Scheduler

Create a batch file that sets the `DISCORD_WEBHOOK` environment variable and runs the script. Configure Task Scheduler to execute the batch file every 15 minutes.

### Linux/macOS (Cron)

Run the script every 15 minutes:

```cron
*/15 * * * * export DISCORD_WEBHOOK="https://discord.com/api/webhooks/your_webhook" && python /path/to/cisa_notifier.py
```

