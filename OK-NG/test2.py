def convert_image_paths_to_dict(image_paths):
    # Create a dictionary to store the unique image names and their counts
    image_count = {}
    for path in image_paths:
        image_name = path.split('/')[-1]
        if image_name in image_count:
            image_count[image_name] += 1
        else:
            image_count[image_name] = 1

    # Create the resulting list of dictionaries
    result = []
    for image_name, count in image_count.items():
        for i in range(count):
            detect_result = "NG" if image_name == "frame_20240630-141050.jpg" else "OK"
            result.append({"name": f"D:/myData/{image_name[:-4]}_{i + 1}.jpg", "detect_result": detect_result})

    return result


# Example usage:
image_paths = ['saved_frames/frame_20240630-141050.jpg', 'saved_frames/frame_20240630-141050.jpg',
               'saved_frames/frame_20240630-141050.jpg',
               'saved_frames/frame_20240630-141050.jpg', 'saved_frames/frame_20240630-141050.jpg',
               'saved_frames/frame_20240630-141051.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg', 'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg',
               'saved_frames/frame_20240630-141052.jpg']

converted_images = convert_image_paths_to_dict(image_paths)
for image in converted_images:
    print(image)
