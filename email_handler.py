"""
Email handler — SendGrid submission
Synchronicity Change Management · April 2026
"""

import json
import os
from datetime import datetime


def submit_via_sendgrid(participant_name, access_code, scored_data, raw_data):
    """
    Submit completed SVA data via SendGrid.
    Requires SENDGRID_API_KEY in environment or Streamlit secrets.
    """
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import (
            Mail, Attachment, FileContent, FileName,
            FileType, Disposition
        )
        import base64

        # Get API key
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get('SENDGRID_API_KEY')
            except Exception:
                pass

        if not api_key:
            return False, 'SendGrid API key not configured.'

        # Build JSON payload
        submission = {
            'instrument': 'SVA',
            'version': '2.0',
            'participant_name': participant_name,
            'access_code': access_code,
            'submitted_at': datetime.utcnow().isoformat(),
            'raw_data': raw_data,
            'scored_data': scored_data,
        }

        json_str = json.dumps(submission, indent=2, ensure_ascii=False)
        json_bytes = json_str.encode('utf-8')
        encoded = base64.b64encode(json_bytes).decode('utf-8')

        # Build email
        safe_name = participant_name.replace(' ', '_').replace('/', '-')
        filename = f'SVA_{safe_name}_{access_code}_{datetime.utcnow().strftime("%Y%m%d_%H%M")}.json'

        message = Mail(
            from_email='assessments@synchronicity.co.za',
            to_emails='info@synchronicity.co.za',
            subject=f'SVA Submission — {participant_name} [{access_code}]',
            html_content=(
                f'<p>SVA submission received from <strong>{participant_name}</strong>.</p>'
                f'<p>Access code: <strong>{access_code}</strong></p>'
                f'<p>Submitted: {datetime.utcnow().strftime("%d %B %Y at %H:%M UTC")}</p>'
                f'<p>JSON data attached.</p>'
            )
        )

        attachment = Attachment(
            FileContent(encoded),
            FileName(filename),
            FileType('application/json'),
            Disposition('attachment')
        )
        message.attachment = attachment

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            return True, 'Submission successful.'
        else:
            return False, f'SendGrid returned status {response.status_code}.'

    except ImportError:
        return False, 'SendGrid library not installed.'
    except Exception as e:
        return False, str(e)


def save_local_backup(participant_name, access_code, scored_data, raw_data):
    """
    Save a local JSON backup. Used when SendGrid is not configured.
    """
    try:
        submission = {
            'instrument': 'SVA',
            'version': '2.0',
            'participant_name': participant_name,
            'access_code': access_code,
            'submitted_at': datetime.utcnow().isoformat(),
            'raw_data': raw_data,
            'scored_data': scored_data,
        }

        os.makedirs('submissions', exist_ok=True)
        safe_name = participant_name.replace(' ', '_').replace('/', '-')
        filename = f'submissions/SVA_{safe_name}_{access_code}_{datetime.utcnow().strftime("%Y%m%d_%H%M")}.json'

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(submission, f, indent=2, ensure_ascii=False)

        return True, filename
    except Exception as e:
        return False, str(e)
