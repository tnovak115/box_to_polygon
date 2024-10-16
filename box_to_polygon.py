import xml.etree.ElementTree as ET

def find_boxes_in_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        images = root.findall('.//image')
        for image in images:
            boxes = image.findall('box[@label="mask_ped"]')
            for box in boxes:
                xtl = int(box.get('xtl'))
                ytl = int(box.get('ytl'))
                xbr = int(box.get('xbr'))
                ybr = int(box.get('ybr'))
                y_diff = ybr-ytl
                mid = int((xbr+xtl)/2)
                onethird = ybr + int((1/3)*y_diff)
                twothird = ybr + int((1/3)*y_diff)
                points = f"{mid},{ytl};{xtl},{onethird};{xbr},{onethird};{xtl},{twothird};{xbr},{twothird};{mid},{ybr};"
                polygon = ET.Element('polygon', {
                    'label': 'mask',
                    'source': box.get('source', ''),
                    'occluded': box.get('occluded', '0'),
                    'points': points,
                    'z_order': box.get('z_order', '0')
                    })

                image.append(polygon)
        for image in images:
            for box in image.findall('box'):
                image.remove(box)

        tree.write(file_path)

        for image in images:
            image.attrib.pop('box', None)

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

xml_file_path = 'cam3_annotations.xml'
find_boxes_in_xml(xml_file_path)