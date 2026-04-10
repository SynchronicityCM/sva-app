# SVA — Spiral Values Assessment
## Version 2.0 · Synchronicity Change Management · April 2026

---

## Files

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `items.py` | Complete item bank — all 63 items |
| `scoring.py` | Scoring engine |
| `email_handler.py` | SendGrid submission handler |
| `requirements.txt` | Python dependencies |
| `secrets.toml.template` | Secrets template |

---

## Deployment — Streamlit Community Cloud

1. Push all files to a GitHub repository
2. Go to share.streamlit.io and connect the repository
3. Set `app.py` as the main file
4. In App Settings > Secrets, add:
   ```
   SENDGRID_API_KEY = "your-api-key"
   ```
5. Deploy

---

## Local development

```bash
pip install -r requirements.txt
mkdir .streamlit
cp secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your SendGrid key
streamlit run app.py
```

---

## SendGrid setup

1. Create a free SendGrid account (sendgrid.com)
2. Verify your sending domain or email address
3. Create an API key with Mail Send permissions
4. Add the key to Streamlit secrets
5. Update `from_email` in `email_handler.py` if needed

---

## Data flow

1. Participant completes assessment (45–55 minutes)
2. On submission: responses are scored and packaged as JSON
3. JSON is emailed to `info@synchronicity.co.za` via SendGrid
4. If SendGrid fails: JSON saved locally in `submissions/` folder
5. JSON file fed into extraction pipeline for report generation

---

## Access codes

Access codes are generated at assessment start (8 characters, uppercase alphanumeric).
Participants use their code to return to an incomplete assessment.

**Note:** Save-and-resume currently restarts from the beginning if the participant 
returns in a new session. Full persistence requires a database integration 
(Streamlit Community Cloud does not provide persistent storage).

For full persistence: integrate with a simple database (Supabase free tier recommended)
or Microsoft 365 SharePoint list.

---

## Clinical notes

- All items authored by Wayne Kruger — do not modify without explicit sign-off
- Shadow items use inverted scale (1=Strongly agree = highest shadow)
- Rejection items use inverted scale (1=This drains me significantly = highest rejection)
- Acceptance scores derived from rank + intensity conversion table
- Self/Group orientation derived from acceptance scores — no additional items
- SC responses flagged if under 15 words — soft block before proceeding

---

*SVA Version 2 · Synchronicity Change Management · April 2026 · Confidential*
