#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report-writing 渲染脚本
===========================

输入：调用方提供的一个 dict（也支持 JSON 文件传入），结构参见 README。
输出：OUT_DIR/<paper_id>.tex  以及  同名 .pdf（若 xelatex 可用）

命令行用法：
    python render.py --json meta.json --out build/
    python render.py --json meta.json --out build/ --no-compile

不引入第三方依赖（仅使用标准库），可在没有 pip 的环境运行。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "main.tex.tmpl"
DEFAULT_HEADER_LOGO = SKILL_DIR / "assets" / "header_logo.png"
DEFAULT_COVER_BG = SKILL_DIR / "assets" / "cover_bg.png"


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def _wrap_underline(value: str, width: str = "60mm") -> str:
    r"""把 value 放在一个固定宽度的 \underline{\makebox} 里。
    如果 value 为空，则横线宽度固定但没字，避免出现字浮在线上的视觉。
    """
    safe = value.strip() if value else ""
    if not safe:
        return f"\\underline{{\\makebox[{width}]{{}}}}"
    return f"\\underline{{\\makebox[{width}][c]{{{_tex_escape(safe)}}}}}"


def _tex_escape(s: str) -> str:
    """对 TeX 特殊字符做最少转义。调用方传入的纯文本只需要转义 & % $ # _ { } \\ ~ ^"""
    if s is None:
        return ""
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(c, c) for c in s)


def _maybe_break_title(title: str) -> str:
    """把过长的标题按连接词分两行。返回 \\ 连接的字符串（供 \\shortstack 使用）。"""
    if len(title) <= 24:
        return _tex_escape(title)
    # 优先在"基于/的/与/对/下/中"等连接词之后断行
    breakers = ["基于", "的", "与", "对", "下", "中", "—", "：", ":"]
    for b in breakers:
        idx = title.find(b, 8)  # 至少 8 字后才断
        if 8 <= idx <= len(title) - 8:
            return _tex_escape(title[: idx + len(b)]) + r"\\" + _tex_escape(title[idx + len(b) :])
    # 兜底按中点断行
    mid = len(title) // 2
    return _tex_escape(title[:mid]) + r"\\" + _tex_escape(title[mid:])


def _detect(path: Path) -> bool:
    """判断文件是否存在且非空。"""
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False


# ---------------------------------------------------------------------------
# 渲染各分块
# ---------------------------------------------------------------------------
def render_header_logo(meta: dict) -> str:
    """根据是否有 header_logo 输出 fancyhead[L] 行。"""
    custom = meta.get("header_logo")
    candidate = Path(custom) if custom else DEFAULT_HEADER_LOGO
    if custom and _detect(Path(custom)):
        path = custom
    elif not custom and _detect(DEFAULT_HEADER_LOGO):
        path = str(DEFAULT_HEADER_LOGO)
    else:
        # 无 header_logo：让题目居中显示
        return (
            "\\fancyhead[L]{\\hfill}"
            "\\fancyhead[C]{\\fontsize{10.5pt}{12pt}\\selectfont "
            + _tex_escape(meta["title_zh"]) + "}"
            "\\fancyhead[R]{\\hfill}"
        )
    # 有 header_logo：左侧显示，右侧显示题目
    return (
        f"\\fancyhead[L]{{\\raisebox{{-0.12cm}}{{\\includegraphics[height=0.86cm]{{{_tex_escape(path)}}}}}}}"
        f"\\fancyhead[C]{{}}"
        f"\\fancyhead[R]{{\\fontsize{{10.5pt}}{{12pt}}\\selectfont {_tex_escape(meta['title_zh'])}}}"
    )


def render_cover(meta: dict) -> str:
    """封面：根据是否有 cover_bg 切换分支。"""
    custom = meta.get("cover_bg")
    if custom and _detect(Path(custom)):
        cover_bg_path = custom
        branch = "with_bg"
    elif not custom and _detect(DEFAULT_COVER_BG):
        cover_bg_path = str(DEFAULT_COVER_BG)
        branch = "with_bg"
    else:
        branch = "no_bg"

    info_extra_rows = ""
    if meta.get("college"):
        info_extra_rows += (
            "\\heiti\\zihao{3} 学\\hspace{2em}院： & "
            + _wrap_underline(meta["college"])
            + " \\\\[1.6em]\n"
        )
    if meta.get("advisor"):
        info_extra_rows += (
            "\\heiti\\zihao{3} 指导教师： & "
            + _wrap_underline(meta["advisor"])
            + " \\\\[1.6em]\n"
        )
    if meta.get("date"):
        info_extra_rows += (
            "\\heiti\\zihao{3} 提交日期： & "
            + _wrap_underline(meta["date"])
            + " \\\\\n"
        )

    title_lines = _maybe_break_title(meta["title_zh"])

    if branch == "with_bg":
        return f"""
\\begin{{tikzpicture}}[remember picture,overlay]
  \\node[anchor=south west,inner sep=0pt] at (current page.south west)
    {{\\includegraphics[width=\\paperwidth,height=\\paperheight]{{{_tex_escape(cover_bg_path)}}}}};

  % 题目行白底矩形
  \\fill[white] ($(current page.south west)+(39mm,111.0mm)$)
    rectangle ($(current page.south west)+(178mm,137.8mm)$);
  \\node[anchor=west,font=\\heiti\\zihao{{-3}}]
    at ($(current page.south west)+(42.5mm,124.7mm)$) {{题\\quad 目：}};
  \\node[align=center,font=\\heiti\\zihao{{-3}}]
    at ($(current page.south west)+(125mm,124.7mm)$)
    {{\\shortstack{{ {title_lines} }}}};

  % 个人信息行白底矩形
  \\fill[white] ($(current page.south west)+(39mm,42mm)$)
    rectangle ($(current page.south west)+(178mm,85.0mm)$);
  \\node[anchor=north west,inner sep=0pt] at ($(current page.south west)+(39mm,82mm)$) {{
    \\begin{{tabularx}}{{139mm}}{{@{{}}p{{32mm}}@{{\\hspace{{1em}}}}X@{{}}}}
      \\heiti\\zihao{{-3}} 姓\\hspace{{2em}}名： & {_wrap_underline(meta.get("author", ""))} \\\\[1.6em]
      \\heiti\\zihao{{-3}} 班\\hspace{{2em}}级： & {_wrap_underline(meta.get("class", ""))}   \\\\[1.6em]
      \\heiti\\zihao{{-3}} 学\\hspace{{2em}}号： & {_wrap_underline(meta.get("student_id", ""))} \\\\[1.6em]
      {info_extra_rows}
    \\end{{tabularx}}
  }};
\\end{{tikzpicture}}
""".strip()
    else:
        return f"""
\\begin{{tikzpicture}}[remember picture,overlay]
  % 题目：页面上 1/3 高度处居中
  \\node[align=center,font=\\heiti\\zihao{{2}}]
    at ($(current page.north)+(0,-0.33\\paperheight)$)
    {{\\shortstack{{ {title_lines} }}}};

  % 个人信息：页面上 2/3 高度处居中
  \\node[anchor=north] at ($(current page.north)+(0,-0.62\\paperheight)$) {{
    \\begin{{tabularx}}{{130mm}}{{@{{}}p{{34mm}}@{{\\hspace{{1em}}}}X@{{}}}}
      \\heiti\\zihao{{3}} 姓\\hspace{{2em}}名： & {_wrap_underline(meta.get("author", ""))} \\\\[1.6em]
      \\heiti\\zihao{{3}} 班\\hspace{{2em}}级： & {_wrap_underline(meta.get("class", ""))}   \\\\[1.6em]
      \\heiti\\zihao{{3}} 学\\hspace{{2em}}号： & {_wrap_underline(meta.get("student_id", ""))} \\\\[1.6em]
      {info_extra_rows}
    \\end{{tabularx}}
  }};
\\end{{tikzpicture}}
""".strip()


def render_abstract_zh(meta: dict) -> str:
    cls_line = (
        "\\noindent{\\heiti 分类号：}" + _tex_escape(meta.get("classification_zh", "")) + "\\par"
        if meta.get("classification_zh")
        else ""
    )
    return f"""\\begin{{center}}
{{\\heiti\\zihao{{3}} {_tex_escape(meta['title_zh'])}}}\\par
\\end{{center}}

\\vspace{{1.2em}}
\\noindent{{\\heiti 摘要：}}\\par
{_tex_escape(meta.get('abstract_zh', ''))}

\\vspace{{0.4em}}
图 {meta.get('figure_count', 0)}，表 {meta.get('table_count', 0)}，参考文献 {meta.get('ref_count', 0)} 篇。\\par
\\noindent{{\\heiti 关键词：}}{_tex_escape(meta.get('keywords_zh', ''))}\\par
{cls_line}"""


def render_abstract_en(meta: dict) -> str:
    cls_line = (
        "\\noindent{\\bfseries Classification:}\\ " + _tex_escape(meta.get("classification_en", "")) + "\\par"
        if meta.get("classification_en")
        else ""
    )
    return f"""\\begin{{center}}
{{\\bfseries\\zihao{{3}} {_tex_escape(meta['title_en'])}}}\\par
\\end{{center}}

\\vspace{{1.2em}}
\\noindent{{\\bfseries Abstract:}}\\par
{_tex_escape(meta.get('abstract_en', ''))}

\\vspace{{0.4em}}
\\noindent{{\\bfseries Keywords:}}\\ {_tex_escape(meta.get('keywords_en', ''))}\\par
{cls_line}"""


# ---------------------------------------------------------------------------
# sections 解析
# ---------------------------------------------------------------------------
_HEADING_RE = re.compile(r"^\s*(#{1,3})\s*(\d+(?:\.\d+){0,2})\s+(.+?)\s*$")


_BLOCK_START = re.compile(r"^\[(TABLE|FIGURE|CODE):\s*")


def _read_block_body(lines, i):
    """Skip blank lines, then read non-empty lines until blank line, next block start, or EOF."""
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    body = []
    while i < len(lines):
        s = lines[i].strip()
        if s == "":
            break
        if _HEADING_RE.match(lines[i]) or _BLOCK_START.match(lines[i]):
            break
        body.append(lines[i])
        i += 1
    return body, i


def render_sections(sections_text: str) -> str:
    """Parse a plain-text sections block into LaTeX.

    Block syntax (declaration line must close with ] on the same line):

        [TABLE: caption]
        | col1 | col2 | col3 |
        | a    | b    | c    |

        [FIGURE: caption | path/to/fig.png | width=0.6\textwidth]

        [CODE: language=python caption="example"]
        x = 1
        print(x)
    """
    lines = sections_text.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = _HEADING_RE.match(line)
        if m:
            hashes, num, title = m.group(1), m.group(2), m.group(3).strip()
            depth = max(len(hashes), num.count(".") + 1)
            cmd = ("\\section", "\\subsection", "\\subsubsection")[min(depth - 1, 2)]
            out.append(f"{cmd}{{{_tex_escape(title)}}}")
            i += 1
            continue
        bm = _BLOCK_START.match(line)
        if bm:
            tag = bm.group(1)
            rest = line[bm.end():].strip()
            if not rest.endswith("]"):
                # invalid block syntax: emit line as plain text and skip
                out.append(_tex_escape(line))
                i += 1
                continue
            attrs = rest[:-1].strip()
            body_lines, i = _read_block_body(lines, i + 1)
            if tag == "TABLE":
                out.append(_build_table(attrs, "\n".join(body_lines)))
            elif tag == "FIGURE":
                out.append(_build_figure(attrs, "\n".join(body_lines)))
            elif tag == "CODE":
                out.append(_build_code(attrs, "\n".join(body_lines)))
            continue
        if line.strip():
            out.append(_tex_escape(line))
        i += 1
    return "\n\n".join(out)







def _build_table(caption: str, block: str) -> str:
    """[TABLE: 标题
        rows:
          | 符号 | 含义 |
          | R   | 收益 |
      ]"""
    # 收集所有以 | 开头或包含 | 的行
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        if "|" in s:
            cells = [c.strip() for c in s.split("|")]
            rows.append(cells)
    if not rows:
        return f"\\begin{{center}}\\textit{{[空表格: {caption}]}}\\end{{center}}"
    ncols = max(len(r) for r in rows)
    # 补齐
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    # 构造 tabularx 列：默认 Y 列
    col_spec = "Y " * ncols
    latex_rows = []
    for ridx, r in enumerate(rows):
        if ridx == 0:
            # 表头加粗
            cells = " & ".join(f"\\textbf{{{_tex_escape(c)}}}" for c in r)
            latex_rows.append(cells + r" \\")
            latex_rows.append(r"\midrule")
        else:
            cells = " & ".join(_tex_escape(c) for c in r)
            if ridx == 1:
                # toprule 已隐含在 header 上方
                pass
            latex_rows.append(cells + r" \\")
    body = "\n      ".join(latex_rows)
    return f"""\\begin{{table}}[H]
\\centering
\\caption{{{_tex_escape(caption)}}}
\\small
\\begin{{tabularx}}{{\\textwidth}}{{{col_spec.strip()}}}
\\toprule
      {body}
\\bottomrule
\\end{{tabularx}}
\\end{{table}}"""


def _build_figure(caption_attr: str, block: str) -> str:
    """[FIGURE: 标题 | path/to/fig.png | width=0.6\\textwidth]"""
    parts = [p.strip() for p in caption_attr.split("|")]
    if len(parts) < 2:
        return f"\\begin{{center}}\\textit{{[无效图片声明: {caption_attr}]}}\\end{{center}}"
    caption = parts[0]
    img_path = parts[1]
    width = "0.6\\textwidth"
    for p in parts[2:]:
        if p.startswith("width="):
            width = p[len("width=") :]
    return f"""\\begin{{figure}}[H]
\\centering
\\includegraphics[width={width}]{{{_tex_escape(img_path)}}}
\\caption{{{_tex_escape(caption)}}}
\\end{{figure}}"""


def _build_code(attrs: str, block: str) -> str:
    """[CODE: language=python caption="..."]"""
    style = "ide-dark"
    caption = None
    for tok in attrs.split():
        if tok.startswith("language="):
            lang = tok.split("=", 1)[1]
            style = f"ide-dark-{lang}" if lang not in ("python",) else "ide-dark"
        elif tok.startswith("caption="):
            caption = tok.split("=", 1)[1].strip('"')
    code = block
    if caption:
        return f"""\\begin{{codeframebox}}
\\captionsetup{{labelformat=empty}}
\\begin{{lstlisting}}[{('caption=' + _tex_escape(caption) + ', ' if caption else '')}style={style}]
{code}
\\end{{lstlisting}}
\\end{{codeframebox}}"""
    return f"""\\begin{{codeframebox}}
\\begin{{lstlisting}}[style={style}]
{code}
\\end{{lstlisting}}
\\end{{codeframebox}}"""


# ---------------------------------------------------------------------------
# 参考文献
# ---------------------------------------------------------------------------
def render_bibitems(bibitems):
    """bibitems: list of (key, raw_text)"""
    return "\n".join(f"\\bibitem{{{k}}} {_tex_escape(v)}" for k, v in bibitems)


# ---------------------------------------------------------------------------
# 顶层渲染
# ---------------------------------------------------------------------------
def render(meta: dict) -> str:
    if not TEMPLATE.is_file():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")
    src = TEMPLATE.read_text(encoding="utf-8")

    substitutions = {
        "TITLE_ZH": _tex_escape(meta["title_zh"]),
        "TITLE_EN": _tex_escape(meta.get("title_en", meta["title_zh"])),
        "HEADER_LOGO": render_header_logo(meta),
        "COVER": render_cover(meta),
        "ABSTRACT_ZH": render_abstract_zh(meta),
        "ABSTRACT_EN": render_abstract_en(meta),
        "SECTIONS": render_sections(meta.get("sections", "")),
        "BIBITEMS": render_bibitems(meta.get("bibitems", [])),
    }
    for k, v in substitutions.items():
        src = src.replace("{{" + k + "}}", v)

    # 残余占位符（调用方未提供任何可选字段时）清理
    src = re.sub(r"\{\{[A-Z_]+\}\}", "", src)
    return src


# ---------------------------------------------------------------------------
# 编译
# ---------------------------------------------------------------------------
def compile_pdf(tex_path: Path, out_dir: Path, runs: int = 2) -> Path:
    if not shutil.which("xelatex"):
        raise RuntimeError("xelatex not in PATH; install TeX Live or MiKTeX with xelatex")
    out_dir.mkdir(parents=True, exist_ok=True)
    for k in range(runs):
        proc = subprocess.run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(out_dir),
                str(tex_path),
            ],
            capture_output=True,
            text=True,
            cwd=str(tex_path.parent),
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout[-4000:])
            raise RuntimeError(f"xelatex failed (run {k + 1}/{runs})")
    pdf = out_dir / (tex_path.stem + ".pdf")
    if not pdf.is_file():
        raise RuntimeError("xelatex reported success but PDF not found")
    return pdf


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, help="path to meta JSON")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--no-compile", action="store_true", help="only emit .tex")
    args = ap.parse_args()

    meta = json.loads(Path(args.json).read_text(encoding="utf-8"))
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    paper_id = meta.get("paper_id") or re.sub(r"[^\w\-]+", "_", meta["title_zh"])[:40]
    tex_path = out_dir / f"{paper_id}.tex"

    tex = render(meta)
    tex_path.write_text(tex, encoding="utf-8")
    print(f"[report-writing] wrote {tex_path}")

    if not args.no_compile:
        pdf = compile_pdf(tex_path, out_dir)
        print(f"[report-writing] compiled {pdf}")


if __name__ == "__main__":
    main()