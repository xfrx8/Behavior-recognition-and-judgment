import json


class JSONGenerator:
    def __init__(self, barcode, total_result, images):
        self.barcode = barcode
        self.total_result = total_result
        self.images = images

    def update_barcode(self, barcode):
        self.barcode = barcode

    def update_total_result(self, total_result):
        self.total_result = total_result

    def update_images(self, images):
        self.images = images

    def generate_json(self):
        data = {
            "data": {
                "barcode": self.barcode,
                "total_result": self.total_result,
                "images": self.images
            }
        }
        return json.dumps(data, indent=4, ensure_ascii=False)

    def convert_image_paths_to_dict(self, image_paths):
        image_count = {}

        for path in image_paths:
            image_name = path.split('/')[-1].split('\\')[-1] 
            if image_name in image_count:
                image_count[image_name] += 1
            else:
                image_count[image_name] = 1

        # Create the resulting list of dictionaries
        result = []
        for image_name, count in image_count.items():
            for i in range(count):
                # Use total_result to determine detect_result
                detect_result = self.total_result
                result.append({"name": f"E:/saved_frames/{image_name[:-4]}.jpg", "detect_result": detect_result})

        return result
