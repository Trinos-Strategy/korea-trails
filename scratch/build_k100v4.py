import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.argv = sys.argv
from build_k100 import build, YUSHAN, YUSHAN_EN, IC, L
import importlib
content = importlib.import_module('k100v4_content')
CONTENT = content.CONTENT
COURSES = content.COURSES
mountain, lang = sys.argv[1], sys.argv[2]
html = build(mountain, lang)
out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
out.write_text(html, encoding='utf-8')
print(f'wrote {out} ({len(html.splitlines())} lines)')
