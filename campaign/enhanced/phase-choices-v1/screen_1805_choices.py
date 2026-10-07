"""Stage closure variants and replay both branches; stop at first viable detour."""
from pathlib import Path
import json,os,subprocess,sys

root=Path(__file__).resolve().parents[3]
here=Path(__file__).resolve().parent
n=int(os.environ.get('LLC_CHOICE_LEVEL','1805'))
choices=json.loads((here/f'level-{n}-choice-candidates.json').read_text())['candidates']
baseline=json.loads((here.parent/'house-order-screen-v1/event_tiles.json').read_text())
overlay=here/f'level-{n}-choice-stage.json'
preview=here/f'level-{n}-choice-stage.html'
node=Path(r'C:\Users\rahul\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe')
results=[]
for index,candidate in enumerate(choices):
    value=dict(baseline);value[str(n)]=candidate['close']
    overlay.write_text(json.dumps(value))
    subprocess.run([sys.executable,str(here.parent/'build_preview.py'),'--house-order-event-tiles',str(overlay),'--output',str(preview)],cwd=root,check=True,stdout=subprocess.DEVNULL)
    env={**os.environ,'LLC_PREVIEW_PATH':str(preview),'LLC_CHOICE_INDEX':str(index),'LLC_CHOICE_LEVEL':str(n)}
    result=subprocess.run([str(node),str(here/'test_1805_choice_stage.cjs')],cwd=root,check=True,capture_output=True,text=True,env=env)
    row=json.loads(result.stdout);results.append(row)
    print(json.dumps({'index':index,'close':candidate['close'],'extra':candidate['extraSteps'],
                      'default':row['default'],'signal':row['signal']}),flush=True)
    if row['default']['completed'] and row['signal']['completed']:
        (here/f'level-{n}-choice-screen.json').write_text(json.dumps({'attempts':results,'winner':index},indent=2))
        break
else:(here/f'level-{n}-choice-screen.json').write_text(json.dumps({'attempts':results,'winner':None},indent=2))
