import datetime
import os
from PIL import Image
import fitz  # fitz就是pip install PyMuPDF
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file_name", default="租房合同.pdf")


"""
    pdf转图片
"""
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    create_directory(".\\output_img")
    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.save(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)



"""
    合并图片成pdf
"""
def merge_img_to_pdf(path: str, name: str):
    create_directory(".\\output_pdf")
    img_open_list = []                                 # 创建打开后的图片列表
    for root, dirs, files in os.walk(path):
        for i in files:
            file = os.path.join(root, i)               # 遍历所有图片，带绝对路径
            img_open = Image.open(file)                # 打开所有图片
            if img_open.mode != 'RGB':
                img_open = img_open.convert('RGB')     # 转换图像模式
            img_open_list.append(img_open)             # 把打开的图片放入列表
    # pdf_name = name + '.pdf'                           # pdf文件名
    pdf_name = name
    img_1 = img_open_list[0]                           # 打开的第一张图片
    # 把img1保存为PDF文件,将另外的图片添加进来，列表需删除第一张图片，不然会重复
    img_open_list = img_open_list[1:]
    img_1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=img_open_list)
    print('转换成功！pdf文件在当前程序目录下！')
    clear_imgs(path)


"""
    批量删除图片文件
"""
def clear_imgs(path: str):
    for root, dirs, files in os.walk(path):
        for i in files:
            file = os.path.join(root, i)
            os.remove(file)
    return True


"""
    验证文件夹是否存在，不存在则创建
"""
def create_directory(path: str):
    if os.path.exists(path):
        return False
    os.mkdir(path)
    return True


if __name__ == "__main__":
    # 1、PDF地址
    args = parser.parse_args()
    pdf_name = args.file_name
    pdfPath = f'.\\input_pdf\\{pdf_name}'
    # 2、需要储存图片的目录
    imagePath = './output_img'
    pyMuPDF_fitz(pdfPath, imagePath)
    output_pdf_path = f'.\\output_pdf\\{pdf_name}'
    merge_img_to_pdf(imagePath, output_pdf_path)


