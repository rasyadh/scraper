import os
from os import walk
from os.path import join
import glob
import shutil
import xlsxwriter

def merge_brand(export_name, source):
    for (dirpath, dirnames, filenames) in walk(source):
        for dirname in dirnames:
            dest_output = export_name + dirname.lower()
            if not os.path.exists(dest_output):
                os.makedirs(dest_output)
            
            for image in glob.iglob(join(source, dirname, "*.jpg")):
                shutil.copy(image, dest_output)

def main_without_image(export_name, source):
    workbook = xlsxwriter.Workbook(export_name)

    for (dirpath, dirnames, filenames) in walk(source):
        for subdirname in dirnames:
            if not subdirname.startswith("."):
                worksheet = workbook.add_worksheet(name=subdirname)
                worksheet.set_column('A:A', 50)
                worksheet.set_column('B:B', 100)
                worksheet.set_column('C:C', 30)
                worksheet.write('A1', 'Brand')
                worksheet.write('B1', 'Name')
                worksheet.write('C1', 'Price')
                
                for (subdirpath, subdirnames, subfilenames) in walk(join(source, subdirname)):
                    for index, filename in enumerate(subfilenames):
                        if not filename.startswith("."):
                            arr_name = filename.split('.jpg')[0].split('_')

                            worksheet.write('A{}'.format(index + 2), arr_name[0])
                            worksheet.write('B{}'.format(index + 2), arr_name[1])
                            worksheet.write('C{}'.format(index + 2), arr_name[2])
                    
    workbook.close()

if __name__ == '__main__':
    SOURCE_PATH = 'outputs/indomaret/full'
    EXPORT_NAME = 'merge/'
    # merge_brand(EXPORT_NAME, SOURCE_PATH)

    SOURCE = 'merge'
    EXPORT = 'excel/all.xlsx'
    main_without_image(EXPORT, SOURCE)