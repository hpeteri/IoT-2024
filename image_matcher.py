import cv2
import os
from skimage.metrics import structural_similarity as ssim

def load_and_preprocess_image(image_path):
    """Load an image and convert it to grayscale."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path '{image_path}' could not be loaded.")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def compare_images(image1, image2):
    """Compare two grayscale images and return their similarity percentage."""
    # Ensure both images are the same size for comparison
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    # Calculate the Structural Similarity Index (SSIM)
    score, _ = ssim(image1, image2, full=True)
    return score * 100  # Convert to percentage

def match_image_to_targets(input_image_path, target_folder_path):
    """
    Match an input image to all target images in a folder.
    Returns Structural Similarity index as percentage
    for each target image.
    """
    try:
        # Load and preprocess the input image
        input_image = load_and_preprocess_image(input_image_path)

        # Prepare to store results
        similarity_scores = {}

        # Iterate over all target images in the folder
        for target_image_name in os.listdir(target_folder_path):
            target_image_path = os.path.join(target_folder_path, target_image_name)
            if not os.path.isfile(target_image_path):
                continue

            # Load and preprocess the target image
            target_image = load_and_preprocess_image(target_image_path)

            # Compare the input image with the target image
            similarity = compare_images(input_image, target_image)
            similarity_scores[target_image_name] = similarity

        return similarity_scores

    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    # Example usage
    input_image_path = "input.jpg"  # Replace with your input image path
    target_folder_path = "targets"  # Replace with your target images folder path

    results = match_image_to_targets(input_image_path, target_folder_path)

    if results:
        print("Similarity scores:")
        for target, score in results.items():
            print(f"{target}: {score:.2f}%")
    else:
        print("No matches found or an error occurred.")
