import os
import requests

# Configuration - Official CISA Live KEV JSON Feed
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1521804495569424436/QPIZb-XY_N_OUr0-FexmwxSYmtuNQl3KeghZ-dkSRhQrNYoUzz_jPleDPzx-TVaPi4B4"
DB_FILE = "processed_alerts.txt"

def get_processed_alerts():
    """Load previously sent CVEs to prevent duplicates."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def mark_as_processed(cve_id):
    """Save a sent CVE ID to the tracking file."""
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{cve_id}\n")

def send_to_discord(cve_id, vendor, product, description, action, due_date):
    """Format and send the KEV Alert via a Discord Webhook Embed."""
    
    # Construct an official, clean looking layout for critical vulnerabilities
    payload = {
        "embeds": [
            {
                "title": f"🚨 NEW CISA KEV ALERT: {cve_id}",
                "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                "description": f"**Vendor:** {vendor}\n**Product:** {product}\n\n**Description:**\n{description}\n\n**Required Action:**\n{action}",
                "color": 16515843,  # Safety Orange / Red
                "footer": {
                    "text": f"Remediation Due Date: {due_date} | CISA KEV Live"
                }
            }
        ]
    }
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print(f"Failed to send to Discord: {response.status_code}")

def main():
    print("Checking live CISA KEV feed for changes...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(CISA_KEV_URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching KEV feed: {e}")
        return

    vulnerabilities = data.get("vulnerabilities", [])
    if not vulnerabilities:
        print("No entries found in the KEV catalog.")
        return

    processed_alerts = get_processed_alerts()
    new_alerts_found = 0

    # Process oldest entries to newest entries in the database structure
    for vuln in vulnerabilities:
        cve_id = vuln.get("cveID")
        
        # Check if we have processed this specific CVE before
        if cve_id not in processed_alerts:
            vendor = vuln.get("vendorProject", "Unknown")
            product = vuln.get("product", "Unknown")
            description = vuln.get("shortDescription", "No details provided.")
            action = vuln.get("requiredAction", "Patch or apply workaround immediately.")
            due_date = vuln.get("dueDate", "URGENT")
            
            print(f"New KEV Identified: {cve_id}")
            send_to_discord(cve_id, vendor, product, description, action, due_date)
            mark_as_processed(cve_id)
            new_alerts_found += 1

    if new_alerts_found == 0:
        print("Your database is up to date with the KEV Catalog. No new updates.")
    else:
        print(f"Successfully synced {new_alerts_found} new KEV vulnerability cards to Discord!")

if __name__ == "__main__":
    main()