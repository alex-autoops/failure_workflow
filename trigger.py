import json
from pathlib import Path
import fnmatch

ROOT = Path(__file__).resolve().parent

def show(value):
    print(json.dumps(value, indent=2) if not isinstance(value, str) else value)

def triggers():
    show('SIMULATION. Filters: push to main + *.py; manual allowed; scheduled cron 0 9 * * 1 on default branch.')
    for event in json.loads((ROOT/'events.json').read_text()):
        kind=event['event']
        if kind=='push':
            ok=event['branch']=='main' and fnmatch.fnmatch(event['path'],'*.py')
            reason='both branch and path match' if ok else 'branch or path filter did not match'
        elif kind=='workflow_dispatch': ok,reason=True,'manual trigger enabled'
        else:
            ok=event['cron']=='0 9 * * 1' and event['on_default_branch']
            reason='schedule and default branch match' if ok else 'scheduled workflow is not on default branch'
        show({'fixture':event,'result':'RUN' if ok else 'SKIP','reason':reason})

if __name__ == "__main__":
    triggers()
