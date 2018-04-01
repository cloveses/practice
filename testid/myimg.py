from PIL import Image,ImageDraw,ImageFont

im = Image.open('zc.jpg').convert('RGBA')

txtim=Image.new('RGBA', im.size, (0,0,0,0))

fnt = ImageFont.truetype('simsun.ttc',56)
mydraw = ImageDraw.Draw(txtim)
mydraw.text((60,60),'中化',font=fnt,fill=(220,20,20,60))
out = Image.alpha_composite(im,txtim)
out.show()
