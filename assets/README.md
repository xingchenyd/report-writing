# assets 目录

`course-paper-latex` 默认从本目录读取两张可选的位图：

- `header_logo.png` — 页眉左上角 logo，建议宽高比 ≤ 4:1
  （模板里 `\includegraphics[height=0.86cm]{...}` 会按高度自适应宽度）
- `cover_bg.png` — 封面底图，建议与 A4 比例接近（210:297）

## 用法

1. 把校徽/校名图另存为 `header_logo.png`，放入本目录
2. （可选）把想要做封面的背景图另存为 `cover_bg.png`，放入本目录
3. 调用方不传 `header_logo` / `cover_bg` 参数时，skill 会自动使用本目录里的图
4. 如果本目录里没有这两张图，skill 按 §3 自动回退：
   - 无 header_logo → 页眉改为只显示居中的论文题目
   - 无 cover_bg → 封面不铺底图，标题与个人信息按页面黄金比例分布

## 临时覆盖

调用方可在请求里指明：

  使用 cover_bg = C:\path\to\my_cover.png
  使用 header_logo = C:\path\to\my_logo.png

skill 会优先使用调用方提供的路径，本目录里的同名文件会被忽略。