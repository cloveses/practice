import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm, mm
from reportlab.graphics.barcode import code39, code128, code93

# import getdata

## 尺寸cm
ID_SIZE = (20,16)
## 水印文本
WATERMARK_TXT = "泗县教体局"
## cm
POSITIONS = ((5,12),(5,9),(5,6),(5,3),(12,8))
## 以上为以下五项的输出位置
STUDS = [("李文娟",'男','01中学','201838574737','tt.png'),
        ("张文地",'男','01中学','201838574736','tt.png'),
        ("小文地",'男','01中学','201838574733','tt.png')]
IMG_PATH = ".\\idsd"

BAR_METHODS = {'code39':code39.Extended39, 
            'code128':code128.Code128,
            'code93':code93.Standard93}

BAR_POS = (5,10)


def confirm_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def set_font(canv,size,font_name='msyh',font_file='msyh.ttf'):
    pdfmetrics.registerFont(TTFont(font_name,font_file))
    canv.setFont(font_name,size)

def draw_barcode(canv,idcode,codetype='code128'):
    ## 绘制条形码
    ## codetype have:code39,code93,code128
    barcd = BAR_METHODS[codetype](idcode)
    barcd.drawOn(canv,BAR_POS[0]*cm,BAR_POS[1]*cm)
    # barcode39 = code39.Extended39('34322545666')
    # barcode39.drawOn(c,20,20)
    # barcode93 = code93.Standard93('34322545666')
    # barcode93.drawOn(c,20,60)
    # barcode128 = code128.Code128('34322545666')
    # barcode128.drawOn(c,20,100)

def draw_page(canv,stud):
    set_font(canv,16)
    ## 背景图
    # canv.drawImage('bg.jpg',POSITIONS[-1][0]*cm,POSITIONS[-1][1]*cm)
    for index,info in enumerate(stud[:4]):
        canv.drawString(POSITIONS[index][0]*cm,POSITIONS[index][1]*cm,info)
    canv.drawImage(stud[-1],POSITIONS[-1][0]*cm,POSITIONS[-1][1]*cm)
    canv.setFillColorRGB(180,180,180,alpha=0.3)
    canv.drawString(POSITIONS[-1][0]*cm+cm,POSITIONS[-1][1]*cm+0.5*cm,WATERMARK_TXT)
    canv.showPage()

def gen_pdf(dir_name,sch_name,studs):
    confirm_path(dir_name)
    path = os.path.join(dir_name,sch_name + '.pdf')
    canv = canvas.Canvas(path,pagesize=(ID_SIZE[0]*cm,ID_SIZE[1]*cm))
    for stud in studs:
        draw_page(canv,stud)
    canv.save()

# def gen_all_pdfs(dir_name):
#     schs = getdata.get_schs()
#     for sch in schs:
#         studs = getdata.get_studs(sch)
#         gen_pdf(dir_name,sch,studs)

if __name__ == '__main__':
    gen_pdf(IMG_PATH,'01中学',STUDS)