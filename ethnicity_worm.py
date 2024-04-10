import sys
import csv
import SimpleITK as sitk
import pathlib

result = {}
p = pathlib.Path('X:')
with open('temp.csv', 'w') as sys.stdout:
    for file in p.glob('**/0000.dcm'):

        try:
            file_reader = sitk.ImageFileReader()
            file_reader.SetImageIO('GDCMImageIO')
            file_reader.SetFileName(str(file))
            file_reader.LoadPrivateTagsOn()
            file_reader.ReadImageInformation()
            info = {k: file_reader.GetMetaData(k) for k in file_reader.GetMetaDataKeys()}
        except:
            continue

        if '0010|0010' in info:
            
            name = info['0010|0010'].strip()
            race = ''
            if '0010|2160' in info:
                race = info['0010|2160'].strip()

            print(f'{name},{race},{file}')

            if name and race:
                if name in result:
                    if race != result[name]:
                        print(f"* check {name}")
                elif name in names:
                    result[name] = race


with open('result.csv', 'w', newline='') as f:
    csv.writer(f).writerows(result.items())

