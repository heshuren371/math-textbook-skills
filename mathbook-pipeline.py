#!/usr/bin/env python3
"""
📘 mathbook — 通用数学教材自动化流水线
==========================================
领域无关的核心管线 + 可插拔审计域 + 分层修复

兼容: Hermes Agent, Claude Code, Codex CLI, 任何 LLM Agent

用法:
  mathbook init <书名>                初始化教材项目
  mathbook chapter new <id> "<标题>"   创建新章
  mathbook chapter add <id>            加入 book.tex
  mathbook audit structural [id]       结构审计 (环境配对/格式/通用)
  mathbook audit analysis [id]         ε-N/ε-δ 审计 (数学分析)
  mathbook audit topology [id]         拓扑审计 (开集/紧致/连通)
  mathbook audit algebra [id]          代数审计 (群/环/域)
  mathbook audit full [id]             全量审计 (所有已注册域)
  mathbook fix syntax [id]             LaTeX 语法修复
  mathbook fix pairing [id]            环境配对修复
  mathbook fix unicode [id]            Unicode 字符修复
  mathbook fix all [id]                全量修复
  mathbook build                       编译
  mathbook report [id]                 量化报告
  mathbook pipeline <起始> <结束>      批量管线

配置: MATHBOOK_DOMAIN=analysis|topology|algebra ... （环境变量）
      或在项目根目录放 .mathbook.yml
"""
import sys, os, re, json, subprocess
from pathlib import Path

VERSION = '2.0'
CWD = Path.cwd()
DOMAINS = ['structural', 'analysis', 'topology', 'algebra', 'number-theory']
LEVELS = {'送分':0,'简单':1,'基础':2,'普通':3,'中等':4,'进阶':5,'拔高':6,'极难':7,'竞赛':8}
LEVEL_NAMES = {v:k for k,v in LEVELS.items()}

# ══════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════

def info(msg): print(f'  ℹ️  {msg}')
def ok(msg):   print(f'  ✅ {msg}')
def warn(msg): print(f'  ⚠️  {msg}')
def fail(msg): print(f'  ❌ {msg}')

def load(path):
    p = Path(path)
    return p.read_text(encoding='utf-8') if p.exists() else ''

def save(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding='utf-8')

def get_domain():
    """从环境变量或配置文件读取领域"""
    env = os.environ.get('MATHBOOK_DOMAIN', '').lower()
    if env in DOMAINS: return env
    cfg = load(CWD / '.mathbook.yml')
    for line in cfg.split('\n'):
        if line.startswith('domain:'):
            d = line.split(':',1)[1].strip().lower()
            if d in DOMAINS: return d
    return 'structural'  # 默认：仅结构审计

def find_tex_files(id_filter=None, dirs=None):
    """查找 .tex 文件，支持按 id 过滤"""
    if dirs is None:
        dirs_names = ['part0','part1','part2','part3','part4','part5','chapters','src','tex']
        dirs = [d for d in dirs_names if (CWD / d).is_dir()]
        if not dirs:
            # 自动搜索一级目录下的 tex 文件
            dirs = ['.']
    files = []
    for d in dirs:
        for f in sorted(Path(d).glob('*.tex')):
            files.append(f)
    if id_filter:
        files = [f for f in files if id_filter in f.stem]
    return files

def find_tex_file(ch_name):
    """按名称查找单个 tex 文件"""
    for f in CWD.rglob(f'{ch_name}*.tex'):
        if f.suffix == '.tex':
            return f
    return None

def count_environments(text):
    """统计环境配对"""
    stats = {}
    for env in ['exercise','examplebox','definitionbox','theorembox',
                'propositionbox','lemma','corollary','proof',
                'proposition','remark','note','claim','conjecture']:
        b = text.count(f'\\begin{{{env}}}')
        e = text.count(f'\\end{{{env}}}')
        if b > 0 or e > 0:
            stats[env] = (b, e, b == e)
    return stats

def count_math_mode(text):
    """检查数学模式配对"""
    # \(...\) 和 \[...\] 配对
    op = text.count('\\(')
    cp = text.count('\\)')
    ob = text.count('\\[')
    cb = text.count('\\]')
    return {'paren': (op, cp, op==cp), 'bracket': (ob, cb, ob==cb)}

def find_unicode_toxins(text):
    """检查 Unicode 毒瘤"""
    toxins = {}
    for ch, name in [('→','→ 箭头'),('✓','✓ 勾'),('✗','✗ 叉'),
                     ('【','【全角括号'),('】','】全角括号'),
                     ('℃','℃ 温度'),('💪','emoji'),('📖','emoji')]:
        n = text.count(ch)
        if n > 0: toxins[ch] = n
    return toxins

# ══════════════════════════════════════════════════════
# init — 初始化项目
# ══════════════════════════════════════════════════════

def cmd_init(args):
    title = args[0] if args else '数学教材'
    print(f'📘 初始化教材项目: {title}')
    
    dirs = ['chapters','figures','shared','appendix']
    for d in dirs:
        (CWD / d).mkdir(exist_ok=True)
    
    book_tex = f'''% ============================================================
% {title}
% ============================================================
\\documentclass[12pt,a4paper,openany]{{ctexbook}}
\\input{{shared/preamble}}
\\title{{\\Huge {title}}}
\\author{{}}
\\date{{}}
\\begin{{document}}
\\maketitle
\\tableofcontents
\\newpage
%% 用 mathbook chapter add 添加章节
\\end{{document}}
'''
    save(CWD / 'book.tex', book_tex)
    
    preamble = '''% ============================================================
% 共享导言区
% ============================================================
\\usepackage{amsmath,amssymb,amsthm}
\\usepackage[a4paper,margin=2cm]{geometry}
\\usepackage[most]{tcolorbox}
\\usepackage{graphicx,array,booktabs,multirow}
\\usepackage{hyperref,fancyhdr,listings,xcolor,enumitem}
\\graphicspath{{figures/}}
\\lstset{language=Python,basicstyle=\\small\\ttfamily,
  backgroundcolor=\\color{gray!5},frame=single,numbers=left,
  breaklines=true}

%% 定理环境（可自定义）
\\newtcolorbox{definitionbox}[1][]{colback=green!5!white,colframe=green!60!black,fonttitle=\\bfseries,title={定义~#1}}
\\newtcolorbox{theorembox}[1][]{colback=blue!5!white,colframe=blue!60!black,fonttitle=\\bfseries,title={定理~#1}}
\\newtcolorbox{examplebox}[1][]{colback=orange!5!white,colframe=orange!70!black,fonttitle=\\bfseries,title={例题~#1}}
\\newtcolorbox{applicationbox}{colback=teal!5!white,colframe=teal!60!black,fonttitle=\\bfseries\\large,title={学完本章你能做什么？}}
\\newtcolorbox{progressbox}{colback=yellow!10!white,colframe=yellow!60!orange,fonttitle=\\bfseries\\large,title={进步宣言}}
'''
    save(CWD / 'shared' / 'preamble.tex', preamble)
    
    # .mathbook.yml 配置
    cfg = f'''# mathbook 项目配置
title: {title}
domain: structural  # 审计域: structural|analysis|topology|algebra|number-theory
chapters_dir: chapters
figure_dir: figures
compiler: tectonic
'''
    save(CWD / '.mathbook.yml', cfg)
    
    ok(f'项目已初始化: {CWD}')
    for d in dirs:
        info(f'创建 {CWD/d}/')
    info('运行 mathbook chapter new 创建第一章')
    return 0

# ══════════════════════════════════════════════════════
# chapter — 章节管理
# ══════════════════════════════════════════════════════

def cmd_chapter(args):
    if len(args) < 2 or args[0] not in ['new','add','list']:
        print('用法: mathbook chapter new <id> "<标题>"')
        print('      mathbook chapter add <id>')
        print('      mathbook chapter list')
        return 1
    
    sub = args[0]
    
    if sub == 'new':
        ch_id = args[1]
        title = args[2] if len(args) > 2 else f'第{ch_id}章'
        
        # 自动确定存放目录
        chapters_dir = CWD / 'chapters'
        chapters_dir.mkdir(exist_ok=True)
        tex_path = chapters_dir / f'{ch_id}-{title}.tex'
        
        template = f'''%% ============================================================
%% {ch_id}: {title}
%% ============================================================
\\chapter{{{title}}}

\\begin{{applicationbox}}
\\textbf{{学完本章你能做什么？}}
\\begin{{enumerate}}
  \\item
  \\item
  \\item
\\end{{enumerate}}
\\end{{applicationbox}}

%% 从这里开始写内容
\\section{{从上一章来}}

\\section{{核心内容}}

\\begin{{definitionbox}}[]\n\\end{{definitionbox}}
\\begin{{examplebox}}[1]\n\\end{{examplebox}}

\\section{{本章小结}}
\\begin{{progressbox}}\n\\end{{progressbox}}
\\subsection*{{通往下一章}}
'''
        # 如果存在 difficulty 练习模板，追加
        for level_name, count in [('送分',4),('简单',4),('基础',4),('普通',5),('中等',5),('进阶',4),('拔高',3),('极难',1)]:
            template += f'\n%% {"="*5} {level_name} {"="*5}\n'
            for _ in range(count):
                template += f'\\begin{{exercise}}[{level_name}] \\end{{exercise}}\n'
        
        save(tex_path, template)
        ok(f'创建: {tex_path}')
        cmd_chapter(['add', ch_id])
        return 0
    
    elif sub == 'add':
        ch_id = args[1]
        tex_file = find_tex_file(ch_id)
        if not tex_file:
            fail(f'未找到 {ch_id}*.tex')
            return 1
        
        rel = tex_file.relative_to(CWD)
        include = f'\\include{{{rel.parent.name}/{tex_file.stem}}}'
        
        book = load(CWD / 'book.tex')
        if include in book:
            ok(f'已在 book.tex 中: {rel}')
            return 0
        
        book = book.replace('\\end{document}', f'{include}\n\\end{{document}}')
        save(CWD / 'book.tex', book)
        ok(f'加入 book.tex: {include}')
        return 0
    
    elif sub == 'list':
        print('已注册章节:')
        for f in find_tex_files():
            print(f'  {f.stem}')
        return 0

# ══════════════════════════════════════════════════════
# audit — 审计层（可插拔）
# ══════════════════════════════════════════════════════

def _structural_audit(files):
    """结构审计——领域无关"""
    total_ok = 0; total_fail = 0
    # 表头：\\(..\\) 和 \[..\] 中的反斜杠用 chr(92)
    bs = chr(92)
    print(f'  {"文件":40s} {"环境":>6s} {bs}(..{bs}) {bs}[..{bs}] {"毒瘤":>4s} {"状态":>6s}'.replace(bs + '(..' + bs + ')', chr(92)+'('+'..'+chr(92)+')').replace(bs+'[..'+bs+']',chr(92)+'['+'..'+chr(92)+']'))
    print('─' * 75)
    
    for fp in files:
        ch = fp.stem
        t = load(fp)
        
        envs = count_environments(t)
        mm = count_math_mode(t)
        toxins = find_unicode_toxins(t)
        
        env_ok = all(ok for _,_,ok in envs.values()) if envs else True
        paren_ok = mm['paren'][2]
        bracket_ok = mm['bracket'][2]
        toxin_cnt = sum(toxins.values())
        
        fails = []
        if not env_ok: fails.append('环境')
        if not paren_ok: fails.append('\\(不配对')
        if not bracket_ok: fails.append('\\[不配对')
        if toxin_cnt > 0: fails.append('毒瘤')
        
        status = '✅' if not fails else '❌'
        if fails: total_fail += 1
        else: total_ok += 1
        
        env_str = f'{sum(b for b,_,_ in envs.values())}/{sum(e for _,e,_ in envs.values())}' if envs else '-'
        print(f'{ch:40s} {env_str:>6s} {"✅" if paren_ok else "❌":>6s} {"✅" if bracket_ok else "❌":>6s} {toxin_cnt:4d} {status:>6s}')
    
    print('─' * 75)
    print(f'通过: {total_ok} | 未通过: {total_fail}')
    return total_fail

def _analysis_audit(files):
    """数学分析审计——ε-N/ε-δ 追踪"""
    total_fail = 0
    print(f'\n{"文件":35s} {"lim":>5s} {"ε":>4s} {"定理框":>4s}')
    print('─' * 55)
    
    for fp in files:
        t = load(fp)
        ch = fp.stem
        lims = t.count('\\lim')
        has_eps = bool(re.search(r'varepsilon|ε-N|ε-δ|epsilon', t))
        theorems = t.count('\\begin{theorembox}')
        
        if lims > 0 and not has_eps:
            total_fail += 1
            print(f'{ch:35s} {lims:5d} {"❌":>4s} {theorems:4d}')
        else:
            print(f'{ch:35s} {lims:5d} {"✅" if has_eps else "○":>4s} {theorems:4d}')
    
    if total_fail > 0:
        warn(f'有 {total_fail} 个文件含 lim 但没有 ε 定义')
    else:
        ok('全部文件 ε 追踪通过')
    return total_fail

def _topology_audit(files):
    """拓扑学审计——开集/紧致/连通 等关键词"""
    total_fail = 0
    print(f'\n{"文件":35s} {"开集":>4s} {"闭集":>4s} {"紧致":>4s} {"连通":>4s} {"拓扑":>4s}')
    print('─' * 60)
    
    for fp in files:
        t = load(fp)
        ch = fp.stem
        has_open = '\\begin{definitionbox}' in t and ('开集' in t or 'open' in t.lower())
        has_closed = '闭集' in t or 'closed' in t.lower()
        has_compact = '紧' in t or 'compact' in t.lower()
        has_connected = '连通' in t or 'connected' in t.lower()
        has_topology = '拓扑' in t or 'topolog' in t.lower()
        
        print(f'{ch:35s} {"✅" if has_open else "○":>4s} {"✅" if has_closed else "○":>4s} {"✅" if has_compact else "○":>4s} {"✅" if has_connected else "○":>4s} {"✅" if has_topology else "○":>4s}')
    
    return 0

def _algebra_audit(files):
    """代数学审计——群/环/域/同态/同构"""
    print(f'\n{"文件":35s} {"群":>4s} {"环":>4s} {"域":>4s} {"同态":>4s} {"同构":>4s}')
    print('─' * 60)
    
    for fp in files:
        t = load(fp)
        ch = fp.stem
        has_group = '\\begin{definitionbox}' in t and any(w in t for w in ['群','group'])
        has_ring = '环' in t or 'ring' in t.lower()
        has_field = '域' in t or 'field' in t.lower()
        has_hom = '同态' in t or 'homomorph' in t.lower()
        has_iso = '同构' in t or 'isomorph' in t.lower()
        
        print(f'{ch:35s} {"✅" if has_group else "○":>4s} {"✅" if has_ring else "○":>4s} {"✅" if has_field else "○":>4s} {"✅" if has_hom else "○":>4s} {"✅" if has_iso else "○":>4s}')
    
    return 0

def _number_theory_audit(files):
    """解析数论审计"""
    print(f'\n{"文件":35s} {"素数":>4s} {"ζ":>4s} {"L函数":>4s} {"渐进":>4s}')
    print('─' * 55)
    for fp in files:
        t = load(fp); ch = fp.stem
        print(f'{ch:35s} {"✅" if "素数" in t else "○":>4s} {"✅" if "zeta" in t.lower() else "○":>4s} {"✅" if "L函数" in t else "○":>4s} {"✅" if "渐进" in t else "○":>4s}')
    return 0

AUDIT_DOMAINS = {
    'structural': ('全局结构', _structural_audit),
    'analysis': ('数学分析', _analysis_audit),
    'topology': ('拓扑学', _topology_audit),
    'algebra': ('代数学', _algebra_audit),
    'number-theory': ('解析数论', _number_theory_audit),
}

def cmd_audit(args):
    domain = args[0] if args and args[0] in AUDIT_DOMAINS else 'structural'
    ch_filter = args[1] if len(args) > 1 and args[0] in AUDIT_DOMAINS else None
    
    # 如果第一个参数是 id_filter，使用默认 domain
    if args and args[0] not in AUDIT_DOMAINS:
        ch_filter = args[0]
        domain = get_domain()
    
    files = find_tex_files(ch_filter)
    if not files:
        fail('未找到 .tex 文件')
        return 1
    
    name, audit_fn = AUDIT_DOMAINS[domain]
    print(f'🔍 审计域: {name} ({domain})')
    
    if domain == 'structural':
        return audit_fn(files)
    elif domain == 'analysis':
        return audit_fn(files)
    else:
        return audit_fn(files)

# ══════════════════════════════════════════════════════
# fix — 修复层（分层修复）
# ══════════════════════════════════════════════════════

def _fix_latex_syntax(text):
    """LaTeX 语法修复"""
    changes = []
    # 1. examplebox }→]
    new, n = re.subn(r'(\\begin\{examplebox\}\[.*?)\}', r'\1]', text)
    if n: changes.append(f'examplebox }}→] x{n}')
    text = new
    
    # 2. end{examplebox] → end{examplebox}
    n = text.count('end{examplebox]')
    if n: changes.append(f'end{{examplebox]}} x{n}')
    text = text.replace('end{examplebox]', 'end{examplebox}')
    
    return text, changes

def _fix_pairing(text):
    """环境配对修复"""
    changes = []
    
    # 1. 连续 exercise 缺 end
    begin_c = text.count('\\begin{exercise}')
    end_c = text.count('\\end{exercise}')
    if begin_c > end_c:
        ex_idx = text.find('\\section{习题}')
        if ex_idx < 0: ex_idx = text.rfind('\\subsection')
        if ex_idx >= 0:
            before = text[:ex_idx]
            after = text[ex_idx:]
            lines = after.split('\n')
            fixed, open_p = [], 0
            for line in lines:
                if '\\begin{exercise}' in line:
                    if open_p > 0: fixed.append('\\end{exercise}')
                    open_p += 1
                if '\\end{exercise}' in line: open_p -= 1
                fixed.append(line)
            while open_p > 0:
                fixed.append('\\end{exercise}'); open_p -= 1
            text = before + '\n'.join(fixed)
            changes.append(f'exercise 闭合 x{begin_c-end_c}')
    
    # 2. \[ 缺 \]
    lines = text.split('\n')
    fixed_lines, in_math = [], False
    for line in lines:
        if '\\[' in line and '\\]' not in line:
            if in_math: fixed_lines.append('\\]')
            in_math = True
        if '\\]' in line: in_math = False
        if in_math and '\\end{' in line.strip() and '\\end{proof}' not in line:
            fixed_lines.append('\\]')
            in_math = False
        fixed_lines.append(line)
    if in_math: fixed_lines.append('\\]')
    text = '\n'.join(fixed_lines)
    
    return text, changes

def _fix_unicode(text):
    """Unicode 字符修复"""
    changes = []
    replacements = {
        '→': '$\\to$',
        '×': '$\\times$',
        '【': '[', '】': ']',
    }
    for ch, rep in replacements.items():
        n = text.count(ch)
        if n > 0:
            text = text.replace(ch, rep)
            changes.append(f'{ch}→{rep} x{n}')
    
    # ✓✗ 在文本中 → [OK][X]（但不影响数学模式内的）
    for ch, rep in [('✓', '[OK]'), ('✗', '[X]')]:
        n = text.count(ch)
        if n > 0:
            text = text.replace(ch, rep)
            changes.append(f'{ch}→{rep} x{n}')
    
    return text, changes

def _fix_mathmode(text):
    """数学模式修复"""
    changes = []
    
    # \blacksquare 修复
    old = '\\(\\\\(\\blacksquare\\)\\)'
    new = '\\blacksquare'
    if old in text:
        text = text.replace(old, new)
        changes.append('blacksquare 括号修复')
    
    # 独立 \blacksquare → \(\blacksquare\)
    # 匹配不在 \( 和 \) 内的 \blacksquare
    for m in re.finditer(r'\\blacksquare', text):
        start = max(0, m.start()-3)
        before = text[start:m.start()]
        if '\\(' not in before and '\\)' not in before:
            text = text[:m.start()] + '\\(\\blacksquare\\)' + text[m.end():]
            changes.append('blacksquare 加数学模式')
            break
    
    return text, changes

FIX_LAYERS = {
    'syntax': ('LaTeX 语法', _fix_latex_syntax),
    'pairing': ('环境配对', _fix_pairing),
    'unicode': ('Unicode 字符', _fix_unicode),
    'mathmode': ('数学模式', _fix_mathmode),
}

def cmd_fix(args):
    """修复命令: fix <层> [id]"""
    # 解析参数：fix all / fix syntax / fix all ch31 / fix syntax ch31
    layer = 'all'
    ch_filter = None
    
    if args:
        if args[0] in FIX_LAYERS:
            layer = args[0]
            ch_filter = args[1] if len(args) > 1 else None
        elif args[0] == 'all':
            layer = 'all'
            ch_filter = args[1] if len(args) > 1 else None
        else:
            # 没有指定层，直接用第一参数作为 id
            ch_filter = args[0]
    
    files = find_tex_files(ch_filter)
    if not files:
        fail('未找到 .tex 文件')
        return 1
    
    layer_names = [layer] if layer != 'all' else list(FIX_LAYERS.keys())
    
    for fp in files:
        t = load(fp)
        if not t.strip(): continue
        orig = t
        all_changes = []
        
        for l in layer_names:
            name, fn = FIX_LAYERS[l]
            t, changes = fn(t)
            all_changes.extend(changes)
        
        if t != orig:
            save(fp, t)
            changes_str = ', '.join(all_changes) if all_changes else '各项修复'
            ok(f'{fp.stem}: {changes_str}')
        else:
            info(f'{fp.stem}: 无需修复')
    
    return 0

# ══════════════════════════════════════════════════════
# build — 编译
# ══════════════════════════════════════════════════════

def cmd_build(args):
    book = CWD / 'book.tex'
    if not book.exists():
        fail('未找到 book.tex')
        return 1
    
    print('🔨 编译中...')
    r = subprocess.run(['tectonic', 'book.tex'], cwd=CWD,
                      capture_output=True, text=True, timeout=600)
    
    for line in r.stdout.split('\n'):
        if 'error' in line.lower() or 'Writing' in line:
            print(f'  {line.strip()}')
    
    pdf = CWD / 'book.pdf'
    if pdf.exists():
        ok(f'编译成功: {pdf} ({pdf.stat().st_size//1024} KB)')
    else:
        fail('编译失败，请检查错误')
        return 1
    return 0

# ══════════════════════════════════════════════════════
# report — 报告
# ══════════════════════════════════════════════════════

def cmd_report(args):
    ch_filter = args[0] if args else None
    files = find_tex_files(ch_filter)
    
    print('═' * 65)
    print('  📊 《数学教材》审计报告')
    print('═' * 65)
    
    # 运行结构审计
    _structural_audit(files)
    
    # 根据域选择额外审计
    domain = get_domain()
    if domain != 'structural':
        name, audit_fn = AUDIT_DOMAINS[domain]
        print(f'\n📎 附加审计域: {name}')
        audit_fn(files)
    
    print()
    return 0

# ══════════════════════════════════════════════════════
# pipeline — 批量管线
# ══════════════════════════════════════════════════════

def cmd_pipeline(args):
    if len(args) < 2:
        print('用法: pipeline <起始ID> <结束ID>')
        return 1
    
    for ch_id in args:
        title = f'第{ch_id}章'
        print(f'\n[{ch_id}] {title}')
        print('─' * 25)
        cmd_chapter(['new', ch_id, title])
        cmd_audit([ch_id])
        cmd_fix([ch_id])
    
    cmd_build([])
    cmd_report([])
    return 0

# ══════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__.strip())
        return 0
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    cmds = {
        'init': cmd_init,
        'chapter': cmd_chapter,
        'audit': cmd_audit,
        'fix': cmd_fix,
        'build': cmd_build,
        'report': cmd_report,
        'pipeline': cmd_pipeline,
    }
    
    if cmd not in cmds:
        print(f'未知命令: {cmd}')
        print('可用: init, chapter, audit, fix, build, report, pipeline')
        return 1
    
    return cmds[cmd](args)

if __name__ == '__main__':
    sys.exit(main())
