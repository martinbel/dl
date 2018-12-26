import os
import glob
import pandas as pd
import re
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    keep_classes = ['pistol']
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            class_name = member[0].text
            if class_name in keep_classes:
                value = (re.sub(".xml", ".jpg", xml_file),#root.find('filename').text ,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         class_name,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    output_dir = '/mnt/dl/data/guns/'
    for directory in ['train', 'test']:
        xml_df = xml_to_csv(os.path.join(output_dir, directory))
        xml_df.to_csv(os.path.join(output_dir, directory + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

if __name__ == '__main__':
    main()
