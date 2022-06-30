import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# hide toolbar
plt.rcParams['toolbar'] = 'None'
# enbable Chinese
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

img = mpimg.imread('qrcode.png')
imgplot = plt.imshow(img)
plt.axis('off')
plt.title('请扫码')
plt.ioff()
plt.show()