import math
import datetime
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,Table,TableStyle,PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# 生成考试异常登记表

# 表头
TAB_HEAD = [['报名号','准考证号','检录处','第一项','','第二项','','800/1000米','序号','备注'],
    ['','','','立定跳远','跳绳','实心球','坐位体前屈','','','']]

# 合并单元格命令
TAB_STYLE = [('SPAN',(0,0),(0,1)),
    ('SPAN',(1,0),(1,1)),
    ('SPAN',(2,0),(2,1)),
    ('SPAN',(3,0),(4,0)),
    ('SPAN',(5,0),(6,0)),
    ('SPAN',(7,0),(7,1)),
    ('SPAN',(8,0),(8,1)),
    ('SPAN',(9,0),(9,1))
    ]
# 页脚文本
FOOT_TEXT = "检录员签名:_________ &nbsp;&nbsp;&nbsp;裁判员签名 跳绳:___________&nbsp;&nbsp;&nbsp;&nbsp;跳远:___________ \
    &nbsp;&nbsp;&nbsp;&nbsp;实心球:___________&nbsp;&nbsp;&nbsp;&nbsp;体前屈:___________&nbsp;&nbsp;&nbsp;&nbsp;径部:______"

# 每页人数
PAGE_NUM = 24
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))

# 换页
PAGE_STOP = PageBreak()

# 获取标题与普通段落样式
stylesheet=getSampleStyleSheet()
stylesheet['Title'].fontName = 'msyh'
stylesheet['Normal'].fontName = 'msyh'
stylesheet['Normal'].fontSize = 12
# 表格样式命令
TAB_STY_LST = [
    # ('TEXTCOLOR',(0,0),(1,-1),colors.red),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('INNERGRID', (0,0),(-1,-1), 0.25, colors.black),
    # ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ('GRID',(0,0), (-1,-1),1,colors.black),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONT', (0,0), (-1,-1), 'msyh'),
    ('BOTTOMPADDING',(0,0),(-1,-1),2),
    ('TOPPADDING',(0,0),(-1,-1),2)]
TAB_STY_LST.extend(TAB_STYLE)
# 生成表格样式
TAB_STY = TableStyle(TAB_STY_LST)
# 生成页眉和页脚段落
TITLE_PARA = Paragraph(("&nbsp;" * 2).join("2018年泗县中考体育考试异常情况登记表"),stylesheet['Title'])
FOOT_PARA = Paragraph(FOOT_TEXT,stylesheet['Normal'])


# 生成每页元素
def gen_page_elmnts(pdatas,sch = '泗县一中',group_name = '女',test_date = '4月21日上午'):
    page_elmnts = []
    page_elmnts.append(TITLE_PARA)
    title_text_sch = "考点：{}".format(sch)
    title_text_group = "组别: {}子组".format(group_name)
    title_text_date = ''.join((str(datetime.datetime.today().year),'年',test_date))
    sep_sign = "&nbsp;" * 50
    title_text = sep_sign.join((title_text_sch,title_text_group,title_text_date))
    page_elmnts.append(Paragraph(title_text,stylesheet['Normal']))
    page_elmnts.append(Spacer(1,15))
    if len(pdatas) < PAGE_NUM + 2:
        pdatas.extend([''] * 10 for i in range(PAGE_NUM + 2 - len(pdatas)))
    table = Table(pdatas,colWidths=78)
    # 指定序号列（第八列）宽
    table._argW[8] = 36
    # 设置样式
    table.setStyle(TAB_STY)
    page_elmnts.append(table)
    page_elmnts.append(Spacer(1,16))
    page_elmnts.append(FOOT_PARA)
    return page_elmnts

# 生成所有页元素
def gen_elements(datas,sch = '泗县一中',group_name = '女',test_date = '4月21日上午'):
    elements = []
    for i in range(math.ceil(len(datas) / PAGE_NUM)):
        start = i * 24
        end = (i + 1) * 24
        pdatas = []
        pdatas.extend(TAB_HEAD)
        for index,data in enumerate(datas[start:end]):
            row = [''] * 10
            row[0] = ''.join(('243547788',data[0]))
            row[1] = ''.join(('463432433',data[1]))
            # 生成序号
            row[8] = index + 1
            pdatas.append(row)
        page_elmnts = gen_page_elmnts(pdatas,sch = '泗县一中',group_name = '女',test_date = '4月21日上午')
        elements.extend(page_elmnts)
        elements.append(PAGE_STOP)
    return elements


def gen_pdf(elements,file_name='test.pdf'):
    doc = SimpleDocTemplate(file_name,pagesize=(A4[1],A4[0]),topMargin = 15,bottomMargin = 15)
    doc.build(elements)

# 以半天为单位生成登记表
def get_half_pdf(file_name,datas,sch = '泗县一中',group_name = '女',test_date = '4月21日上午')
    elements = gen_elements(datas,sch = '泗县一中',group_name = '女',test_date = '4月21日上午')
    gen_pdf(elements,file_name='test.pdf')

# 生成半天同一性别登记表
def get_pdf_type_a():
    from .booktab_sets import arrange_datas_type_a
    from .phdl import StudPh
    for arrange_datas in arrange_datas_type_a:
        file_name = ''.join(arrange_datas[:2])
        file_name = ''.join((file_name,'.pdf'))
        studs = StudPh.select(lambda s:s.sex == arrange_datas[-1] and s.sch == arrange_datas[2]).order_by(StudPh.phid)[:]
        get_half_pdf(file_name,studs,arrange_datas[0],arrange_datas[-1],arrange_datas[1])

# 生成半天不同性别登记表
def get_pdf_type_b():
    from .booktab_sets import arrange_datas_type_b
    from .phdl import StudPh
    for arrange_datas in arrange_datas_type_b:
        file_name = ''.join(arrange_datas[:2])
        sexes = ('女','男')
        for sex in sexes:
            studs = StudPh.select(lambda s:s.sex == sex and s.sch in arrange_datas[-1]).order_by(StudPh.phid)[:]
            cfile_name = ''.join((file_name,sex,'.pdf'))
            get_half_pdf(cfile_name,studs,arrange_datas[0],sex,arrange_datas[1])


if __name__ == '__main__':
    DATAS = [['0','1'] for i in range(50)]
    elements = gen_elements(DATAS)
    gen_pdf(elements)


