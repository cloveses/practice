import os
import img2pdf
from PIL import Image,ImageDraw,ImageFont

ID_SIZE = (400,200)
## 水印文本
WATERMARK_TXT = "泗县教体局"
POSITIONS = ((50,30),(50,60),(50,90),(50,120),(240,20))
## 以上为以下五项的输出位置
STUDS = [("李文娟",'男','01中学','201838574737','tt.png'),
        ("李文地",'男','01中学','201838574731','tt.png'),
        ("王文地",'男','01中学','201838574730','tt.png'),
        ("张文地",'男','02中学','201838574736','tt.png'),
        ("小文地",'男','02中学','201838574733','tt.png')]
IMG_PATH = ".\\ids"

def confirm_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def add_watermake(img):
    '''
    为传入的图片添加水印
    '''
    txtim=Image.new('RGBA',ID_SIZE, (0,0,0,0))
    fnt = ImageFont.truetype('simsun.ttc',18)
    mydraw = ImageDraw.Draw(txtim)
    mydraw.text((198,160),WATERMARK_TXT,font=fnt,fill=(180,180,180,90))
    out = Image.alpha_composite(img,txtim)
    return out

def gen_img(datalst):
    for stud in datalst:
        ## 添加文本信息
        main_img = Image.new('RGBA', ID_SIZE, (255,255,255,0))
        fnt = ImageFont.truetype('simsun.ttc',16)
        mydraw = ImageDraw.Draw(main_img)
        for i,stud_str in enumerate(stud[:len(stud)]):
            mydraw.text(POSITIONS[i],stud_str,font=fnt,fill='black')
        ## 添加照片
        pho = Image.open(stud[-1]).convert('RGBA')
        pho = pho.crop((0,0,pho.size[0],pho.size[1]))
        x = POSITIONS[-1][0]
        y = POSITIONS[-1][1]
        box = (x,y,x+pho.size[0],y+pho.size[1])
        main_img.paste(pho,box)
        ## 调用添加水印函数
        main_img = add_watermake(main_img)
        path_name = os.path.join(IMG_PATH,stud[2])
        confirm_path(path_name)
        file_name = os.path.join(path_name,stud[3]+'.jpg')
        main_img.convert('RGB').save(file_name)

def get_pdf(dir_name):
    sch_dirs = [directory for directory in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,directory))]
    for sch_dir in sch_dirs:
        sub_dir = os.path.join(dir_name,sch_dir)
        imgs = [os.path.join(sub_dir,imgpath) for imgpath in os.listdir(sub_dir)]
        pdf_path = os.path.join(dir_name,sch_dir+'.pdf')
        with open(pdf_path,'wb') as f:
            f.write(img2pdf.convert(imgs))

if __name__ == '__main__':
    gen_img(STUDS)
    get_pdf(IMG_PATH)



    # txtim=Image.new('RGBA', im.size, (0,0,0,0))
    # fnt = ImageFont.truetype('simsun.ttc',56)
    # mydraw = ImageDraw.Draw(txtim)
    # mydraw.text((60,60),'中化',font=fnt,fill=(220,20,20,60))
    # out = Image.alpha_composite(im,txtim)
