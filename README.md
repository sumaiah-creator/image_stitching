📄 Image Stitcher - Python Script 
Overview
This script provides a graphical user interface (GUI) using Tkinter to load two images and stitch them together using feature matching and homography with OpenCV. It uses the SIFT (Scale-Invariant Feature Transform) algorithm to detect keypoints and descriptors, and FLANN (Fast Library for Approximate Nearest Neighbors) for matching.

🧾 Requirements
Before running the script, ensure the following Python libraries are installed:
pip install opencv-python opencv-contrib-python numpy
tkinter is included by default in standard Python installations.

🛠️ How It Works
1. load_image()
Opens a file dialog to choose an image.
Reads and resizes the image to (600x400) pixels for consistency.
Returns the image as a NumPy array.

2. stitch_images(img1, img2)
Uses SIFT to detect keypoints and compute descriptors in both images.
Uses FLANN matcher to find the best keypoint matches.
Applies Lowe's ratio test to filter good matches.
If at least 10 good matches are found:
Computes a homography matrix using RANSAC.
Warps img2 onto the perspective of img1 and blends them.
Returns the stitched image if successful, else prints an error.

3. run_gui()
Creates the GUI window with buttons to:
Load the first image.
Load the second image.
Stitch both images.
Displays the stitched result in a new OpenCV window.

🖱️ Usage
Run the script:
python image_stitcher.py
Use the GUI to:
Load Image 1.
Load Image 2.
Click "Stitch Images" to view the result.

🧩 Notes
Images should have overlapping areas for stitching to succeed.
SIFT is part of opencv-contrib-python; ensure it's installed.
You can adjust the Lowe’s ratio (0.7) or minimum match count (10) for performance tuning.

📸 Example
python
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
result = stitch_images(img1, img2)
cv2.imshow("Stitched", result)

📌 Limitations
Works best with well-lit, planar scenes with good feature overlap.
May not handle parallax or wide-angle distortions well.
