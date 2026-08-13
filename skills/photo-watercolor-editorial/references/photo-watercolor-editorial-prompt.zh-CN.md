# photo-watercolor-editorial 四区块提示词编译器

先确定执行配置、证据、版式、面部、复杂度、变化配方、标题和锚点，再写提示词。把完整状态保存为一份版本 2 的 `prompt-contract.json`，随后只向 ImageGen 发送四个非空区块。每个标题必须独占一行，标题与正文之间、区块之间都必须有空行。前三个区块标题共用；`artifact-full` 的第四块必须叫 `OUTPUT CONTROL`，`portable-direct` 的第四块必须叫 `TITLE AND OUTPUT`。完整英文提示词不得超过 320 词，并且只能输出当前执行配置对应的分支。通过门禁后直接传递已保存 UTF-8 文件的原始文本，不得重新拼接。

优先级依次为：证据和关系；完整几何；连通形体；已选机制结果；焦点结构；已选变化；水彩场域；当前标题输出分支。需要压缩时先删可选气氛，不得删合同结果。

## 结构化合同

合同结构和合法值以 [英文编译器](photo-watercolor-editorial-prompt.en.md) 的版本 2 示例为准。它必须包含：

- `execution_profile`：`artifact-full` 或 `portable-direct`；
- `semantic`：照片、构图、设计、方向、比例、完整性、识别线索、焦点和四区域复杂度；
- `variation`：一个内部 recipe、任务内 variation ID、被锁定的轴、全部已选轴和已通过的兼容规则；
- `artifact`：准确标题、标题颜色、字体资源、主标题槽位、不同的备用槽位，以及最多两次本地合成。

变化值只能来自 [变化引擎](variation-engine.md)。两种执行配置都在合同中保存真实标题，但只有 `portable-direct` 可以把标题内容发送给 ImageGen。

## 区块一 — `SUBJECT AND COMPOSITION`

内部合同可以保留模式名，但不得把 `editorial-recompose`、`poster-rebuild`、`source-locked`、`contact-only`、`evidence-only` 等元语言发送给 ImageGen。只写实际画面结果：主体放在哪里、尺度如何、哪些姿态和关系保持不变、支撑留下什么、留白在哪里。

图片接口提供原生 `size` 或 `aspect_ratio` 参数时，优先通过参数传递画幅。提示词中只写一次 `Use a [W:H] canvas.`，不得再补一个数学等值比例或解释句。接口没有原生参数时，也仍只保留这一句。

`poster-only` 写 `Repaint the upload entirely as watercolor.`；`include-original` 使用英文编译器中的源图忠实照片区域句。构图、设计、完整性和变化轴都使用英文编译器给出的直白视觉结果。`trace_mode: none` 不生成任何句子。区块必须以 `Show only the selected subject, essential support, and open paper.` 结束。

`artifact-full` 把合同槽位写成纯留白：`Keep the [slot] calm and empty, with open paper and an even light value.`。随后用“该空白与主体如何平衡或分离”的直白句子描述关系，不出现 `title field`，也不向 ImageGen 解释后续用途。

## 区块二 — `PRIMARY FORM`

始终加入：

> Build one connected silhouette from a few broad value masses and long directional boundaries, with one clear focal area and calm interiors.

按英文编译器原样加入每个已激活复杂度机制的正向结果，每种机制只出现一次。加入已选焦点接口；`open_mouth: true` 时加入统一张嘴接口。最后按英文编译器加入唯一的边缘方式和焦点对比接口。

## 区块三 — `MEDIUM AND FIELD`

写明冷压纸水彩、宽阔透明色洗、克制的湿画法渗色、受控积色、纸面作为高光和主动留白显露，以及清洁分色。把内部色板预算翻译成 `very limited`、`limited` 或 `restrained ... moderate variation`，不得要求模型自审计精确色数。明暗块、透明叠层和装饰笔触也统一使用 `a few`、`broad`、`sparse` 等倾向性表述。

不得加入 `Exclude` 或 `Avoid` 清单。区块以正向表面句结束：`Keep every painted form matte and tactile, with calm interiors and visible paper grain.`

## 区块四 — 当前执行配置

### `artifact-full`

第四块标题使用 `OUTPUT CONTROL`。不得出现真实标题文字，也不要重复“标题字段”语言。只写一句：`Output one finished watercolor artwork with this open-paper area remaining calm, empty, and visually unmarked.`。

### `portable-direct`

第四块标题使用 `TITLE AND OUTPUT`，先加入唯一的标题关系接口。在合同主槽位中准确设置一次标题，使用克制的编辑衬线字体和合同指定的源图深色。字号为短边的 `6%-7%`；标题包围盒面积目标约为总画布的 `1%`；宽度不超过 `35%`，高度不超过 `12%`；距对齐画布边缘 `10%-12%`。必要时可做最多三行、不改变词序的换行。加入 `Keep it as the sole typographic element; leave the remaining poster visually unmarked.`，并以 `Output only the finished poster.` 结束。

## 生成门

运行 `python scripts/check_prompt.py --prompt <final-prompt.txt> --contract <prompt-contract.json>`。失败时先修合同或提示词，不得生成。通过只证明结构完整，不能代替真实成图验证。
