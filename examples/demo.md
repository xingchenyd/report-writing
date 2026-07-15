# 完整调用示例

下面的 `meta.json` 可以直接喂给 `scripts/render.py`：

```json
{
  "paper_id": "demo_course_paper",
  "title_zh": "基于强化学习的资源调度策略研究",
  "title_en": "A Study on Resource Scheduling Strategies Based on Reinforcement Learning",
  "author": "张三",
  "class": "信管T2401",
  "student_id": "8304240101",
  "college": "信息管理与人工智能学院",
  "advisor": "李四",
  "date": "2026 年 7 月 15 日",
  "abstract_zh": "本文针对云环境下资源调度问题，引入强化学习方法，对比传统启发式策略。实验结果显示，所提方法在平均完成时间和资源利用率上均有显著提升。",
  "keywords_zh": "强化学习；资源调度；云计算；Q 学习",
  "classification_zh": "TP18",
  "abstract_en": "This paper addresses the resource scheduling problem in cloud computing by introducing a reinforcement learning approach and comparing it with traditional heuristic strategies. Experimental results show that the proposed method achieves notable improvements in average completion time and resource utilization.",
  "keywords_en": "reinforcement learning; resource scheduling; cloud computing; Q-learning",
  "classification_en": "TP18",
  "figure_count": 1,
  "table_count": 1,
  "ref_count": 3,
  "sections": "# 1 引言\n\n云环境中的资源调度一直是研究的热点……\n\n# 2 模型\n\n## 2.1 假设\n\n将调度问题抽象为马尔可夫决策过程 $\\mathcal{M}=\\langle S,A,P,R,\\gamma\\rangle$。\n\n## 2.2 算法\n\n使用 Q 学习算法：\n\n$$Q(s_t,a_t) \\leftarrow Q(s_t,a_t) + \\alpha \\left[ r_{t+1} + \\gamma \\max_a Q(s_{t+1},a) - Q(s_t,a_t) \\right]$$\n\n[TABLE: 不同策略性能对比\n  | 策略 | 平均完成时间 | 资源利用率 |\n  | Heuristic | 12.4s | 78% |\n  | Q-Learning | 9.7s  | 85% |\n]\n\n[CODE: language=python caption="Q 学习核心更新"\nimport numpy as np\n\ndef update(Q, s, a, r, s_next, alpha=0.1, gamma=0.9):\n    Q[s, a] += alpha * (r + gamma * np.max(Q[s_next]) - Q[s, a])\n    return Q\n]\n\n# 3 实验与结论\n\n实验表明，Q 学习在长周期任务上有更优表现……",
  "bibitems": [
    ["sutton", "SUTTON R S, BARTO A G. Reinforcement Learning: An Introduction[M]. 2nd ed. Cambridge: MIT Press, 2018."],
    ["mnih", "MNIH V, KAVUKCUOGLU K, SILVER D, et al. Human-level control through deep reinforcement learning[J]. Nature, 2015, 518(7540): 529-533."],
    ["li2024", "李四, 王五. 云计算资源调度综述[J]. 计算机学报, 2024, 47(3): 123-145."]
  ]
}
```

## 渲染

```bash
python "C:\Users\lenovo\.codex\skills\course-paper-latex\scripts\render.py" \
  --json meta.json \
  --out build/
```

## 预期产物

- `build/demo_course_paper.tex`
- `build/demo_course_paper.pdf`