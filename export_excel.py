from os import walk
from os.path import join
import xlsxwriter

def main(export_name, source, image_dimension):
    workbook = xlsxwriter.Workbook(export_name)

    image_width_height = image_dimension
    cell_width_height = 100.0
    scale = cell_width_height / image_width_height

    for (dirpath, dirnames, filenames) in walk(source):
        for subdirname in dirnames:
            worksheet = workbook.add_worksheet(name=subdirname)
            worksheet.set_column('A:A', 100)
            worksheet.set_column('B:B', 50)
            worksheet.set_column('C:C', 50)
            worksheet.set_column('D:D', 50)
            worksheet.write('A1', 'Image')
            worksheet.write('B1', 'Brand')
            worksheet.write('C1', 'Name')
            worksheet.write('D1', 'Price')
            
            for (subdirpath, subdirnames, subfilenames) in walk(join(source, subdirname)):
                for index, filename in enumerate(subfilenames):
                    arr_name = filename.split('.jpg')[0].split('_')
                    worksheet.set_row(index + 1, 100)

                    worksheet.insert_image(
                        'A{}'.format(index + 2), 
                        join(source, subdirname, filename), 
                        {'x_scale': scale, 'y_scale': scale}
                    )
                    worksheet.write('B{}'.format(index + 2), arr_name[0])
                    worksheet.write('C{}'.format(index + 2), arr_name[1])
                    worksheet.write('D{}'.format(index + 2), arr_name[2])
                    
    workbook.close()

if __name__ == '__main__':
    SOURCE_PATH = 'outputs/blanja/full'
    EXPORT_NAME = 'excel/blanja.xlsx'
    IMAGE_DIMENSION = 500.0
    main(EXPORT_NAME, SOURCE_PATH, IMAGE_DIMENSION)