# -*- coding: utf-8 -*-
"""
Generate SC3 Prof2 concise exam review PDF
"""

from fpdf import FPDF
import os

class SC3ReviewPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        # Use SimSun for regular, SimHei for bold (both work with write/cell)
        fp = 'C:/Windows/Fonts/simsun.ttc'
        fpb = 'C:/Windows/Fonts/simhei.ttf'
        if not os.path.exists(fp):
            fp = 'C:/Windows/Fonts/msyh.ttc'
        if not os.path.exists(fpb):
            fpb = fp
        self.add_font(family='CN', style='', fname=fp)
        self.add_font(family='CN', style='B', fname=fpb)
        self.cn_font = 'CN'
        self.set_auto_page_break(True, 15)

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font(self.cn_font, '', 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, 'SC3 Prof2 考前复习资料', align='L')
        self.cell(0, 4, f'Page {self.page_no()}', align='R', new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.cn_font, '', 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'SC3 Prof2 - Examen 30 Juin 2026', align='C')

    def cover_page(self):
        self.add_page()
        self.ln(40)
        self.set_font(self.cn_font, 'B', 28)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, 'SC3 - Supply Chain Management', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        self.set_font(self.cn_font, 'B', 22)
        self.cell(0, 12, 'Prof2 考前冲刺复习资料', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        self.set_font(self.cn_font, '', 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, '仓储管理 + 运输与国际贸易', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        self.cell(0, 8, '知识点精简版 | 应试导向 | 去除案例/图片/视频/课堂互动', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(15)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(50, y, 160, y)
        self.ln(10)
        self.set_font(self.cn_font, '', 11)
        self.cell(0, 7, '考试日期: 2026年6月30日', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, '课件来源: （已压缩）SC3 prof2.pdf (506页)', align='C', new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, '语言: 中文为主，法语关键术语保留', align='C', new_x="LMARGIN", new_y="NEXT")

    def sec(self, title, num=""):
        self.ln(4)
        self.set_font(self.cn_font, 'B', 14)
        self.set_text_color(0, 51, 102)
        text = f"{num}. {title}" if num else title
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub(self, title):
        self.ln(2)
        self.set_font(self.cn_font, 'B', 11)
        self.set_text_color(51, 102, 153)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font(self.cn_font, '', 9)
        self.set_text_color(40, 40, 40)
        self.write(5, text)
        self.ln(7)

    def bul(self, text, indent=5):
        self.set_font(self.cn_font, '', 9)
        self.set_text_color(40, 40, 40)
        self.set_x(self.l_margin + indent)
        self.write(5, '- ' + text)
        self.ln(6)

    def key(self, text):
        self.set_font(self.cn_font, 'B', 9)
        self.set_text_color(180, 50, 50)
        self.set_x(self.l_margin + 3)
        self.write(5, '★ ' + text)
        self.set_text_color(40, 40, 40)
        self.ln(7)

    def fbox(self, formula, explanation=""):
        self.set_fill_color(245, 245, 250)
        self.set_draw_color(100, 100, 160)
        self.set_font(self.cn_font, 'B', 10)
        self.set_text_color(0, 51, 102)
        self.set_x(self.l_margin + 5)
        self.cell(self.w - self.r_margin - self.l_margin - 10, 7, formula, fill=True)
        self.ln(9)
        if explanation:
            self.set_font(self.cn_font, '', 8)
            self.set_text_color(80, 80, 80)
            self.set_x(self.l_margin + 5)
            self.write(4.5, explanation)
            self.ln(6)
        self.ln(3)

    def tbl(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [(self.w - self.r_margin - self.l_margin) / len(headers)] * len(headers)
        # Header
        self.set_font(self.cn_font, 'B', 8)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align='C')
        self.ln()
        # Rows
        self.set_font(self.cn_font, '', 8)
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(245, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_text_color(40, 40, 40)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 5.5, str(cell), border=1, fill=True, align='C')
            self.ln()
        self.ln(3)


def build_pdf():
    pdf = SC3ReviewPDF()

    # ===== COVER =====
    pdf.cover_page()

    # ===== PART 1: ENTREPOSAGE =====
    pdf.add_page()
    pdf.sec("仓储管理 (Entreposage)", "一")

    pdf.sub("1.1 仓库角色与使命 (Roles & Missions)")
    pdf.body("仓库(Entrepot)是用于容纳库存并保证其可用性的技术手段，通过管理接收、存储、拣货和发货流程来控制运营成本。库存(Stock)是为满足内外部客户需求而持有的商品。")
    pdf.bul("仓库两大使命: 1) 存放库存 (Heberger le stock) 2) 调节流量 (Reguler le flux) — 流入 vs 流出")
    pdf.bul("库存优点: 平衡供需、批量采购节省成本、防范不确定性、保障分销网络安全")
    pdf.bul("库存缺点: 资金占用(Immobilisation financiere)、专用资源(建筑/人员/设备)、过时/损坏/盗窃")
    pdf.key("库存掩盖问题 (Le stock masque les problemes): 库存错误、预测错误、低效流程、沟通问题、生产故障")
    pdf.body("库存的调节功能(Fonction d'ajustement): 作为缓冲吸收供需差异(供应延迟、生产计划、商业优先级、需求预测误差等)。")
    pdf.bul("BFR (Besoin en Fonds de Roulement) = Stock + Client - Dettes d'exploitation；库存消耗营运资金")

    pdf.sub("1.2 仓库8大构成要素 (Les 8 Moyens)")
    pdf.body("仓库 = 建筑(Batiment) + 人员(Hommes) + 设备(Materiel) + 方法(Methodes) + IT系统 + 产品(Produits) + 作业(Operations) + 参与者(Acteurs)")

    pdf.sub("1.3 仓库建筑 (Le Batiment)")
    pdf.bul("仓库等级: A/B/C级，按单元格尺寸、高度、停车位等分类")
    pdf.bul("U型仓库(Entrepot en U): 最常见标准，单元约6,000m2，带喷淋系统(sprinkler)")
    pdf.bul("防火墙2小时耐火 + 内部隔离门；高度>7.20m视为大高度")
    pdf.bul("三大环保认证: HQE(法国)、BREEAM(英国)、LEED(美国)；HQE建筑成本+5%至+15%")
    pdf.bul("ICPE法规: 1510类(可燃物料-最常见)、1530类(木材纸张)、1432类(可燃液体)")
    pdf.bul("SEVESO指令: 危险物质重大事故风险控制 (SEVESO III, 2015年6月1日生效)")

    pdf.sub("1.4 装卸平台 (Les Quais) - 仓库的肺部")
    pdf.bul("装卸区占总面积约15%；法定最少6个装卸口/单元")
    pdf.bul("卡车制动系统(calage)强制使用 — 1996年4月26日法令，运输商责任")
    pdf.bul("设备: 平台调整器(niveleur)、防风裙边(jupe)、LED照明、安全幕帘")
    pdf.bul("EPI个人防护: 安全鞋 + 高可见性背心(EN 471标准)")
    pdf.bul("照明要求: 100 lux；外部平台边缘地面标记+50cm禁行区")
    pdf.bul(">3.5T车辆: 发货方(chargeur)负责装卸和固定(arrimage)；<3.5T: 发货方或运输商")

    pdf.sub("1.5 仓储核心流程 (Les Processus)")
    pdf.body("流程形式化四层次: 供应链概览图(Vision Macro) -> 活动分析 -> 流程图(Logigramme) -> 岗位操作指南(Instruction au poste)")
    pdf.body("核心流程: 1-4接收与控制(Reception & Controle) -> 5-6上架(Mise en stock) -> 7-8拣货(Picking) -> 9-10检验与包装 -> 11-13发货(Expedition) -> 14不合格品管理 -> 15增值服务(VA) -> 16退货管理")
    pdf.key("接收检验: 'sous reserve de deballage'(保留拆包检验权)在法律上无效！异议须在3天内挂号信提出。")
    pdf.bul("检验策略: 按产品/品类、抽样(echentillon)、按供应商、重量检验(ponderal)")
    pdf.bul("不合格品(NC): 指定隔离区(Zone quarantaine)，限15天临时存放，定义出库场景和负责人")

    pdf.sub("1.6 流程分析方法")
    pdf.bul("链条法(Methode des Chainons): 最小化流程交叉和搬运指数(distance x quantite)，6步法")
    pdf.bul("IGM法(Indice Global de Manutention): 图形方法，符号: O操作 口检验 三角形存储 ->移动 D等待")
    pdf.bul("关系图(Graphique de Relations): 计算职能间相互依赖，4步法")

    pdf.sub("1.7 库存管理工具")
    pdf.bul("DDMRP (2002, Ptak & Smith): 5步迭代 — 1)战略库存定位 2)缓冲配置(4级) 3)动态调整 4)需求驱动计划 5)可视化协作执行")
    pdf.bul("重心法(Barycentre): 基于「重量 x 距离」计算最佳仓库地理位置")
    pdf.bul("Wilson公式(1934): 优化订购频率 = 权衡持有成本(Cout de possession) vs 订购成本(Cout de passation)")
    pdf.bul("ABC分析(Pareto 20/80): A=20%参考/80%出货量/重点管理(+++); B=30%/15%/(+); C=50%/5%/(=)")
    pdf.bul("基尼系数(Gini): 0=完全平等 1=完全不平等，检验ABC分类适用性")
    pdf.bul("核心指标: CMM(月均消费量)、SM(平均库存)、TR(周转率)=年出库/SM、TC(覆盖率)=SM/CMM、SS(安全库存)")
    pdf.bul("库存图形: 周转库存 -> 安全库存 -> 订货点(Point de commande) -> 补货 -> 缺货(Rupture)")

    pdf.sub("1.8 物料搬运支持 (Supports de Manutention)")
    pdf.bul("托盘Palette Europe: 1200x800x154mm, 25kg, 载重1500kg+, 4入口9块, 15-20欧")
    pdf.bul("VMF托盘(玻璃业): 1200x1000mm, 载重1500kg；美国托盘(chevrons): 1200x1000mm, 载重1000kg")
    pdf.bul("半托盘(Dusseldorf/EPAL): 600x800mm, 载重500kg, 10-12kg")
    pdf.bul("其他: 箱式托盘(box)、滚轮(roll)、塑料箱、大袋(big bag 500kg-1T)、IBC液体容器(1000L)、纸板palbox、等温集装箱(KTM pharma)")
    pdf.bul("纸箱(Cartons): 单瓦楞(Micro E 1.4mm ~ Grosse A 4.9mm)、双瓦楞(BC/BE 4.2-8mm)、三瓦楞(TC ACC 13-15mm)")
    pdf.key("NIMP15标准: 厚度>6mm的木质包装须去皮(DB)+热处理(HT)+窑干(KD)并标记。欧盟2010年3月18日起禁止溴甲烷(MB)熏蒸。")

    pdf.sub("1.9 叉车与仓库通道设计 (Chariots & Largeur d'Allees) ★考试重点")
    pdf.body("叉车(Chariot automoteur): 配备前叉的机动搬运设备，用于提升/移动托盘、集装箱或箱子。")
    pdf.bul("发动机: 燃气热力(petits)、柴油热力(gros)、电动(电池)；热力在封闭室内须控制CO<50cm3")
    pdf.bul("载重: 1.5T(托盘)至40T+；提升高度>10m；潜力寿命: 60,000h或15-18年")
    pdf.bul("购买成本仅占TCO的7%；法国市场: Linde 30% > Junheinrich ~20% > Toyota ~18% > Still ~14%")
    pdf.bul("电池类型: 铅酸(10年寿命)、锂电池(2014年, 更贵/更快充电)、凝胶电池(6-7年寿命)")
    pdf.bul("氢燃料电池(2015年起): 零CO2(仅水), 充电1-3分钟, 无需充电室")

    pdf.body("通道宽度由叉车转弯半径决定 — 叉车类型与通道对应:")
    pdf.tbl(
        ["叉车类型 (Type de Chariot)", "通道宽度 (Largeur d'Allee)"],
        [
            ["双向/极窄通道叉车 (Allées très étroites)", "1.40m"],
            ["三向/侧向叉车 (Tri-directionnel/Lateral)", "1.80m"],
            ["伸缩式叉车 (Retractable 4 roues)", "2.60m"],
            ["前驱叉车 (Frontal 4 roues)", "3.60m"],
        ],
        [100, 55]
    )

    pdf.fbox("四轮叉车通道: A = R + B + profondeur_tablier + 0.2m", "R=轴距, B=托盘/货物宽度")
    pdf.fbox("三轮叉车通道: A = L + B + 0.2m", "L=车身长(含tablier), B=托盘/货物宽度")
    pdf.fbox("双向通道(允许交汇): 宽1 + 宽2 + 外侧各50cm + 中间40cm = 通道总宽", "")
    pdf.fbox("单向通道(1974年7月30日法令): 车辆/货物宽 + 1m", "Code du travail, Arrete du 30 juillet 1974")

    pdf.sub("1.10 叉车法规与安全 (CACES & Securite)")
    pdf.bul("CACES许可证(R489, CNAMTS): 操作员须持证上岗 + 体检 + 雇主授权")
    pdf.bul("VGP (Visite Generale Periodique): 叉车及升降机构每6月强制检修并登记")
    pdf.bul("仓库第一事故原因 = 叉车！每年约15-20人死亡: 31%翻车 37%行人被撞。70%的致命事故由移动中的叉车造成")
    pdf.bul("行人安全(Code du travail R.4323-52): 行人通道>=80cm宽，须护栏隔离；存储区域禁止行人")
    pdf.bul("货架立柱保护: 塑料+泡沫方案经认证可抵御<=2T叉车8km/h撞击")
    pdf.bul("横梁弯曲(effet banane): 永久变形必须更换")

    pdf.sub("1.11 充电室 (Local de Charge)")
    pdf.fbox("充电器功率 P(KW) = V(volts) x A(amperes) / 1000", "例: 48V x 120A = 5.7KW")
    pdf.bul("典型功率: 三向叉车~7KW, 侧向~6KW, 前驱~5KW, 拣货车~2.5KW, 电动堆高机~1KW")
    pdf.bul("安全: 禁烟/禁明火(氢气)、放电不超80%、加蒸馏水/去离子水不加酸、充电开盖、检查接线柱")

    pdf.sub("1.12 存储结构 (Structures de Stockage)")
    pdf.bul("关键法规: EN 15572+2010年10月22日法令(地震)；EN 15635(每12月强制检查+书面报告)")
    pdf.bul("禁止将货架固定在墙上(2002年8月5日防火令, 1510类)；货架顶部距屋顶>=1m")
    pdf.bul("约75%仓库面积用于存储；最佳填充率: 85%")
    pdf.bul("传统仓库存储密度: 1.2-1.5托盘/m2；高密度自动仓库: 最高3托盘/m2")
    pdf.bul("货架元素: 立柱(Echelle 7-23T) + 横梁(Lisse 0.9/1.8/2.7/3.6m) + 底板(cale) + 支撑(traverse) + 护栏")

    pdf.body("货架计算6步法:")
    pdf.bul("1.确定托盘特征(满载重量/高度) -> 2.选择横梁(长度=数量x[面宽+间隙]) -> 3.计算各层高度 -> 4.确定层数(基于檐下高度) -> 5.确定立柱(高度=累加-顶层高+横梁高+1m/INRS) -> 6.计算跨数")

    pdf.fbox("标准货架面积: S = (A/2 + L + D) x (l + D) x N/d", "A=通道宽, L=托盘长, l=托盘宽, D=安全距0.1m, d=层数, N=托盘数")
    pdf.fbox("堆积式货架: S = (A/2 + a(L+D)) x (l+D) x N/(d*a)", "a=堆积深度(托盘数)")

    pdf.bul("各类货架: 标准式、窄通道式、堆积式(accumulateur)、穿梭式(navette <=750kg, 20-30位)、动态式(FIFO最佳)、移动式(mobile)、悬臂式(cantilever)、夹层(mezzanine ~200欧/m2)、堆垛储存(vrac/gerbage)")
    pdf.bul("横梁承重: 1-4T(取决于钢材截面和长度)")

    pdf.sub("1.13 机械化与自动化 (Mecanisation & Automatisation)")
    pdf.bul("自动化(Automatisation)=无人介入；机械化(Mecanisation)=人+辅助工具")
    pdf.bul("WCS (Warehouse Control System): 管理机械化流程，WMS的补充")
    pdf.bul("分散指数(Indice de fractionnement) = 出库单位数/入库单位数；>10时建议自动化")
    pdf.bul("拣选生产率: 纸单基准100 -> RF扫码+5% -> Voice-picking+10% -> 机械化流水线+20%")
    pdf.bul("电商仓库: 人员成本可达运营成本的60%，减少无效移动至关重要")
    pdf.bul("自动化局限: 缺乏灵活性、难以重配置、容量有限、安装与维护成本高")
    pdf.bul("适用场景: 规律活动+低季节性+高库存+电商拆零拣选")
    pdf.bul("设备种类: 自动存取机(Transstockeur 托盘/料箱)、Kardex旋转柜、AGV自动导引车、模块化输送机(Plug&Carry)、自动包装机(Neopost ID 3D优化-40%体积)、码垛机器人、分拣机(trieur)")
    pdf.bul("Kiva Systems: Amazon 2012年7.75亿美元收购, 2016年已有45,000台机器人在全球仓库运行")
    pdf.bul("Pick to light: 灯光+数量显示 -> 操作员确认 -> 库存实时更新")
    pdf.bul("Pick to voice: 语音指令 -> 双手自由 -> 不需标签 -> +10%效率 (设备成本2500-3000欧/人)")
    pdf.bul("Goods to Man(货到人): Scallog系统450-600次取货/小时 vs 传统100-150次/小时")

    pdf.sub("1.14 WMS仓库管理系统")
    pdf.bul("WMS核心功能: 产品(编号/批次/日期/...) + 状态(流程节点) + 位置(精确仓库地址) = 三位一体管理")
    pdf.bul("WMS数据表: 产品表(<=50属性)、位置表、距离表、包装表、供应商/客户表、人员表、流程树、拣货模式")
    pdf.bul("WMS质量期望(调查排名): 1.易用性 2.进化能力 3.流程匹配度 4.与其他系统接口 5.参数配置便利")
    pdf.bul("WMS安装原因: 1.生产率提升 2.数据可靠性 3.流程绩效 4.人力资源优化 5.缩短周期")
    pdf.bul("关键原则: WMS适应操作流程，而非反之！第一步永远是详尽的流程功能分析")
    pdf.bul("WMS高级功能排名: 1.仪表盘 2.退货管理 3.订单管理 4.TMS对接 5.电商模块")
    pdf.bul("条码打印: 热转印技术 203DPI, 单头寿命>80km")
    pdf.bul("RF扫码枪: 有线100欧起, 无线400欧起, 多功能<=1500欧")
    pdf.bul("Smart Glasses智能眼镜(2014年): 替代语音/射频, 视线引导+双手自由")

    pdf.sub("1.15 仓库仪表盘 (Tableau de Bord)")
    pdf.bul("BI商业智能: 从多源系统(ERP/WMS/TMS/CRM)通过ETL(Extract Transform Load)抽取数据至Data Warehouse")
    pdf.bul("6大测量维度: 量(Volumes) + 时(Delais) + 本(Couts) + 能(Capacites) + 绩(Performance) + 产(Productivite)")
    pdf.bul("量: 接收/上架/拣货/发货/运输量 时: 卸货/接收/备货/装载/运输时间")
    pdf.bul("本: 建筑/人员/设备/消耗品/结构成本 能: 存储/设备/人员利用率")
    pdf.bul("绩: OTD/OTIF达成率、库存准确率、cut-off遵守率 产: 操作员/机器效率")
    pdf.key("黄金法则: 你不能管理你无法测量的；你不能测量你无法定义的；你不能定义你不理解的。")

    pdf.sub("1.16 仓库人力资源管理 (GRH)")
    pdf.bul("人力是仓库第一支出；管理核心: 可变编制+长短期员工混合+工作量预测+排班+执行规章制度")
    pdf.bul("组织架构图(organigramme)与岗位说明书(fiches de poste): 明确汇报线+职责，员工签字,<=1页")
    pdf.bul("GPEC (Gestion Previsionnelle de l'Emploi et des Competences): 前瞻性HR管理, 法国三年协商义务")
    pdf.bul("多技能矩阵: 0=不会 1=培训过未实操 2=不完全自主 3=完全自主；按人员-活动建立矩阵")
    pdf.bul("培训: 法规培训(CACES/安全/化学风险)+内部培训(流程/WMS/产品/仓库规则)")
    pdf.bul("临时工(interim): 吸收活动高峰，建议同时联系2-3家中介")
    pdf.bul("BtoC电商所需人力远高于批发(精细操作+大量拣货+单件包装)")

    pdf.sub("1.17 经济绩效 (Pilotage Economique)")
    pdf.bul("运营账户: 例 — 20,000m2分销中心~100员工~30台叉车 -> 月均45万欧")
    pdf.bul("UO (Unite d'Oeuvre/计费单位) = 操作成本/活动量 -> 每单位成本, 用于内外部计费")
    pdf.bul("UO计算4步: 1)追踪成本(固定/可变) 2)按活动分摊 3)测量活动量 4)UO x 实际活动 = 计费")
    pdf.bul("季节性: 在投资成本和期望服务水平之间权衡；策略: 库存调节/预期/促销 vs 扩展存储能力")
    pdf.key("仓库核心矛盾: 生产(稳定大批量) vs 销售(丰富品种低缺货) vs 财务(降低库存成本) — 物流人居中调和")

    # ===== PART 2: TRANSPORT ROUTIER =====
    pdf.add_page()
    pdf.sec("公路运输 (Transport Routier)", "二")

    pdf.sub("2.1 市场概况")
    pdf.bul("欧洲市场极其碎片化: 80-90%企业<10名员工；西班牙和意大利最分散")
    pdf.bul("德国和法国为最大的公路运输市场(百万吨计)")
    pdf.bul("市场结构: 约100,000家单车公司(one truck companies)")

    pdf.sub("2.2 卡车重量与尺寸法规 (PTRA/PTR)")
    pdf.key("卡车总行驶重量限制 (Code de la route R 312-4 II) ★重点")
    pdf.bul("PTRA (Poids Total Roulant Autorise): 由DREAL确定, 登记在行驶证上")
    pdf.bul("PTR最大: <=4轴 38T；>4轴 44T (1971:35T -> 1989:40T -> 2014:44T)")
    pdf.bul(">44T需特别许可(Transport exceptionnel, R 433-1)或圆木运输(R 433-9)")
    pdf.bul("单车(Vehicules isoles): 2轴max 19T; 3轴max 26T; >3轴max 32T; 长max 12m; 宽2.55m(冷藏2.60m)")
    pdf.bul("铰接车(Vehicules articules): 牵引车2-3轴; 长max 12m; 宽max 2.55m(冷藏2.60m)")
    pdf.bul("欧盟拒绝超级卡车(mega-camions): 25.25m长/60T, 2015年2月被否决跨境流通")

    pdf.sub("2.3 卡车速度与驾驶时间监控")
    pdf.bul("行车记录仪(Chronotachygraphe): 90年代起；数字式强制安装于新车及替换模拟式设备")
    pdf.bul("适用范围: >8座客运车辆 + >3.5T货运车辆")
    pdf.bul("记录内容: 速度、驾驶时间、工作时间、休息/待命时间 -> 确保遵守法定休息时间和最大驾驶时间")
    pdf.bul("数字式记录仪: 通过UEV(车载单元)记录，数据可远程读取和分析")
    pdf.bul("实时信息信标(Ekolis): GPS定位+温度监控+胎压监控，数据通过安全无线电回传")

    pdf.sub("2.4 司机资质")
    pdf.bul("FIMO (Formation Initiale Minimale Obligatoire): 初始最低强制培训")
    pdf.bul("FCOS (Formation Continue Obligatoire de Securite): 持续安全强制培训")
    pdf.bul("长途司机(chauffeur routier) vs 配送司机(chauffeur-livreur): 不同工作性质和培训")

    pdf.sub("2.5 运输成本定价")
    pdf.fbox("运输成本 PRF = a(EUR/km) x km + b(EUR fixe)", "例: PRF(A->B) = 0.9EUR x 80km + 100EUR = 172EUR")
    pdf.bul("成本要素结构: 燃料/轮胎/维修(按公里可变) + 司机工资+社保(部分公里部分固定) + 保险/货损/管理(按线路固定)")
    pdf.bul("市场价格仍由市场供需决定，成本分析用于判断盈亏")

    pdf.sub("2.6 排放标准 (Normes Euro)")
    pdf.bul("Euro排放标准: 欧盟对新车设定越来越严格的污染物排放限值，CO2不在标准内(不视为直接污染物)")
    pdf.bul("Euro VI (2014年起): 车辆价格上涨约7%；法国市场新车注册量下降11%")
    pdf.bul("经济驾驶(eco-conduite): 低转速换挡+稳定速度+低发动机转速+预判交通+维护车辆")
    pdf.bul("减少排放五步: 1)改善空气动力学+优化动力链 2)培训经济驾驶 3)优化装载(双层挂车/铝制轻量) 4)CO2计算器 5)替代能源技术")
    pdf.bul("法国ecotaxe(环保税): 被理解为'额外税负'，缺乏明确投资方向，最终被放弃")

    pdf.sub("2.7 公路运输服务类型 (L'offre Transport)")
    pdf.bul("包车(Affretement): 整车满载不中转，利用全部运力 -> 点对点")
    pdf.bul("零担(Transport de lots): 拼车共享运力不中转 -> A/B/C多点")
    pdf.bul("拼货(Groupage): <3T零散货物，按吨公里计费，经平台中转 -> 多点集散")
    pdf.bul("快递(Messagerie): <3T包裹，每日取派，按重量计费，经星形网络中转")

    pdf.sub("2.8 运输合同与参与者")
    pdf.bul("国内运输: Code des transports + 书面协议 -> 默认适用标准合同(contrat type)")
    pdf.bul("国际运输: CMR公约(Convention de Geneve)优先于法国国内法")
    pdf.bul("主要参与者类型: 个体户(Artisans)、牵引运输商(Tractionnaires)、专业运输商(Specialises)、物流服务商(Prestataires)")
    pdf.bul("货运代理(Affreteur): 为运输商找货源/为货主找运力，优化回程满载")
    pdf.bul("货运交易所(Bourses de fret): 供需在线匹配平台 (如TimoCom 2014年5890万条信息)")

    pdf.sub("2.9 快递/零担网络 (Focus Messagerie)")
    pdf.bul("星形网络(Hub & Spoke): 包裹经平台间干线转运，最大化覆盖区域")
    pdf.bul("分类: 单包裹(<30kg, >24h) / 标准(<3T, >24h) / 快速(=24h, <3T) / 特快(<24h, <3T)")
    pdf.bul("运输平台 vs 仓库: 平台=货物不停留极短停+无增值服务；仓库>=24h存储+picking+增值服务")
    pdf.bul("Hub案例: UPS Cologne-Bonn扩建2亿美元，190,000包裹/小时，平均15分钟通过时间")

    pdf.sub("2.10 社会倾销 (Dumping Social)")
    pdf.bul("2014年7月10日法(n.2014-790): 发包方( donneur d'ordre)须核实承包方外派员工的劳动监察申报")
    pdf.bul("法国企业须保存承包方申报副本并纳入企业人事登记册")
    pdf.bul("违规后果: 发包方因未核实将面临行政罚款(amende administrative)")

    # ===== PART 3: INCOTERMS 2020 =====
    pdf.add_page()
    pdf.sec("国际贸易术语 (Incoterms 2020)", "三")

    pdf.sub("3.1 基本概念")
    pdf.bul("ICC(国际商会, 1919年巴黎创立): 全球最大商业组织, 4500万+成员, 100+国家")
    pdf.bul("Incoterms = International Commercial Terms，界定买卖双方在国际贸易中的责任、风险和费用")
    pdf.bul("注意: Incoterms不界定物权转移时间！保险仅CIP和CIF有规定")
    pdf.bul("表达格式: 三字母缩写+三个点(精确地址！) 例: FCA Shanghai Port")
    pdf.bul("1936年首版6个术语(仅海运) -> 2020年最新版本，覆盖所有运输模式")

    pdf.sub("3.2 四大类Incoterms 2020")
    pdf.tbl(
        ["类别", "术语", "核心含义", "风险/费用"],
        [
            ["E 启运(Depart)", "EXW", "卖方义务最小: 工厂交货", "买方承担全部"],
            ["F 主运费未付", "FCA/FAS/FOB", "卖方交货至承运人", "买方承担主运输"],
            ["C 主运费已付", "CFR/CIF/CPT/CIP", "卖方付主运费但风险由买方承担", "风险归买方"],
            ["D 到达(Arrivee)", "DAP/DPU/DDP", "卖方承担全部风险和费用到目的地", "卖方承担全部"],
        ],
        [28, 35, 55, 50]
    )
    pdf.bul("仅用于海运和内河水运: FAS, FOB, CFR, CIF")
    pdf.bul("适用于所有运输方式(多式联运): EXW, FCA, CPT, CIP, DAP, DPU, DDP")

    pdf.sub("3.3 买方策略选择")
    pdf.bul("启运条款(E/F类): 买方掌控运输成本和节点 -> 优点: 最佳成本管控；缺点: 需建立采购物流组织")
    pdf.bul("到达条款(C/D类): 卖方负责运输 -> 优点: 无需自有物流管理；缺点: 成本透明度低")
    pdf.bul("选择取决于: 双方运输策略+谈判能力+力量对比")

    pdf.sub("3.4 国际贸易相关主题 (Sujets Connexes)")
    pdf.bul("NIMP15: 木质包装植物检疫标准(>6mm须处理标记)")
    pdf.bul("海关(Douanes): DELTA申报、保税仓储(Stock sous douane)、AEO/OEA认证经营者")
    pdf.bul("支付(Paiements): 信用证(CREDOC)、跟单托收(Remise documentaire)、预付")
    pdf.bul("保险: 航次保险(Assurance au voyage)、DTS特别提款权(Droits de Tirage Speciaux)、从价税(Ad Valorem)")
    pdf.bul("运输模式选择: 短距(<500km)公路最优；中距(500-3000km)铁路有竞争力；长距(>3000km)海运/空运")
    pdf.bul("风险信息源: MOCI(国际贸易导报)、COFACE(外贸保险)、央行经济公报、使馆经济参赞")

    # ===== PART 4: TRANSPORT MARITIME =====
    pdf.sec("海运与空运 (Transport Maritime & Aerien)", "四")

    pdf.sub("4.1 海运船舶术语")
    pdf.bul("Conventionnel: 传统件杂货；Porte-conteneur: 集装箱船；Feeder: 支线集装箱船(~5000 TEU)")
    pdf.bul("Panamax: 可通过巴拿马运河最大船型；Post-Panamax: 超过巴拿马通行能力")
    pdf.bul("Ro-ro: 滚装船(运输带轮货物)；Vraquier: 散货船(Bulk)；Gazier/Methanier/Petrolier: 液/气体运输船")

    pdf.sub("4.2 主要航线及耗时")
    pdf.bul("中国->美国东岸(经巴拿马): 31天 | 中国->美国西岸: 17天")
    pdf.bul("美国->欧洲: 9天 | 欧洲->南美: 18天 | 欧洲->非洲(几内亚湾): 13天")
    pdf.bul("欧洲->中国(经苏伊士): 30天 | 欧洲->中国(经好望角): 41天")

    pdf.sub("4.3 代表船型")
    pdf.bul("Maersk B级(2006): 4,000 TEU, 294m x 32m, 36节~70km/h — 快速但高能耗, 已转用作feeder")
    pdf.bul("Maersk E级: 14,770 TEU, 397m x 56m — 可通过苏伊士但不过巴拿马")
    pdf.bul("Maersk Triple E: 18,300 TEU, 400m x 59m, 巡航35km/h — 降速37%节油+50%减排CO2")
    pdf.bul("MSC Oscar (2015): 19,224 TEU — 当时世界最大集装箱船")

    pdf.sub("4.4 海运费用结构")
    pdf.bul("基本运费(Taux de fret): 集装箱=按箱一口价；滚装=按米；件杂货=按吨或m3")
    pdf.bul("附加费: BAF(油价) + CAF(美元汇率, 海运以USD计价) + LSS(低硫 IMO2020) + OCR(中国出发) + ISPS(港口安保)")
    pdf.bul("运河通行费: 巴拿马/苏伊士运河")
    pdf.bul("滞期费(Surestaries): 超期占用集装箱罚款")
    pdf.bul("港口拥堵附加费: 目的港拥堵时额外收费")
    pdf.bul("THC/Liner Terms: 港口装卸费(收箱->靠船->装船->卸船->移箱->交运) — 独立于Incoterms")

    pdf.sub("4.5 空运 (Transport Aerien)")
    pdf.bul("ULD (Unit Loading Device): 标准化空运集装器，与飞机货舱匹配")
    pdf.bul("适用: 高价值+高时效货物")
    pdf.bul("主力: 大型货机(747F/777F等) + 客机腹舱(belly cargo)")

    # ===== PART 5: E-COMMERCE =====
    pdf.sec("电商物流 (Logistique E-commerce)", "五")

    pdf.sub("5.1 电商物流特点")
    pdf.bul("与传统零售最大区别: SKU数量极大(长尾效应)，订单多但每单数量少 -> 极高分散指数")
    pdf.bul("退货率远高于传统零售 -> 逆向物流(Retours)至关重要")
    pdf.bul("四大模块: 仓储(Stockage) + 快递(Messagerie) + 末端配送(Dernier km) + 信息流(Flux d'information)")
    pdf.bul("最后一公里: 最昂贵和最复杂的环节；解决方案: 自提点(Point relais)、快递柜(Consigne)、即时配送(Livraison express)")
    pdf.bul("城市物流挑战: 拥堵、环保限制(ZFE低排放区)、停车困难")

    # ===== PART 6: KEY FORMULAS =====
    pdf.add_page()
    pdf.sec("核心公式速查 (Formules Cles)", "六")

    pdf.sub("库存管理")
    pdf.fbox("经济订购量 QEC = RacineCarree(2 x D x Cc / Cp)", "D=年需求量, Cc=每次订购成本, Cp=单位年持有成本 (Wilson/Harris)")
    pdf.fbox("服务率 = 按时完整交付订单数 / 总订单数", "Taux de service")
    pdf.fbox("周转率 TR = 年出库量 / 平均库存 SM", "Taux de Rotation")
    pdf.fbox("覆盖率 TC = 平均库存 SM / 月均消费量 CMM", "Taux de Couverture")

    pdf.sub("仓库面积")
    pdf.fbox("标准货架: S = (A/2 + L + D) x (l + D) x N/d", "A=通道宽, L=长, l=宽, D=安全距0.1m, d=层数, N=托盘数")
    pdf.fbox("堆积式: S = T x (p x Se + Sa)", "T=跨数, p=深度, Se=单元面积, Sa=通道面积")
    pdf.fbox("堆积最优深度: p = RacineCarree((P-n) x Sa / (n x Se))", "P=总堆数, n=参考数")

    pdf.sub("叉车通道")
    pdf.fbox("四轮叉车: A = R + B + P_tablier + 0.2m", "")
    pdf.fbox("三轮叉车: A = L + B + 0.2m", "")
    pdf.fbox("双向通道: A = Largeur1 + Largeur2 + 2x50cm + 40cm", "")
    pdf.fbox("单向通道: A = Largeur_vehicule + 1m", "")

    pdf.sub("运输与运营")
    pdf.fbox("公路运输成本: PRF = a(EUR/km) x km + b(EUR)", "")
    pdf.fbox("充电功率: P(KW) = V(volts) x A(amperes) / 1000", "")
    pdf.fbox("计费单位: UO = 操作成本 / 活动量 (EUR/unite)", "")
    pdf.fbox("分散指数: n = 出库单位数 / 入库单位数", "n>10时自动化ROI高")

    # ===== PART 7: KEY NUMBERS =====
    pdf.sec("必记数字 (Chiffres Cles)", "七")
    pdf.tbl(
        ["指标", "数值"],
        [
            ["仓库装卸区占比", "~15%"],
            ["法定最少装卸口/单元", "6个"],
            ["存储最佳填充率", "85%"],
            ["存储面积占总面积", "~75%"],
            ["传统仓库存储密度", "1.2-1.5 托盘/m2"],
            ["高密度仓库存储密度", "<=3 托盘/m2"],
            ["HQE建筑成本溢价", "+5% a +15%"],
            ["行人通道最小宽度", "80cm"],
            ["法国叉车事故死亡/年", "15-20人"],
            ["叉车寿命/潜能", "60,000h / 15-18年"],
            ["购买成本占TCO比例", "~7%"],
            ["托盘Europe(1200x800x154mm)", "25kg / 1500kg+载重"],
            ["卡车<=4轴PTR max", "38T"],
            ["卡车>4轴PTR max", "44T"],
            ["卡车最大宽度", "2.55m (冷藏2.60m)"],
            ["卡车最大长度(单车)", "12m"],
            ["快递货物上限", "<3T / <48h"],
            ["Voice-picking设备成本", "2,500-3,000EUR/人"],
            ["WMS条码打印头寿命", ">80km"],
        ],
        [100, 65]
    )

    # ===== EXAM TIPS =====
    pdf.sec("考试提醒 (Conseils d'Examen)", "八")
    pdf.bul("熟记叉车类型与通道宽度对应: 1.40m / 1.80m / 2.60m / 3.60m")
    pdf.bul("卡车重量限制: 38T(<=4轴) / 44T(>4轴)，必须精确记忆")
    pdf.bul("Wilson公式(QEC)、服务率、周转率公式必背")
    pdf.bul("Incoterms 2020四大类(E/F/C/D)及风险/费用划分，记住'仅限海运'的4个术语(FAS/FOB/CFR/CIF)")
    pdf.bul("货架面积公式: 标准 vs 堆积式，理解并能应用")
    pdf.bul("仓库8大构成要素: 建筑+人员+设备+方法+IT+产品+作业+参与者")
    pdf.bul("每个关键概念尽量同时给出法语术语，展现双语能力")
    pdf.bul("NIMP15/CACES/VGP/ICPE/SEVESO等法规内容了解即可，核心概念和公式优先")
    pdf.bul("回答结构: 定义 -> 解释/公式 -> 应用 -> 结论")
    pdf.bul("关注不同部门(生产/销售/财务)在仓储/物流决策中的矛盾与平衡")

    # Output
    output_path = "D:/CC/cc/SC3_Prof2_考前复习资料.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
