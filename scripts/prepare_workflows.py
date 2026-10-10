#!/usr/bin/env python3
"""Fill the workflow templates with your own n8n IDs so they are ready to import.

Usage:
    python3 prepare_workflows.py config.json [--out ready]

config.json (see assets/config.example.json):
    n8n_url                 your n8n address, e.g. https://n8n.example.com
    timezone                IANA time zone, e.g. Asia/Riyadh
    verify_token            any long random text (or "auto")
    whatsapp_credential_id  ID of the "WhatsApp Token" credential in n8n
    notify_workflow_id      ID of the imported notify workflow (leave empty on the first run)
    tables                  IDs of the 8 data tables (contacts, settings, messages, log,
                            chats, campaigns, notes, push)

First run without notify_workflow_id: only notify.json is written. Import it, copy its ID
from the browser address bar, put it in config.json, and run again for the other three.
"""
import json, os, re, secrets, sys, uuid
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, '..', 'assets', 'workflows')
TABLE_KEYS = ['contacts', 'settings', 'messages', 'log', 'chats', 'campaigns', 'notes', 'push']


def fail(msg):
    print('ERROR: ' + msg)
    sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else 1)
    cfg_path = sys.argv[1]
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'ready'
    if not os.path.isfile(cfg_path):
        fail('config file not found: ' + cfg_path)
    try:
        cfg = json.load(open(cfg_path, encoding='utf-8'))
    except ValueError as e:
        fail('config.json is not valid JSON: ' + str(e))

    url = str(cfg.get('n8n_url', '')).rstrip('/')
    if not re.match(r'^https://[^\s/]+', url):
        fail('n8n_url must start with https://')
    tz = str(cfg.get('timezone', '')).strip()
    try:
        ZoneInfo(tz)
    except Exception:
        fail('timezone is not a valid IANA name, e.g. Asia/Riyadh')
    token = str(cfg.get('verify_token', '')).strip()
    if not token or token == 'auto':
        token = 'wa-' + secrets.token_urlsafe(18)
        cfg['verify_token'] = token
        json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    cred = str(cfg.get('whatsapp_credential_id', '')).strip()
    if not cred:
        fail('whatsapp_credential_id is empty: create the "WhatsApp Token" credential first')
    tables = cfg.get('tables', {})
    missing = [k for k in TABLE_KEYS if not str(tables.get(k, '')).strip()]
    if missing:
        fail('missing table IDs: ' + ', '.join(missing))
    notify_id = str(cfg.get('notify_workflow_id', '')).strip()

    values = {'__N8N_URL__': url, '__TIMEZONE__': tz, '__VERIFY_TOKEN__': token,
              '__WHATSAPP_CREDENTIAL_ID__': cred, '__NOTIFY_WORKFLOW_ID__': notify_id}
    for k in TABLE_KEYS:
        values['__TABLE_' + k.upper() + '__'] = str(tables[k]).strip()

    os.makedirs(out_dir, exist_ok=True)
    names = ['notify'] + (['sender', 'receiver', 'panel'] if notify_id else [])
    for nm in names:
        s = open(os.path.join(TPL, nm + '.json'), encoding='utf-8').read()
        for k, v in values.items():
            s = s.replace(k, v)
        left = sorted(set(re.findall(r'__[A-Z0-9_]+__', s)))
        if left:
            fail(nm + ': unfilled placeholders ' + ', '.join(left))
        w = json.loads(s)
        for n in w['nodes']:
            n['id'] = str(uuid.uuid4())
            if 'webhookId' in n:
                n['webhookId'] = str(uuid.uuid4())
        json.dump(w, open(os.path.join(out_dir, nm + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('ready: ' + os.path.join(out_dir, nm + '.json'))

    if not notify_id:
        print('\nNext: import ready/notify.json into n8n, copy its workflow ID into notify_workflow_id, run again.')
    else:
        print('\nMeta webhook settings:')
        print('Callback URL: ' + url + '/webhook/whatsapp-controller')
        print('Verify token: ' + token)
        print('Panel: ' + url + '/webhook/wac')


if __name__ == '__main__':
    main()
