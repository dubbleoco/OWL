import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_USER = "dubbleoco@gmail.com"
SMTP_PASS = "ggqf coda ezcu xrwq"
TO_EMAIL = "neall.dollhopf@icloud.com"
SWIPE_URL = "https://dubbleoco.github.io/OWL/swipe.html"
DASH_URL = "https://dubbleoco.github.io/OWL/"

def load_pellets():
    pfile = os.path.expanduser("~/OWL/pellets.json")
    if not os.path.exists(pfile):
        return []
    with open(pfile) as f:
        return json.load(f)

def type_color(t):
    colors = {"IDEA":"#f5c842","TODO":"#4a90e2","TASK":"#4a90e2","RESEARCH":"#00d48a","MEMORY":"#a87bdb","URGENT":"#ff4458"}
    return colors.get(t.upper(), "#888888")

def type_emoji(t):
    emojis = {"IDEA":"\U0001f4a1","TODO":"\u26a1","TASK":"\u26a1","RESEARCH":"\U0001f50d","MEMORY":"\U0001f9e0","URGENT":"\U0001f525"}
    return emojis.get(t.upper(), "\U0001f4a1")

def build_html(pellets):
    today = datetime.now().strftime("%B %d, %Y")
    count = len(pellets)

    cards = ""
    for p in pellets:
        t = p.get("type","IDEA").upper()
        content = p.get("content","").strip()
        date = p.get("date","")
        time = p.get("time","")

        lines = content.split("\n")
        title = lines[0][:80] if lines else "Untitled"

        processed = ""
        raw_lines = []
        in_processed = False
        for line in lines:
            if line.startswith("### PROCESSED"):
                in_processed = True
                continue
            if in_processed:
                if line.strip().startswith("Status:"):
                    continue
                processed += line + "\n"
            else:
                raw_lines.append(line)

        raw_text = "\n".join(raw_lines).strip()
        if not processed:
            processed = raw_text

        brief = processed.strip()[:500]
        if len(processed.strip()) > 500:
            brief += "..."

        color = type_color(t)
        emoji = type_emoji(t)

        cards += f"""
        <tr><td style="padding:8px 0;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a22;border-radius:16px;overflow:hidden;">
            <tr><td style="padding:20px 24px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="width:40px;vertical-align:top;">
                    <div style="width:36px;height:36px;border-radius:50%;background:{color};text-align:center;line-height:36px;font-size:16px;">{emoji}</div>
                  </td>
                  <td style="padding-left:12px;">
                    <div style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:{color};margin-bottom:6px;">{t}</div>
                    <div style="font-family:Georgia,serif;font-size:17px;font-weight:700;color:#f5f3ef;line-height:1.3;margin-bottom:10px;">{raw_text[:100]}</div>
                  </td>
                </tr>
              </table>
              <div style="border-top:1px solid rgba(255,255,255,0.06);margin:12px 0;"></div>
              <div style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:13px;line-height:1.7;color:rgba(255,255,255,0.55);white-space:pre-wrap;">{brief}</div>
            </td></tr>
          </table>
        </td></tr>"""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#0f0f13;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f13;"><tr><td align="center" style="padding:32px 16px;">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:480px;">

  <tr><td style="padding:0 0 24px;text-align:center;">
    <div style="font-size:32px;margin-bottom:8px;">\U0001f989</div>
    <div style="font-family:Georgia,serif;font-size:24px;font-weight:700;color:#f5c842;margin-bottom:4px;">Owl Digest</div>
    <div style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;color:rgba(255,255,255,0.3);">{today}</div>
  </td></tr>

  <tr><td style="padding:0 0 20px;text-align:center;">
    <div style="display:inline-block;background:rgba(245,200,66,0.12);color:#f5c842;font-size:13px;font-weight:600;padding:8px 20px;border-radius:20px;">
      {count} pellet{"s" if count != 1 else ""} processed
    </div>
  </td></tr>

  {cards}

  <tr><td style="padding:24px 0;text-align:center;">
    <a href="{SWIPE_URL}" style="display:inline-block;background:linear-gradient(135deg,#f5c842,#f59e42);color:#0f0f13;font-size:15px;font-weight:700;padding:14px 40px;border-radius:30px;text-decoration:none;letter-spacing:0.02em;">Review & Swipe</a>
  </td></tr>

  <tr><td style="padding:8px 0;text-align:center;">
    <a href="{DASH_URL}" style="font-size:12px;color:rgba(255,255,255,0.25);text-decoration:none;">View full dashboard</a>
  </td></tr>

  <tr><td style="padding:32px 0 0;text-align:center;">
    <div style="font-size:10px;color:rgba(255,255,255,0.1);">Dubble-O Design Co. \u00b7 Chelsea, MI</div>
  </td></tr>

</table>
</td></tr></table>
</body></html>"""
    return html

def build_plain(pellets):
    lines = [f"Owl processed {len(pellets)} pellet(s).\n"]
    for p in pellets:
        t = p.get("type","")
        content = p.get("content","").strip()
        lines.append(f"--- {t} ---")
        lines.append(content[:300])
        lines.append("")
    lines.append(f"\nSwipe: {SWIPE_URL}")
    lines.append(f"Dashboard: {DASH_URL}")
    return "\n".join(lines)

def send_email(subject, html, plain):
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def main():
    pellets = load_pellets()
    today = datetime.now().strftime("%b %d")
    subject = f"\U0001f989 Owl Digest \u2014 {today}"
    html = build_html(pellets)
    plain = build_plain(pellets)
    send_email(subject, html, plain)
    print(f"Digest sent to {TO_EMAIL}")

if __name__ == "__main__":
    main()
