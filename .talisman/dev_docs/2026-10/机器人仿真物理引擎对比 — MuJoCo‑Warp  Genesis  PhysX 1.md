---
title: "机器人仿真物理引擎对比 — MuJoCo‑Warp / Genesis / PhysX"
source: "https://mp.weixin.qq.com/s/QeeL85xEQuWA-o1Pu2XfDg?poc_token=HHH9xmqj58jbN9UU3Ub4cJm5ZXjxRLHmWCNVFqR7"
author:
published:
created: 2026-10-08
description:
tags:
  - "clippings"
---
## 机器人仿真物理引擎对比 — MuJoCo‑Warp / Genesis / PhysX / Newton

human five *2026年10月6日 12:39*

https://mandarobotics.com/blog/comparing-physics-engines/index.html

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ9n2ZvKrPPdSQFdxF32M9l2Qx4ewvTB5UZS3fr6bK9rhBGXxNDCciaPMEibJrrhGhu17R5GFic3JFLIp9emlmot4zyYCSTy1xiaTrU/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

本文采用相同场景与完全一致的机器人控制器，对四款物理引擎开展对比测试。在刚体测试中，各引擎对于任务成功/失败的判定通常保持一致，但在接触力、运动轨迹以及柔性物体仿真行为上存在明显差异。

- 在严格对齐配置的前提下，各引擎对于宏观结果的仿真表现基本一致，例如单物体运动、自由空间内机器人运动、抓取与拾取放置任务（见第2‑4节）。
- 宏观结果相近的背后，力学与运动行为却并不相同：接触力峰值最高可相差一个数量级；即便任务成功率完全相同，轨迹跟踪误差仍可达厘米级（见第2‑6节）。
- 小间隙接触场景最能区分引擎性能：在插销‑插孔装配任务中，采用硬接触模型的PhysX会出现力过载，而其余三款软接触引擎均可完成任务（见4.4节）。
- 柔性物体仿真场景下各引擎分歧最大：即便设置完全相同的标称材料参数与抓取动作，不同引擎得到的结果截然不同；对网格进行加密或者缩小仿真步长，也无法消除这种差异（见第5节）。
- CPU与GPU平台均有合适的仿真选型：对于单环境仿真，CPU版本MuJoCo速度最优；面向RL规模的批量仿真任务，GPU引擎吞吐量占优；但在超大批量规模下，吞吐量增长会趋于平缓（见第7节）。
- 许多看似是物理引擎本身带来的差异，实际上来自仿真环境配置问题：例如导入后关节附加惯量、缺失碰撞掩码、几何模型标签错误等（见第2‑8节）。

仿真是具身AI技术栈的核心组件。当我们利用仿真对机器人行为做基准测试与评估时，主要有两大目标：第一，相较于真实世界测试，仿真能够实现规模化、降低测试成本；第二，仿真需要忠实地复现真实世界物理规律（即缩小Sim2Real gap），从而能够预测机器人实际部署后的性能。

高性能模型有望彻底改变资产生成与Real2Sim工作流，进一步提升仿真的可扩展性与易用性。尽管生成资产的视觉保真度已经十分出色，但对物理行为的建模对于机器人仿真同样至关重要。现实世界中大量细节很难被精确复现，而仿真框架/物理引擎的选型是其中的关键决策。因此本文聚焦仿真的核心组件，旨在回答以下研究问题：

使用不同物理引擎仿真同一个机器人与同一场景时，会产生哪些差异？有哪些需要注意的细节与陷阱？

为解答上述问题，本文深度对比四款物理引擎实现：IsaacSim中的NVIDIA PhysX、原生MuJoCo、Newton(MuJoCo‑Warp)以及Genesis。探究引擎之间产生分歧的场景背后成因，以及该现象对策略评估带来的影响。

## 外观行为相近，内部建模的受力却可能截然不同

使用同一套机器人控制器，驱动机器人在四款仿真环境中将三个方块沿通道向前推动。从视觉上看，各仿真中的行为高度相似，但机器人的运动路径与接触力存在区别。可播放动画对比运动效果，或切换轨迹叠加视图观察轨迹发生分叉的位置。图中曲线展示两个夹指垫作用在方块上的合力（并非夹持力）。

本文在完全受控的实验条件下开展测试，严格对齐场景与资产配置，使用同一个控制器驱动机器人。为保证实验可分析，逐步增加场景复杂度：从基础接触测试，过渡到多物体交互、机器人操作任务；同步测量接触力、运动轨迹以及其余关键指标。

## 1\. 实验方法

### 跨引擎统一基准测试集

仿真是对现实世界的简化。没有任何仿真器可以捕获现实世界全部细节，而即便是微小差异，也会导致仿真结果完全发散。不同引擎对接触求解器实现会做出不同假设，因此同一场景在不同引擎中的演化过程可以完全不一样。 **本文测试这些差异在机器人评估场景下何时会产生实际影响。**

为此，我们搭建一套可在四款引擎上运行的统一基准测试集。严格对齐场景规格与资产文件，通过逐步提升场景复杂度的方式验证兼容性。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZicz2vOIO9RpHciaJjggXLWa5ZCmA37Sehx7MxYUNxic5fMFdgw1ibOw4YKGRZhATiaRWVvCaIFLsbH4lRVuEz0zpCjcqQQib9QCJ3qc/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

实验用例（从简单刚体控制到耦合操作任务，逐步提升场景复杂度，全程记录仿真行为）

### 引擎选型

选取四款业界流行可公开获取的引擎/配置：

| 引擎/仿真栈 | 执行路径 | 版本与配置 |
| --- | --- | --- |
| PhysX | Isaac Sim · CPU TGS | Isaac Sim 6.1.0.0 · float32 |
| Newton (MuJoCo‑Warp) | 独立Newton · 原生MuJoCo‑Warp接触求解 · GPU | Newton 1.5.2 · MuJoCo‑Warp 3.11.0 · Warp 1.16.0 · float32 |
| MuJoCo CPU | 原生CPU运行时 | MuJoCo 3.11.0 · float64 |
| Genesis | 原生刚体求解器 · GPU | Genesis 1.4.1 · float64 |

全部实验硬件环境：RTX PRO 5000实例，NVIDIA GPU驱动版本595.71.05。

### 两类接触模型

MuJoCo CPU、基于Newton运行的MuJoCo‑Warp以及Genesis均采用MuJoCo风格软接触模型，允许物体发生微小穿透；PhysX则将接触处理为刚性硬约束。因此前三者仿真结果预期会更加接近，PhysX作为独立对照组。

四款引擎均在关节坐标系下仿真Franka Emika Panda机械臂；不使用引擎内置驱动，全部由同一个显式力矩控制器驱动机器人。

针对柔性物体，各方案实现差异进一步放大：MuJoCo将柔性物体求解放在同一个求解器内部；Genesis与Newton则分别运行刚体求解器与柔性体求解器，再做耦合。

### 机器人与资产校验

几何模型、质量、质心、惯量、关节轴与关节限位、初始位姿、碰撞几何体全部做对齐校验。导入完成后读取校验参数，而非直接假设源文件解析行为完全一致。针对Franka Emika Panda机械臂，在开展操作实验前，校验导入得到的物理参数与正向运动学结果。

⚠️本研究不存在物理层面的真实真值

本文只做引擎之间的横向对比，并未和真实硬件做对标。多个引擎仿真结果一致， **并不代表某一个引擎更贴近现实世界** 。MuJoCo CPU与解析解仅作为方便使用的基线，不是物理真值。

若无特殊说明，每套配置仅运行一组对齐后的实验。重复实验、减半仿真步长运行仅用于灵敏度校验，不用于计算置信区间、估计成功率或者收敛性分析。通过每一步动量平衡校验，检验记录的力和运动是否自洽；该校验仅验证测量流程，不代表物理真实性。失败废弃的实验记录全部保留在审计笔记中，不会丢弃。

所有引擎输出的物体位姿，在同一个渲染器中回放展示。力矢量箭头统一比例尺：1 N = 1 cm，因此冲击力箭头可能超出画面边界；绘图展示力的完整幅值。

## 2\. 基础控制实验

### 单物体基准校验，验证一致性

首先验证基础运动与接触行为的一致性。对齐原始几何、初始状态、质量、重力、标称表面参数；测量制动距离、碰撞响应力随时间变化、仿真步长敏感性。物体整体运动趋势相近，但接触过程存在区别。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZibicXvvRSRlcRh81hKvicriaYTdy61F8eOtEtfWCibxYCR2zUQibBnKI1M2AcezItIWJfCBBlKcm2Hibw3vdPTG4xUHr5HeCytSaYWM0/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

图例：PhysX CPU｜Newton / MuJoCo‑Warp｜MuJoCo CPU｜Genesis

接触力；重力；比例尺1 N = 1 cm；轨迹使用对应引擎颜色；铰链力矩见详细绘图。

实验场景：滑块减速停止、立方体下落并静置、单铰链连杆。

整体运动相近，但接触历史存在差异。

即便是最简单场景，也能发现导入默认参数、接触力的细微差异。这些基础观测是后续全部实验的基础。

滑块最终停止位置差异仅约0.05 mm；1 ms步长下铰链连杆和独立摆解析解偏差不超过0.084°。这为更复杂场景建立基线。但接触行为不能简单等价：下落立方体稳定后穿透量、瞬态响应各不相同；滑块轨迹接近，但力峰值差异巨大。 **运动趋势一致仅代表控制校验通过，不等于接触物理完全相同。**

#### 滑动方块实验

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ8UwDMuwqOgmlZSibkvqc1OemV8GPY95xeCHetmFMInP9JZPHmicvjlic0W2HdJ1Lhg4uTSZCICm4ZxibshKUibclNJp97854KFMJHU/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

100 g，边长4 cm的方块滑动直至停下。质量、几何、初速度、摩擦、仿真步长全部对齐，仅接触公式不同；无外部施加力。取前0.6 s原始未平滑数据。力曲线为方块受到接触力矢量和，不是单点接触最大力。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ8NsudayWHYEdZeDpFgT31TzibYew2jWdPNlwAZuQKVwibh8hu7WXFkyKLAOl25OiauxpC9Zcgicqjtw0Hwcib5KmcJvlx1IVbQZtCM/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

##### 停止距离几乎一致

| 引擎 | 滑行距离 | 接触合力峰值 |
| --- | --- | --- |
| PhysX | 126.422 mm | 1.06 N |
| Newton / MuJoCo‑Warp | 126.472 mm | 10.46 N |
| MuJoCo CPU | 126.471 mm | 10.46 N |
| Genesis | 126.447 mm | 1.50 N |

各引擎最终滑行距离最大差值仅约0.05 mm。作为参考，理想无旋转库伦摩擦滑块理论滑行距离127.42 mm。

##### 接触过程截然不同

MuJoCo CPU与Newton仿真中，方块质心会短暂抬升约1.12 mm，接触合力峰值约是静止支撑力0.981 N的十倍。Genesis方块始终贴近地面；PhysX质心高度几乎不变。

四组仿真全部通过动量‑平衡校验，仅证明记录的力和动量变化自洽， **不代表物理现象符合现实** 。方块短暂上浮、巨大力峰值属于尚未解决的接触瞬态现象；缩小仿真步长可以削弱上浮，但无法定位其产生根源。

##### 将步长减半带来的变化大于更换引擎

仿真步长减半至1 ms，所有引擎的滑行距离增加0.50‑0.51 mm，该变化量约为不同引擎之间差异的十倍。

MuJoCo CPU、Newton的力峰值下降至约9.17 N，方块最大上浮高度从1.12 mm降低到0.23 mm；Genesis峰值降至1.25 N；PhysX维持约1.06 N。

力的定性差异仍然存在；但弹跳现象对仿真步长高度敏感，不能直接视作引擎固有的属性。

启示：物体停止位置一致，背后的受力与运动过程却可以完全不同。即便只看终点指标评估表现完全一样，机器人策略依然会经历这些瞬态力学过程。

#### 立方体下落碰撞静置

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZib2icibdgzbQNZwIH5Vs85Zfchv0cp19tX10LgX9Ng4a6ZxQKU2uUw8ZhIGfzTge4tZXfPloCnxAJeyYJBicVuZLZ7YYh9kbE3glM/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

同一个方块从质心高度35 cm（离地间隙33 cm）处静止释放，仿真时长1 s。主图采用1 ms步长；2 ms用于灵敏度对照。开启重力，无外力施加。绘图包含高度‑速度全历程；冲击力顶点、最低位置视图做接触时刻局部放大；合力曲线包含重力分量。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZibgE8T9Vv4HEyOodMrpNuUianxLaqyqkuvjibCoS4NRQycV8JYzoHXw5oWNiajFWOq6jiayicsgP55eUkfhW6iauAwAtXUEiaAQJUrgZE/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

##### 刚性急停 vs 柔顺停止

| 引擎 | 接触合力峰值 | 最大穿透重叠量 | 静置时刻 |
| --- | --- | --- | --- |
| PhysX | 253.86 N | <0.001 mm | 0.264 s |
| Newton / MuJoCo‑Warp | 52.04 N | 7.844 mm | 0.362 s |
| MuJoCo CPU | 52.04 N | 7.844 mm | 0.362 s |
| Genesis | 53.44 N | 7.567 mm | 0.364 s |

注：重叠量指旋转后方块最低顶点低于理想平面的深度，不是接触余量。“静置”定义：后续记录中速度持续低于1 mm/s。

四款引擎均在约0.26 s发生接触。PhysX几乎瞬间终止下落。在本文设置10 ms软接触时间常数条件下，MuJoCo、Newton、Genesis允许方块向下穿透平面，再被推回静止，不会产生明显的腾空反弹。

穿透量级可以做近似估算：将MuJoCo的 `solref=(0.01,1)` 近似为连续临界阻尼接触，阻抗接近单位1，则ω≈100 rad/s。0.33 m高度下落，接触时刻速度约2.55 m/s，峰值穿透估计：v/(eω)≈9.4 mm。

该估算和实测值（2 ms步长：8.7‑9.0 mm；1 ms步长：7.6‑7.8 mm）在同一数量级。该一维估算忽略离散积分、多接触耦合，但解释了为什么10 ms的响应时间会产生毫米级穿透。PhysX采用零恢复系数约束，属于完全不同的接触配置。

##### 步长减半，峰值力近似翻倍？

PhysX仿真步长从2 ms改为1 ms，峰值力从127.53 N上升到253.86 N。但接触后前40 ms的总冲量在两种步长下均为0.29234 N·s。 **相同总冲量在更短时间内释放，单步平均力就会变大。仅对比峰值力会产生误导。**

1 ms步长下，MuJoCo CPU、Newton的40 ms冲量0.30430 N·s；Genesis为0.30341 N·s；速度历程差异造成微小冲量差距。

校验注意事项

基线与重复实验默认2 ms，再运行一组1 ms。四款引擎1 ms轨迹满足每步5×10⁻⁶ N·s的动量容差。Newton 2 ms轨迹误差达到1.4×10⁻⁵ N·s，不用于主图展示。后续读取确认原生接触力和广义接触力一致；微小偏差出现在原生力与加速度之间，并非力坐标系转换错误，属于数值一致性方面待注意的问题。

2 ms软接触仿真穿透8.74‑9.01 mm；1 ms下降至7.57‑7.84 mm。这并不构成收敛性研究。原始实验数据与审计记录全部保留；力峰值没有做平滑缩放处理。

#### 单铰链测试

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZicU3OWookHxAn6V7HTeYg3iaKfjmSibedP8pXwIMfawaoLFdmL0wxFuX2ia4eNia29EaHczX77dosHiba30ZcYTOR4NGr6cQ84xIsg0/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

均匀连杆质量1 kg，长30 cm，宽4 cm，悬挂在无摩擦铰链上。初始偏离竖直方向0.5 rad，初速度为0；0.1‑0.2 s施加0.2 N·m力矩脉冲；开启重力，无碰撞，无策略，无位置驱动，无阻尼。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZibPcPe9rWh1OJpJHPhWP8QWu1fKKHstiahAmnRgppYrhnqc5HkU1PgCicLGTLmY2ScMdBaPNVVRIqF2CR9tuAqvv0JZlyUuoRHBo/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

轨迹叠加后高度重合；黑点标记固定铰支点。图中仅绘制重力箭头，关节反力没有记录；施加力矩绘制在曲线中，不使用力箭头可视化。1 ms步长下对齐力矩回放，并和非线性单摆解析方程做对比。

##### 导入默认参数问题：看似物理差异，实则是模型导入错误

Genesis最初运行版本连杆摆动速度明显偏慢，1 s内和参考解最大偏差达到51.4°。原因：MJCF文件规定附加惯量armature为0，但导入后关节被带入0.1 kg·m²的附加转动惯量。显式设置为0并回读校验后，Genesis仿真结果与MuJoCo CPU达到浮点精度级一致。

同样导入检查还发现基座固定设置错误、PhysX关节坐标系缩放问题。修正后全部模型正向运动学校验通过，质心最大偏差低于0.1 μm。

##### 离散误差很小，同一引擎多次运行结果确定

1 ms步长，四款引擎仿真结果与理想刚体ODE解析解偏差不超过0.084°；0.5 ms步长偏差小于0.042°。

本无接触测试场景中，Newton/MuJoCo‑Warp在随机种子0、1、2下回放得到完全一致帧序列。但在碰撞链场景下Newton会出现结果变化。说明该现象取决于场景或者计算逻辑， **不能笼统宣称GPU物理仿真一定是非确定的。**

经验教训：优先校验模型导入与力矩映射。有些巨大的引擎差异仅仅来源于导入的关节属性；修正后简单铰接体在各个引擎中仿真高度一致。

## 3\. 多物体交互

### 接触构型改变如何改变碰撞轨迹

从简单物体碰撞出发，测试力峰值差异是否会进一步造成物体轨迹姿态的分化。结果显示PhysX的硬约束接触模型会开始体现区别。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ8kJF9Yom7xpiagQIVdXHOX33CLZiaVCaZ34XX6M989LgK4Z0kziaCkbib6cTnxG95Lgzvia0RJRLZ8Jw1qib17PgKxicyKRrRBjlicdfI/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=9)

仿真步长0.5 ms。可切换轨迹叠加视图对比路径；重点观察0.085‑0.116 s的碰撞时刻。1 s仿真结束时球体仍然处于滚动状态。记录世界坐标系轨迹与原生力信号，不做平滑。XY视图坐标轴独立缩放；3D回放使用真实几何比例。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZicSa9POM6HMTgiawtArUq6cPaaQBy6DCibVbLfInQm2mqvr0qn3tvbDBsAjSJNK9ogrz1XXGhRH6cYRUSgeyT7tia2wFsPCB6TE2E/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=10)

实验配置：球体半径3 cm（150 g）；立方体边长6 cm（100 g）；棱柱截面等边三角形边长9 cm，高度6 cm（100 g）。全部物体初始静止放置地面；球体以初速度1.4 m/s同时赋予匹配滚动角速度。标称摩擦系数0.3，无显式滚动摩擦、扭转摩擦。质量惯量回读和原始定义数值精度对齐，但这不代表碰撞烘焙几何、接触定律完全一致。

##### 同一条碰撞链式事件，仿真输出肉眼可见的不同结果

四款引擎均复现球体‑立方体‑棱柱的撞击序列。仿真0.9995 s时刻立方体中心位置：

- PhysX：(119.3, 4.9) mm
- Newton/MuJoCo‑Warp：(136.5, ‑2.7) mm
- MuJoCo CPU：(139.0, ‑3.1) mm
- Genesis：(135.1, ‑5.0) mm

棱柱朝向角度分别约23.0°、55.5°、57.4°、55.3°。差异不仅仅体现在力曲线，物体最终位置姿态也出现明显分化。

##### 是否仅仅是仿真随机性造成？

相同初始条件、不同随机种子，每个引擎运行三次。PhysX、MuJoCo CPU、Genesis多次运行输出完全一致。Newton仿真结果存在波动：球体最大偏差4.40 mm，立方体0.88 mm，棱柱1.70 mm。

PhysX和其余引擎之间立方体终点平均偏差18.7‑21.3 mm，远大于单引擎多次运行带来的波动。其余三者之间差异较小，约2.6‑4.3 mm；三次重复不足以做统计推断。

Genesis与Newton均运行在GPU；PhysX、MuJoCo CPU运行于CPU。Genesis在该碰撞链测试中结果确定，但在后续密集物体扫掠场景会出现波动。 **GPU运行本身不能用来预测仿真是否具有确定性；结果取决于场景和具体实现。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ8Viaic5sk4mb9UdUibicMXfRh4vFIXrSRm88qcKy7iao8Aqh7fd7WfnNKZavX4rKrdEibPeSEamrpq0meYoJhSv7MHSCICskNf5RjjI/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=11)

随机种子控制Python/NumPy、Genesis初始化，但无法保证GPU仿真确定；Newton相同种子重复运行也出现变化，说明结果分散度和种子没有明确关联。

仿真步长从1 ms减半到0.5 ms，立方体、棱柱终点位移随引擎不同变化0.1‑4.8 mm；还在运动的球体对步长更加敏感。PhysX采用零恢复系数硬接触，其余引擎使用软接触。

结论：还没有引入机器人，仅仅依靠接触数值求解差异就已经产生肉眼可区分的不同结果。

## 4\. 机器人实验

### 跨仿真器对齐机器人资产的集成测试

当引入机器人之后，仿真分歧既可以来源于接触求解，也可以来源于机器人本身无接触阶段动力学差异。因此首先校验导入后惯量、坐标系、关节约定、力矩上限、参考运动；将前面铰链连杆校验扩展到完整机械臂正向运动学、等力矩运动反馈跟踪（全程关闭接触）。

继承前面铰链测试的导入参数修正。完成修正后，匹配力矩输入条件下Panda机械臂在四款引擎中运动几乎完全一致。 **自由空间运动一致，不等于接触行为等价。** 后续抓取、堆叠、推物实验用来检验接触带来的区别。

#### Panda机械臂运动测试

仅仅匹配目标位姿是不够的。在解释一次抓取失败之前，我们需要区分三类来源：导入模型差异、铰接体动力学差异、反馈控制器差异：

1. **资产与运动学等价性 — 已校验** 。使用同一份Panda模型与标准手爪，不使用四份各自打包资产。校验关节坐标系、连杆质心、惯量、限位、夹指约定；在相同关节角度下对比末端执行器位姿。
2. **无接触条件下相同力矩回放 — 完成测量** 。发送带时间索引的关节力矩；显式控制原生驱动、被动阻尼、重力补偿。在引入策略之前对比关节与末端轨迹。
3. **统一显式控制器 — 更长时序回放** 。使用完全一致的PD方程、增益、限幅、控制周期。目标状态一致，但由于反馈感知到的系统状态不同，输出力矩可以不同。报告力矩曲线和跟踪误差，不能当作完全相同动作回放。

实验使用机械臂全部7个关节；手爪夹指固定张开至4 cm；源资产来自MuJoCo Menagerie的Panda模型。所有适配器关闭接触被动阻尼、附加惯量armature、原生驱动；实验短运动范围内监控关节限位但不强制限位。该配置是简化动力学基线，不是Panda产品级配置。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZicoFYicNibcuYhIeuzlHB3l8LL5aKbjVXZ3vTOGNX5p27RVHv5NmWviafzPEj8kkOPOcv17vLia18N4cMib12tB0vsqDFO3uUBIMaq8/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=12)

2.5 s往返运动，由共享外部控制器驱动；连杆显示源资产粗网格；轨迹跟随手爪坐标系原点。即使画面渲染碰撞网格，仍然关闭碰撞检测。不记录关节反力；绘图绘制力矩指令。参考运动、PD增益、力矩限幅全部对齐，控制器频率1 kHz。由于存在反馈，各引擎输出指令力矩可以不同。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ8ECukSGMGuMHatjTv2qc6d1v1SQUfankBvSic1SkvQbshicHeXtb8fxG6HvVR5ic8teWhkSTYSOxT6jOYdD1xXY7hKvmk2kZ4v2Y/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=13)

##### 使用共享控制器跟踪长时序运动

关节空间参考轨迹使用平滑五次曲线运动到偏移位姿再返回，总时长2.5 s。使用标准模型离线生成前馈动力学序列。每个引擎运行完全相同的显式PD，增益、力矩截断一致，控制频率1 kHz。目标状态完全相同，但反馈力矩响应各引擎观测到的关节状态。

单纯开环力矩脉冲会在约1 s之后使机械臂超出关节限位；本组增益下100 Hz的跟踪测试腕部误差很大。展示的运行全部采用统一1 kHz控制器配置，不针对引擎单独调参。

手爪最大移动距离约19.3 cm。1 ms物理步长条件下，各引擎关节最大跟踪误差不超过0.026°；手爪相对于MuJoCo CPU版本最大偏移0.194 mm。每个引擎内部，三组不同种子回放帧序列完全复现。

将物理步长减半，PhysX最大偏移扩大到0.740 mm。 **并不代表步长越小结果一定越好。这属于跨引擎尚未解决的差异，不能证明哪条轨迹更符合现实；两个引擎的轨迹都会随步长改变，我们缺少完整机械臂的独立动力学参考解。**

##### Open-loop baseline：0.5 s完全相同力矩输入

每个引擎施加完全一致的开环力矩。1 ms步长运行0.5 s；偏移量以MuJoCo CPU结果做参照。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZic172qiaXsafK5hMHpR2xUkT5Bk4UdoqsHnRBQwjvicW2c6y2mTrIg9ZMXkPZibqLYMXRXj4bRu6O2dYBdBmh3sPlxRsDuVibn828o/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=14)

全部11根连杆的质量、质心偏移、完整惯量张量，在连杆局部坐标系下做比对。最大偏差分别小于1.7×10⁻⁷ kg、2.6×10⁻⁹ m、5×10⁻⁸ kg·m²。选取五组指定关节构型，运行前校验正向运动学；仿真全程校验原生位姿和报告关节角度一致性。

输入完全相同的初始姿态、重力补偿力矩；0.05‑0.15 s关节2叠加+2 N·m；0.15‑0.25 s关节4叠加‑1 N·m。前馈力矩随机器人运动保持不变，不做引擎专属重力补偿，无反馈。

1 ms步长下，手爪原点相对MuJoCo CPU最大偏移：PhysX 0.035 mm，Newton/MuJoCo‑Warp 0.0031 mm；关节角度最大偏差分别0.024°、0.00047°。Genesis与MuJoCo CPU浮点级重合。同一个引擎，三组种子回放帧完全一致。

0.5 ms步长条件，PhysX手爪最大偏移增长到0.213 mm；Newton为0.0040 mm，关节最大偏差0.058°、0.00073°。偏差仍然很小，但仅仅一次步长加密不足以说明收敛，也无法定位来源。

结论：资产、力矩语义对齐完成后，无接触条件下Panda在四款引擎中的运动高度重合。

#### 抓取‑抬起‑释放任务

对齐配置的机器人能否在持续接触任务上表现一致？Panda机械臂使用两个独立驱动夹指抓取边长4 cm、100 g方块；执行脚本：闭合‑抬起‑释放序列，使用自由空间测试的同一套机械臂控制器。单根夹指力矩上限4 N；所有接触面标称摩擦系数0.5。

测试两组情况：方块居中；方块沿夹指宽度方向偏移8 mm。

为隔离问题，使用显式对齐的盒型夹持垫，不使用引擎烘焙得到的Panda指尖网格；机器人其余部分关闭碰撞几何体。在测试真实手爪复杂几何之前，先完成简单铰接抓取测试。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ9L1tyVaHnufyp1KSicEwcOt7icicSUPX3YJaHAtQzRfX6OejhUqnveiaYTncxEHeAvH0wDo16HsXLpRXEfAq37y1eYX5L3UkHSsNk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=15)

- 居中抓取：抬起夹持力表现相近。仿真时长3.5 s；时序：0.3‑0.8 s闭合；1.0‑1.8 s抬起；夹持至2.3 s；2.3‑2.7 s打开夹指，随后物体静置。1 ms完整记录。
- 偏心抓取：任务成功一致，但释放之后行为出现差异。参考运动控制器不变；仅方块初始位置偏移8 mm。观察2.3‑2.7 s释放‑落地过程，可切换轨迹叠加视图。
![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZibic0ibDrbtSouYd845UZtKFVzWFB1J80yibv5FdLpdUpheCsiaV5BQet4ENWyn7UgUp1SRy1MwUo5fjMicfoLibfKqRWIbYicg6xrTibo/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=17)

观测结果：八组实验全部完成方块抬起释放。偏心工况释放之后，方块水平最终偏移：PhysX 9.0 mm，Genesis 6.9 mm，Newton/MuJoCo‑Warp 1.1 mm，MuJoCo CPU 0.3 mm。 **任务全部成功，但接触演化轨迹各不相同。**

局限：全部为1 ms物理步长下单次实验；引擎之间接触正则化参数并不相同。

在对齐夹持垫几何前提下，同一个控制器在各个引擎均可完成抓取；最值得关注的分歧来自物体释放之后的落点。

### 4.1 机器人：拾取‑放置任务

#### 边缘堆叠拾取放置

测试机器人操作领域非常典型的拾取放置任务。这类场景大量出现在机器人操作基准测试中。核心问题：微小的接触差异，是否足以改变操作任务的成败？

机器人拾取40 mm、100 g方块，移动100 mm，放置在另一块方块上方。两块方块均为可动物体，下方方块不做固定。全部引擎运行同一控制器，不做物体感知修正，不对引擎调参。

夹指配置沿用抓取测试：单指力矩上限4 N，盒型夹持垫，标称摩擦系数0.5；机器人其余部分关闭碰撞。

改变上方方块期望放置位置，设置不同偏移阈值，观测各引擎在该场景下表现。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ8aBItrEjib36jZlibZz76829BRq9qhY05bjRicia2IxeNZAnYkYib3FhE0Kmd1Cc2LpvWDo2e9ssZ7aGujZPvY6DYL34fuw0HWnfLA/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=18)

放置偏移设置： 0 mm — 完全居中； 16 mm — 在边缘内侧； 20 mm — 理想临界边缘； 22 mm — 超出边缘；

仿真时长6 s；流程：闭合夹指‑抬起‑搬运‑下放‑打开夹指（3.6‑4.0 s）‑机械臂收回，物体静置。回放采样间隔5 ms；曲线保留全部物理步数据。竖直虚线标记4 s夹指完全打开时刻；水平线X=20 mm标记理想静态倾覆边缘。两者都不是经验性的成功阈值。

| 标称放置偏移 | 静置后结果 |
| --- | --- |
| 0 mm | 四款引擎均保持堆叠 |
| 16 mm | 四款引擎均保持堆叠 |
| 20 mm | 四款引擎全部倾覆倒塌 |
| 22 mm | 四款引擎全部倾覆倒塌 |

补充说明：Newton居中堆叠场景方块虽然没有倒塌，但后半段竖直方向存在约0.081 mm的位移；短暂接触断开、速度尖峰，没有通过我们更严格的静置判定标准，分开记录，不标记为成功堆叠。

补充对照：将20 mm工况上方方块初始位置X偏移‑1 mm，Y偏移+1 mm，所有引擎都维持堆叠；反向对角线偏移，则全部倒塌。说明这组实验划定局部放置临界转换边界，不是单纯X方向倾覆阈值。对照实验记录在审计文档，不进入回放下拉选项。

无修改重复运行仅改变随机种子，倾覆结果可复现。PhysX、MuJoCo CPU回放帧完全确定；Genesis种子带来差异小于0.00001 mm。Newton上方方块轨迹重复运行偏差4.8‑6.9 mm， **即使同一随机种子下重复运行依然会发生。**

结论：本堆叠任务中，四款引擎对“放置后是否倒塌”的判定保持一致。Newton居中堆叠虽然不倒，但不满足静置判据。

### 4.2 机器人：推物实验

#### 狭窄通道内接触力测试

更加复杂的多接触场景下会发生什么？机械臂推动三个松散放置的40 mm、100 g方块，穿过两堵固定墙壁构成通道。初始前方两个方块总跨度84 mm。测试通道宽度90 mm（有裕量）、80 mm（需要物体重新排布）；控制器不变，不对引擎调参。

，时长00:12

<video src="https://mpvideo.qpic.cn/0b2eu4abwaaagqagfa6etvvfbj6ddotqagya.f10002.mp4?dis_k=45bd0b0cdec097da66aa7b492038df3f&amp;dis_t=1791425910&amp;play_scene=10120&amp;auth_info=W4jFp98IOAdj6PzS5TpXBn1uWDdOFW9ZLXdsSh18Nht9bDFWUUFHfRJcKmwKAVsl&amp;auth_key=346a097c7f99cf903736c1d8e11d0b51&amp;vid=wxv_4725618367368380421&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

手爪执行固定直线路径目标：保持0.5 s，3 s内向前推动240 mm，之后保持到5 s。夹指目标姿态固定；所有引擎运行同一个1 kHz柔顺关节控制器；全局标称摩擦系数0.5。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ9iawkOhyAicPicRva3DeicnfcHJttcv7iaKP6AAl8C7acJU0XJPRXfPDLYiavuwibm9KywMEKrNFbyoE3ARr3kaNyTo7pYWM3bEO7sjQ/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=19)

实验组：

- 90 mm — 无阻碍推物
- 80 mm — 阻碍推物
- 90 mm，后方方块横向偏移+1 mm
- 90 mm，后方方块横向偏移‑1 mm
- 90 mm，0.5 ms物理步长

记录方块质心、手爪坐标系轨迹；切换叠加视图，重点观察通道入口物体重排过程。静态反作用力箭头不做展示；回放每5 ms采样；绘图保留全速率记录。推进进度定义：最靠后方方块质心相对通道入口位置。全部三个方块质心越过通道入口至少60 mm，判定为成功通过通道。

初始前方两个方块总宽度84 mm。90 mm通道留有间隙；80 mm通道必须发生物体旋转或者互相错开。因此两组宽度属于强几何偏向的对照，没有扫描中间宽度边界。

四款引擎全部完成90 mm通道推物；全部无法完成80 mm通道。宏观任务结果一致，但物体轨迹出现分化：80 mm实验结束时刻，MuJoCo CPU和Genesis后方方块位置相差约13 cm。

90 mm通道条件，后方方块横向偏移仅仅1 mm，MuJoCo CPU物体轨迹最大偏移可达31.4 mm；PhysX仅2.4 mm。但无修改重复运行下两者结果完全复现。仿真步长减半，MuJoCo CPU轨迹变化最大27.8 mm，PhysX仅0.27 mm；但任务成败不变。 **不能凭借该灵敏度推断哪个引擎物理更接近真实。**

表格：相对90 mm基准，物体轨迹最大变化量（单位 mm）；数值取同一时间戳下全部三个物体最大值，不仅仅是终点距离；布局扰动取正负偏移两组中更大值。

| 引擎 | 无修改重复运行 | 布局扰动±1 mm | 仿真步长减半 |
| --- | --- | --- | --- |
| PhysX | 0 | 2.40 | 0.27 |
| Newton / MuJoCo‑Warp | 2.76 | 27.99 | 5.27 |
| MuJoCo CPU | 0 | 31.36 | 27.81 |
| Genesis | 0.003 | 3.55 | 0.45 |

启示：宽窄通道在所有引擎任务结果一致；但仅仅1 mm布局扰动，MuJoCo家族引擎物体位移变化幅度是PhysX、Genesis的十倍。 **任务结果相同，不代表仿真鲁棒性相同。**

### 4.3 机器人：密集物体扫掠实验

#### 15个物体场景下的可复现性

，时长00:27

<video src="https://mpvideo.qpic.cn/0bc3uyc2oaafmuan4mwbbfvfljwdu6taljya.f10002.mp4?dis_k=c87a1258ade019877c6e1f227bfa26db&amp;dis_t=1791425910&amp;play_scene=10120&amp;auth_info=XfP4vbJSblc07KvfsD9WVng1XTZIFWdXcSFtH0p4MB97ZzQEBBgRLUVYfWFfBFp1&amp;auth_key=79e238eda1afe258af3a8fa27e8e08e2&amp;vid=wxv_4725619174822330369&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

上面两个场景引擎宏观结果大多一致。当大量接触级联发生时会怎样？Panda机械臂安装一块220 mm推板，沿45°斜线运动，聚拢15个球体、立方体、圆柱体，推动穿过300 mm开口，沿缓斜坡落入托盘。一部分物体落入托盘，一部分留在外部，一部分掉落桌面。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ9LXBfjdZxE4ojye7LOT96YjnmRsv8UOIpcXyXjfGG9eLhGmp9fNUItBsJd2nT8TksMTGFgRBqpEVVq8EBLOTN7GhXHwWzRR38/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=21)

每个引擎运行三次完全相同输入的重复实验。统计最终落在托盘内部物体数量（12.5 s时刻物体质心判据）。每次重复实验启动全新进程，输入完全相同，随机种子固定为0。全部12次实验均通过质量、质心、惯量、运动学有限状态校验。该场景是在MuJoCo CPU中开发定型，存在任务选择偏向。

| 引擎/运行 | 第1次重复 | 第2次重复 | 第3次重复 |
| --- | --- | --- | --- |
| PhysX CPU | 9 / 15 | 9 / 15 | 9 / 15 |
| Newton / MuJoCo‑Warp | 11 / 15 | 8 / 15 | 7 / 15 |
| MuJoCo CPU | 10 / 15 | 10 / 15 | 10 / 15 |
| Genesis | 10 / 15 | 8 / 15 | 8 / 15 |

PhysX、MuJoCo CPU三次运行物体轨迹完全复现。Newton第一次收集物体最多，但后两次少于两个CPU版本；Genesis同样出现结果变化。

Genesis推板接触力尖峰现象尚未定位；托盘计数仅作为诊断输出，不能证明记录接触力是正确的。Genesis推板记录峰值力6.37‑7.52 kN；对比MuJoCo CPU约57 N；Newton/MuJoCo‑Warp 50‑169 N；PhysX 605 N。该峰值发生在仿真后期推板顶住静止物体阶段，对托盘物体计数几乎没有影响；物理成因尚未解决。

重要提示：将密集场景仿真结果差异归因于引擎选型之前， **首先要测量同一引擎内部多次运行的波动。** 本实验中，同一引擎输入不变带来的结果波动幅度，可以和不同引擎之间差异相当。相比单次运行排名，三次重复得到的结果分布更有参考价值。

### 4.4 机器人：高精度插销装配

#### 小间隙带来结果分化

，时长00:10

<video src="https://mpvideo.qpic.cn/0bc3cmaloaaaxuam4r6evrvfae6dw4jqbnya.f10002.mp4?dis_k=91f7687b9118d84fde95d581040a892c&amp;dis_t=1791425910&amp;play_scene=10120&amp;auth_info=V+r3scZWZFhi7fHW4WlRXHpvBWMcHTJWfXA+GUUoZUxxZDNSUhgbIhNZJ2gOUl1/&amp;auth_key=e8d9ed609e28d6c9f239e5318f8f7ab1&amp;vid=wxv_4725618831476621322&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

力矩驱动的Panda机械臂，将刚性固连的20 mm插销插入带倒角的插孔。改变径向间隙（0.10、0.25、0.50 mm）与初始对位条件（对齐、横向偏移0.25 mm、1°倾斜）。每种条件运行三次，全新进程，输入固定，种子固定；四款引擎合计108次尝试。几何体采用64个面片；物理仿真阻抗控制器频率1 kHz。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZic4wX18rxxNCiaMPpN7PhcImerRwGOtRtMjkCibFwJfEM4pFiaJAib1JwZIia9vrDvqMibBDh0rqYvQb50xGwZDwPGT70hiaAV9lYE1Tk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=22)

现实钢‑钢装配场景末端执行器摩擦力可以超过60 N，力矩超过20 N·m。本实验控制器指令上限设置20 N / 2 N·m；一旦接触合力超过40 N或者力矩超过4 N·m，仿真停止。本实验测试温和接触工况，不是标定工业级装配。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZibD2wyC7hr6hibUmvpBnK9BpjzFdVsk2DnBUIhwxJTicolp4jgzSqd2Jo9njLezOpx38oKPNszVrBIK0FVicJEQFsiaklplF2nMAHk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=23)

统计：27组条件下，达到目标插入深度次数 / 其余结果。

| 引擎 | 达到目标深度（27次总尝试） | 其余结果 |
| --- | --- | --- |
| PhysX CPU | 21 | 6次力过载停止 |
| Newton / MuJoCo‑Warp | 22 | 3次倾斜工况中途停滞；2次数值失效 |
| MuJoCo CPU | 24 | 3次倾斜工况中途停滞 |
| Genesis | 24 | 3次倾斜工况中途停滞 |

0.50 mm间隙，9组实验插销全程不触碰插孔，全部引擎均达到目标深度，属于无接触对照组。0.10 mm小间隙，倾斜插入条件：MuJoCo CPU、Newton、Genesis停滞在15.3‑15.7 mm；PhysX在对齐、倾斜工况均触发过载停止。除Newton峰值力各次运行存在波动、两次数值失效外，其余引擎重复运行结果一致。

##### 接触反馈控制器能否解决停滞？

针对严苛0.10 mm偏移倾斜工况，新增一套接触引导控制器：滤波后的接触力允许有限横向位移向上退让；绕插销尖端力矩允许有限姿态修正。控制器 **不使用插孔位置信息来决定修正方向** 。其余全部条件不变；所有引擎反馈增益完全相同。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ9IZ6Ocu0zia5WPwZfsebP2VGqIZSGRT6mf3fyuF9hKianNyKw990UAS8nBay3WfJeKa8iaibQPWjicgB9Sm3dVqPia49q3icibKdGaB5g/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=24)

倾斜插入工况：基线控制器 → 接触引导控制器；三组引导运行结果区间

| 引擎 | 最终深度(mm) | 接触力峰值(N) | 原生最大穿透(μm) |
| --- | --- | --- | --- |
| PhysX CPU | 12.24 → 12.24（均过载） | 125.83 → 46.32 | 8.67 → 8.34 |
| Newton / MuJoCo‑Warp | 15.31 → 19.93‑19.936 | 17.04 → 19.23‑20.65 | 4.49 → 3.90‑10.08 |
| MuJoCo CPU | 15.32 → 19.95 | 16.85 → 15.30 | 3.23 → 2.02 |
| Genesis | 15.68 → 19.96 | 11.12 → 3.59 | 2.75 → 1.24 |

开启接触反馈之后，MuJoCo CPU、Newton、Genesis三组倾斜工况全部到达目标深度；PhysX全部触发过载停止。Newton虽然深度达标，但多次运行力峰值（19.2‑20.6 N）、穿透量（3.9‑10.1 μm）存在变化。 **达到同样插入深度，不代表接触历史完全相同。**

结论：小间隙场景把两类接触模型明确区分开来。三款软接触引擎会停滞在相近深度，开启接触反馈后成功装配；相同条件下PhysX触发力过载。0.5 mm间隙插销全程不接触，该条件的一致性不能说明接触求解能力。

有效性、力限、重复实验与排除几何说明

“达到目标深度”定义：完整4 s运行的最后0.25 s内深度始终大于等于19 mm；穿透量作为独立诊断指标，不计入结果判据。控制器任务指令上限20 N / 2 N·m，再受关节力矩限幅。一旦接触合力超过40 N、手爪原点力矩超过4 N·m，仿真终止。这不是Panda硬件保护逻辑，不能阻止冲击冲量。

PhysX严苛对齐工况仿真记录到485 N / 331 N·m，原生穿透1.49 mm，属于仿真异常，不代表硬件真实行为。64面片输入通过采样几何校验；128面片PhysX测试出现插销导入容差问题（偏差约24 μm），导入无效，不纳入统计。16分片几何修复方案同样无效。本实验没有对任何引擎做调参以获得更好结果。

MuJoCo CPU、Genesis严苛工况重复运行结果在展示精度内完全一致。Newton严苛偏移工况峰值力各次运行7.5‑13.4 N，一次数值失效；0.25 mm间隙也出现一次数值失效。三次重复用于诊断波动，不足以给出可靠小概率失效概率。回放绘图均展示每组条件第一次运行结果。

## 5\. 可变形物体仿真

### 柔性物体：即使参数对齐，任务结果仍然不一致

，时长00:11

<video src="https://mpvideo.qpic.cn/0bc3deegaaaij4abta6mb5vfqgodmamqqyaa.f10002.mp4?dis_k=5a89cde49f86d393e8e668cb150a1a5c&amp;dis_t=1791425910&amp;play_scene=10120&amp;auth_info=DbC3/Sc9UDG7q9LmZl4HKWgIa0sdYAp6L2kZRHg3T3E2YVdXSUIqQA99bAldUiQ=&amp;auth_key=6efcb8e06989bfccd998e06d57ff4096&amp;vid=wxv_4725617345233076226&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

刚体场景中，尽管建模受力可以相差巨大，但引擎大体行为趋势一致。接下来讨论对真实仿真非常关键、实现难度很高的场景：柔性物体操作。此时不再仅仅对比刚体接触，材料本构、内部网格、夹指‑可变形体耦合方式都会影响结果。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZib0Oc0ZgF7j4oqsJXjgZs5UPyl7H8SMmwibHiavvdWNYalEl7rdicoQTt2I9mACDag0a08QX9TT2EiaRgMtZr2NOTQ1hibKZk08VL6k/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=25)

同一个Panda机械臂运动，挤压‑抬起‑放下直径60 mm球体。测试两套不同网格分辨率，控制网格带来的变量。

实验条件：Panda夹指单指最大力2 N；单指1 N；阈值扫描1.10 N、1.50 N；纯压缩对照。

⚠️不同引擎输出结果差异非常明显。运行失效则定格在最后有效采样点。

球体四面体网格质量约105 g（重力1.031 N）；同等密度理想完整60 mm球体质量113 g。静态对称捏取，接触法向水平，库伦摩擦最大竖直支持力；为每根夹指法向力。，得到阈值：每根夹指法向力至少1.03 N。

1 N夹指力矩上限略低于该阈值；2 N约为静态所需支持力的1.94倍。

注意：1 N、2 N是作动器力矩上限， **不是测得的接触法向力** 。曲面接触、物体形变、关节动力学、抬起加速度都会改变实际受力阈值。1 N工况发生打滑和阈值附近加载是符合预期；剧烈爆炸式运动、无效几何、不一致力反馈属于另外一类失效。

仿真流程4.5 s：夹指闭合，抬起80 mm，保持，下放球体，再打开夹指。先下放再松开夹指，把抓取稳定性和掉落冲击分开。和之前实验一样，仅解析几何夹指垫参与碰撞。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Kltic3d4ibvZ8jTIomnznAibMZSMIuEUtRRn6PP14EfPyGCvshkib9wbClMVpXHHot42WqIm2mia9YPYq8MLWrJrKiam12p1qAaWAoh1xVDEPIG74/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=26)

下表为单次实验；记录首次检测到网格翻转或者完整周期完成。绘图仪器回放使用独立记录，失效时刻可以存在差别。Newton两套实验均设置形状接触阻尼0.2。

| 仿真方案 | 单指上限1 N | 单指上限2 N |
| --- | --- | --- |
| MuJoCo CPU | 1.345 s停止 | 完整周期；抬起高度约66 mm |
| Native MuJoCo‑Warp | 1.335 s停止 | 夹持抬起约60 mm；2.525 s停止 |
| PhysX GPU — 配置未调通 | 0.066 s停止 | 1.536 s停止 |
| Genesis FEM / SAP | 数值运行完成，无法稳定抬起 | 数值运行完成，无法稳定抬起 |
| Newton MJWarp + VBD | 数值跑完，短暂抬起后掉落球体 | 抓取‑下放‑释放全部完成；质心抬起约69 mm |

PhysX 1 N工况夹指还未闭合仿真就停止，需要初始化接触审计。Newton 1 N工况会丢失球体。两套MuJoCo方案在2 N下可以抬起，但下放阶段行为分化；Genesis数值上运行结束，但无法实现稳定抬起。

针对已经可以抬起球体的三套方案，进一步扫描力矩阈值：1.05、1.10、1.15、1.50 N；每次单组运行，输入不随机化。控制器轨迹、物体、引擎数值参数全部固定。Newton保持形状阻尼0.2，步长0.5 ms；原生MuJoCo步长50 μs。再补充PhysX、Genesis在1.10、1.50 N两组测试，步长维持1 ms。

说明：“无效”代表几何翻转检测触发，不是普通打滑，也不是进程崩溃。抬起高度取1.9‑2.2 s窗口质量加权质心上升高度。负质心位移代表物体沉降到初始位置下方。

| 单指力矩上限 | MuJoCo CPU | Native MuJoCo‑Warp | Newton MJWarp + VBD | PhysX GPU 配置未调通 | Genesis FEM / SAP |
| --- | --- | --- | --- | --- | --- |
| 1.05 N | 1.410 s几何失效，尚未进入夹持保持 | 1.365 s几何失效，尚未进入夹持保持 | 完整周期；抬起62.2 mm | 未运行 | 未运行 |
| 1.10 N | 夹持抬起57.8 mm；下放阶段2.340 s几何失效 | 1.390 s几何失效，尚未进入夹持保持 | 完整周期；抬起64.2 mm | 0.216 s几何失效，尚未夹持 | 数值完成，无有效抬起（质心‑3.9 mm） |
| 1.15 N | 完整周期；抬起63.7 mm | 1.445 s几何失效，尚未夹持 | 完整周期；抬起64.9 mm | 未运行 | 未运行 |
| 1.50 N | 完整周期；抬起65.3 mm | 夹持抬起58.7 mm；下放阶段2.410 s几何失效 | 完整周期；抬起66.4 mm | 0.656 s几何失效，尚未夹持 | 数值完成，无有效抬起（质心‑0.7 mm） |

1.10 N工况：MuJoCo CPU可以夹持保持，下放阶段失效；原生MuJoCo‑Warp夹持前就失效；VBD完成全周期。1.50 N本预期全部成功，原生MuJoCo‑Warp依然失效。几何失效中断实验，无法干净对比库伦打滑阈值。PhysX两组工况夹持前失效；Genesis计算跑完但无法实现抬起。

VBD方案力反馈读数需要审慎看待：四个力矩上限条件下，抓取反馈读到峰值分别9.02、165.56、2.28、2.14 N。1.10 N的巨大尖峰发生在下放阶段（约3.00 s）；其物理合理性尚未确认。

#### 无机器人纯压缩对照实验

关闭重力，两块平板挤压球体，名义压缩量20%；保持、释放回弹，总时长1.5 s。修复导入地面平板运动问题后，全部方案都完成几何周期。

使用完全相同柔性模型，50 μs步长：MuJoCo CPU测得平板平均反力2.151 N；原生MuJoCo‑Warp 1.632 N。球体外尺寸也发生区别：平板间隙48.2 mm，两者球体延伸尺寸分别约49.3 mm、53.7 mm。不同穿透深度混淆了表观刚度差异。

无修改重复运行，CPU顶点变化为0；MuJoCo‑Warp最大0.181 mm。步长减半，分别变化0.018、0.176 mm。网格收敛、材料参数等价仍然是待解决问题。

##### 标称参数相同，但模型实现各不相同

统一输入：半径30 mm，密度1000 kg/m³，杨氏模量20 kPa，泊松比0.3，摩擦系数0.5。初始体网格：125顶点，384四面体单元。各引擎实现区别：

- **MuJoCo CPU / Native MuJoCo‑Warp** ：全自由度体积柔性；编译使用同一网格、集总质量；50 μs步长。
- **PhysX GPU** ：Isaac Sim 6.1体TetMesh，GPU动力学，显式接触偏移，休息节点映射校验；1 ms步长。刚体实验沿用原有PhysX配置。
- **Genesis** ：GPU float64隐式FEM，线性共旋本构，SAP耦合；1 ms步长。对共享表面重新网格化，内部单元不同。本实验刚体导入器不支持MJCF椭圆锥摩擦模型，属于配置不匹配。
- **Newton MJWarp + VBD** ：刚体机器人、柔性粒子分别在独立求解器求解，带滞后代理反馈；0.5 ms步长，显式形状接触阻尼0.2。机器人控制器力矩上限、摩擦、球体网格、弹性参数不变。实现参考Isaac Lab文档的实验耦合模式，不是调用Isaac Lab前端。

力测量说明

MuJoCo原生平板/夹指接触读数仅作为求解器内部临时测量。Genesis SAP冲量、Newton VBD代理反力同样导出，但早期版本无法通过零重力动量平衡校验。因此压缩场景不展示力箭头；抓取回放只展示诊断信号，不是经过验证的载荷。PhysX刚体接触探针在物体明显形变时返回零，因此不纳入反力统计。球体重量由网格质量单独计算。

仪器后续校验：独立重跑实验记录Newton耦合缓冲区每一步，确认存在一步延迟。2 N抓取读到反馈峰值34.4 N；步长减半峰值下降至2.56 N；平均抬起高度从68.6变化到66.5 mm。抬起高度相对稳定，但力峰值没有达到步长收敛。Genesis压缩实验，求解器迭代上限从5提升到50，力平衡残差最大从5.01 N下降到0.018 N。PhysX现在可以读取关节反力，无球体对照运行动量平衡残差最大0.000036 N。回放绘图使用施加给仿真的信号，不是读取到的耦合反馈。

实现经验教训：全局设置不会覆盖导入得到的几何体参数

Newton初始配置中，全局阻尼设置为0，但导入几何体形状阻尼保留200。仿真早期运行直接失效，读到1.92 kN力尖峰，力测量完全不可信。参考Franka柔性物体示例，显式设置形状阻尼为0.2之后，2 N抓取可以完成，资产、控制器不作改动。设置阻尼为0同样可以完成抓取。该修正证明耦合抓取可以跑通；但物理标定、迁移到其它场景仍然有待验证。

##### 网格加密、缩小步长能否修复抓取失效？

问题：抓取失败是网格过粗，还是步长过大？保持物理输入指令、运动不变，测试网格分辨率、仿真步长灵敏度。

针对 抓取，一共25组独立测试：5套数值配置，5套仿真方案。原始网格基线、步长减半、步长四分之一；加密网格、步长减半、步长四分之一。运动录制、控制器、力矩上限、标称材料、接触设置全部固定。Newton 保持显式形状阻尼 0.2。

结果：测试范围内，网格加密、更小仿真步长不能稳定消除失效，也不能保证抓取结果一致。MuJoCo CPU 在测试范围内相对稳定；原生 MuJoCo‑Warp 下放阶段失效现象持续存在。Newton+VBD 演示：网格有效不代表抓取一定成功，抓取维持能力取决于网格‑步长组合。加密网格反而使 Genesis 出现几何失效，没有改善结果。本套对照揭示数值敏感性；收敛性、失效机理属于开放问题。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZicPOpm9ttNzK5o83KwlkrJG8iaju8A0fQxwxUhrPejDslH8hSgoVjRSX4n6ecvsrTRdKAuuDL8QUI1j6cMpziclzDWh8RXNhDYdk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=27)

加密细分四面体：从125顶点/384单元升级至729顶点/3072单元；保持多面体边界质量约 ，不把球体变得更圆。Genesis 会对细分表面做原生重网格化，校验实际网格体积。各引擎维持自身典型步长体系：MuJoCo CPU/Warp ；Newton+VBD ；PhysX/Genesis 。两套网格不足以完成收敛性证明。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZics01EK8MABGyNpdD4G6iaANQvGqfkcHNPjdDRU5qBl0gGHrNft92W0PxO1e5SKRwAeKZOfjj2uG18N4OuZL8cR4ibibJfibUSphSg/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=28)

| 仿真方案 | 数值有效性 | 加密/减小步长带来的变化 |
| --- | --- | --- |
| MuJoCo CPU | 5/5全部完成 | 全部条件下均可以抓住球体。原始网格平均抬起 ；加密网格 。 |
| Native MuJoCo‑Warp | 5/5均在下放阶段网格翻转 | 全部达到夹持高度 。原始网格翻转时刻 ；加密网格 ；缩小步长不能消除失效。 |
| PhysX GPU 配置未调通 | 5/5抬起前网格翻转 | 基线仿真 停止；更小步长、加密网格在夹指闭合前 停止。指向初始化/接触设置问题，不能用来判定抓取能力上限。 |
| Genesis FEM / SAP | 原始网格3组完成；加密网格2组翻转 | 原始网格始终无法实现有效抬起（平均位移约 ）；两套加密网格均在抬起阶段约 发生翻转，尚未进入夹持窗口。 |
| Newton MJWarp + VBD | 5/5数值层面运行完成 | 原始网格，步长缩小，平均抬起高度从 。加密网格 工况会丢球，但 工况可以保持抓取，抬起平均 。 |

尚待解决：力读数校验；PhysX初始化‑接触校验独立于本套数值对照。单次实验看到VBD抓取结果随数值配置改变，但不能量化失效发生概率。工况耦合尖峰不在本组 研究范围内。

核心结论：柔性物体是引擎分歧最大的场景。标称材料参数、网格、抓取动作全部一致，结果却从稳定夹持到打滑、几何无效不等；加密网格、缩小仿真步长也不能让结果趋同。 **在每个引擎内部验证可变形物体仿真配置，之后再对比抓取结果。**

## 6\. 控制器调参

### 调参之后任务成功会掩盖轨迹跟踪上的取舍

前面所有实验，同一套人工设定控制器直接在全部引擎运行。这会不会掩盖引擎需要专属调参？回到三方块推物任务。允许每个引擎在同一候选网格中选出最优控制器；选择规则完全一致；使用预留布局做泛化测试。 **物理参数不对引擎调参。**

每个引擎评估27组候选控制器，组合比例增益（），阻尼增益（），推物时长（）。在3组通道布局完成评估，合计324次有效调参实验。之后把选出的控制器与原始基线控制器，在6组预留布局测试：4组通道，2组更窄通道。

##### 全部引擎选出了同一个控制器

全部候选控制器在3组筛选布局上都成功，因此选择规则进入决胜条件：平均机械臂力矩消耗更低。因此四款引擎全部选中同一套参数：比例增益 ，阻尼增益 ，推物时长 。对比基线：增益 ，推物时长 。

该一致结果来自力矩消耗优化目标， **不代表任务性能更好** 。最优参数在网格搜索三个维度的边界；相比次优候选，各引擎优势幅度均低于0.6%。

，时长00:14

<video src="https://mpvideo.qpic.cn/0bc3cualoaaazeam4vgevnvfafodw4kqbnya.f10002.mp4?dis_k=ef127e4d5fe8696e4d0d0313302c0110&amp;dis_t=1791425910&amp;play_scene=10120&amp;auth_info=XuKGtc5VbFBhvq2BtmxQAXlpCTRIHWBXf3NuGEx5MUp4ZjBWUBoTKhAKez9ZV1wi&amp;auth_key=ed5f706e8d5b0359260c7dc5089013a4&amp;vid=wxv_4725619602188058630&amp;format_id=10002&amp;support_redirect=0&amp;mmversion=false" controls="">您的浏览器不支持 video 标签</video>

预留布局上成功数 / 总6组；无失效评估实验

| 控制器 | PhysX CPU | Newton / MJWarp | MuJoCo CPU | Genesis |
| --- | --- | --- | --- | --- |
| 原始基线控制器 | 4/6 | 4/6 | 4/6 | 4/6 |
| 力矩消耗优化选出的控制器（四引擎相同） | 4/6 | 4/6 | 4/6 | 4/6 |

两套控制器在4组布局全部成功，2组布局全部失败。和推物实验保持一致：通道几何决定任务成败。

![图片](https://mmbiz.qpic.cn/mmbiz_png/Kltic3d4ibvZ8ZQibnzeTkpoDZ8Z83p7MQ3dIXmjvHxXPqiajlkEZXPf3VouZWzic0YhhclNkXYan2ibRy6u0we4gvuurs5K4B8jwnSKWUjBhEfGU/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=29)

##### 任务成功率完全相同，但轨迹不同

对比基线控制器与选出控制器在第一组成功预留布局（后方物体偏移 ），第一组窄通道压力测试布局（偏移 ）。回放采样间隔 ，力箭头可能错过短时尖峰；度量指标读取全部 采样。基线运行时长 ；选出控制器运行时长 。

表格：手爪高度方向绝对最大偏差（），基线 → 选出控制器；数值覆盖多组布局区间

| 引擎 | 4组成功90 (\\mathrm{mm})布局 | 2组失败80 (\\mathrm{mm})布局 |
| --- | --- | --- |
| PhysX CPU | 0.8‑6.2 → 1.4‑16.3 | 77‑84 → 245‑315 |
| Newton / MJWarp | 3.3‑4.7 → 22.2‑28.3 | 109.5‑110.1 → 296.6‑297.7 |
| MuJoCo CPU | 2.6‑3.8 → 17.6‑19.1 | 109.2‑109.3 → 298.7‑299.6 |
| Genesis | 0.2‑0.2 → 0.6‑0.7 | 106‑107 → 300‑304 |

成功布局场景，Genesis手爪高度仍然贴近参考轨迹；其余三套引擎在选出控制器条件下出现厘米级高度偏离。窄通道两套控制器全部失败，但选出控制器高度偏离达到 ，基线仅 。

##### 该差异来自增益，还是运动速度？

选出的控制器同时改动增益和推物时间。做对照：维持基线增益不变，把 推物时长从3s缩短至最低 。5种时长，3组布局，4引擎，合计60次实验。所有实验全部成功，手爪高度偏离均不超过 。即使最快推速，手爪竖直方向最大偏差仅 （PhysX）~（Newton/MJ‑Warp）。

![Peak vertical hand deviation versus push duration for four engines; all stay below the 10 mm tolerance.](https://mmbiz.qpic.cn/mmbiz_svg/Q3auHgzwzM41pZq6HXytic7Fs9jFE0FekrByJEvAJfulr4H71ialnF4Fgy000OGQ5WyjGLia6WVJujjibg4M4SLbqHkuiaNrtml0t8YPBFnRtMCAvkdVsBCicUyg/640?wx_fmt=svg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=31)

Peak vertical hand deviation versus push duration for four engines; all stay below the 10 mm tolerance.

因此单纯运动速度不能造成 的手爪偏移；更低的控制增益是更主要诱因。

选择协议与注意事项

排序规则优先级：布局成功数、通过实验物体数、物体最小前进进度；再取归一化机械臂力矩平方均值更低作为决胜条件。力矩消耗指标不是机械功、能量；在完整episode求平均。基线时长5s，选出控制器6s，更长推物时间改变运动过程与平均窗口，倾向选出低速方案。

选出参数 `p0.5‑d0.7‑t4` 采用测试集中最小比例增益、最小阻尼、最长推物时间。和次优选项 `p0.5‑d1‑t4` 相比，Genesis优势0.04%，MuJoCo CPU0.11%，PhysX0.42%，Newton/MJ‑Warp0.59%。需要更多重复实验判断该差距是否大于运行噪声。增益与推速同时改变，无法完全解耦；上面的速度对照做部分说明。

每组配置、布局仅运行一次，种子固定为0。预留布局不参与控制器筛选，但场景开发阶段可能已经接触。手爪偏移读取引擎原生输出手爪位姿。

启示：每个引擎独立调参，任务成功率不会发生变化，四款引擎选出同一个控制器。但手爪轨迹跟踪质量发生变化；仅仅看任务成功率无法观测该现象。 **选择控制器时，必须把轨迹跟踪、接触载荷作为显式评判标准，不能只看任务成功与否。**

## 7\. 运行性能

### 单环境追求CPU速度；大规模并行仿真选择GPU

单环境仿真，MuJoCo CPU速度遥遥领先：无接触Panda机械臂仿真约 步每秒；对比GPU上MuJoCo‑Warp约 ，Genesis约 。单个小规模世界不足以占满GPU算力，每一步的开销占主导。

当大量并行仿真环境同时运行，局面反转：8192个Panda并行世界，MuJoCo‑Warp总吞吐量21.6M步每秒，Genesis11.8M步每秒。MuJoCo‑Warp在全部测试批量规模下吞吐量领先；但批量继续增大，两者差距缩小：128并行世界时相差约3倍；131072并行世界时仅相差约1.3倍。

测试条件：无接触Panda跟踪，步长，关闭渲染；单位百万步每秒；取三次运行中位数。硬件RTX PRO 5000 Blackwell（48GB），主机Ryzen 9 9900X。

限制说明：MuJoCo CPU仅测单环境，没有利用主机16逻辑核做多环境并行；PhysX没有做批量性能测试；Genesis使用float64，MuJoCo‑Warp使用float32。131072并行世界GPU显存占用：MuJoCo‑Warp6.2GiB；Genesis4.9GiB。批量运行轨迹与单世界运行完全一致。

| 并行世界数量 | MuJoCo CPU | MuJoCo‑Warp (GPU) | Genesis (GPU) |
| --- | --- | --- | --- |
| 1 | 0.17 | 0.006 | 0.002 |
| 128 | — | 0.61 | 0.21 |
| 8192 | — | 21.6 | 11.8 |
| 32768 | — | 33.1 | 22.4 |
| 131072 | — | 35.2 | 26.4 |

小结：单环境Panda基准测试，MuJoCo CPU速度最快。大批量并行仿真场景，MuJoCo‑Warp、Genesis获得更高总吞吐量。MuJoCo‑Warp在全部测试批量规模下吞吐量领先；更大批量下Genesis性能差距缩小。

## 8\. 讨论与展望

开展下一次策略评估时需要考量的要点

经验总结

从单物体场景到拥挤场景、软体物体以及控制器调优的过程中，可以归纳出四条反复出现的经验。

在归咎于物理引擎本身之前，先核查导入的模型数据。铰链测试中出现显著的引擎差异，根源其实是导入的关节电枢；只有在导入之后重新核对质量、惯性以及关节坐标系，Panda机械臂才能够在不同引擎上得到一致结果。

结果一致的表象之下，可能隐藏着完全不同的物理行为。停止距离可以做到误差仅0.05 毫米，但峰值作用力却能够相差十倍；即便控制器的任务成功率完全相同，它们实际的运动轨迹也会大相径庭。除了报告任务成功率之外，还应当同时输出作用力数据、运动轨迹以及失效的严重程度。

在对各个引擎进行优劣排序之前，先测量同一引擎内部本身的结果波动。在拥挤清扫场景当中，GPU上使用完全相同输入进行多次重复运行，得到的结果离散程度已经不亚于不同物理引擎之间的差异；而在推物体场景下，仅仅1毫米的布局改动，就会让部分引擎里物体发生远大于其他引擎的位移。

必须在每一款引擎当中单独验证软体物体效果。仅仅对齐名义上的材质参数，并不能保证抓取结果保持一致；细化网格或是调整仿真时间步长，也无法消除这类结果差异。

综合以上内容，这些实验构成了一套跨引擎对比的验证工作流：从单物体起步，逐步增加物体交互；先测试机器人无接触自由运动，再测试接触工况；每一个步骤都复核导入模型，将仿真步长减半并且重新运行实验。至于引擎选型本身，CPU版本MuJoCo适合单一场景下的开发与调试；而GPU加速引擎更适合批量训练。

使用不止一款引擎开展评估

恰恰是策略最容易暴露缺陷的场景下，不同引擎之间的仿真结果分歧最为明显：高接触的拥挤环境、紧配合插入任务以及软体物体仿真。因此，使用第二款物理引擎额外跑一遍评估，是成本很低的鲁棒性校验手段。针对经过学习得到的策略，应当把观测pipeline、动作解析逻辑、控制器连同策略权重一并做冻结处理。当出现评估分数落差时，不要直接归因于策略本身的好坏；先用上面提到的校验手段开展排查。回放已经记录下的控制指令，可以帮助把系统动力学效应与闭环感知带来的影响分离开。我们后续的博客文章就会以此为主题，研究在某一个引擎训练完成的策略迁移到其他引擎上做评估的情况。

修正仿真场景本身，不要单纯为提升成功率去调参

场景搭建依然需要针对不同引擎分别细致处理：导入得到的电枢数据、缺失的碰撞掩码、标记错误的几何体，这些问题都曾经干扰过我们早期的实验结果。应当把针对物理模型规格的修正，和为了提高任务成功率而进行的调优两件事区分开来。记录每一个引擎独有的数值参数设置，保留原始对照组，并且每一次改动之后都重新跑一遍对照实验。我们针对控制器的研究也说明了目标函数必须清晰明确的原因：平均控制作用力降低并没有带来成功率提升，反而允许出现了更大的轨迹跟踪偏差。

局限性与后续工作

本次对比针对的是特定版本实现、特定仿真场景以及特定的参数范围。绝大多数配置仅做了单次测试；重复对照实验也说明，如果想要得出普适性更强的结论，就必须开展多次重复测量。部分仿真场景最初是基于CPU版MuJoCo开发的；在场景开发阶段，就已经筛选过一部分控制器布局。这就使得任务选择本身会偏向开发者更为熟悉的构型。机器人采用了简化的碰撞几何体，很多时候仅仅建模了指尖软垫；同时本次实验使用显式脚本化控制。原生驱动层面的可移植性、学习策略的跨引擎迁移能力、从仿真迁移到真实世界的仿真‑实机精度，都还需要另外开展实验，并且配合真实硬件测量进行校验。本系列后面两篇博文，将会分别讨论学习策略迁移以及仿真到真实世界的精度问题。

现阶段最亟待完成的验证工作包括PhysX软体初始化问题，以及剩余耦合作用力诊断；其次是Genesis引擎在拥挤清扫场景下后期出现的作用力尖峰。相关警示标注已经写在对应的实验结果旁。除完成上述校验以外，增加重复实验、校准接触与材质模型、开展系统性收敛性研究，都可以进一步强化整套对比结论的可信度。