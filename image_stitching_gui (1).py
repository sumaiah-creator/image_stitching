
import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (600, 400))  # Resize for consistency
        return img
    return None

def stitch_images(img1, img2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    if len(good_matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        result = cv2.warpPerspective(img2, H, (img1.shape[1] + img2.shape[1], img1.shape[0]))
        result[0:img1.shape[0], 0:img1.shape[1]] = img1
        return result
    else:
        print("Not enough matches found")
        return None

def run_gui():
    def load_first():
        nonlocal img1
        img1 = load_image()
        lbl1.config(text="Image 1 Loaded")

    def load_second():
        nonlocal img2
        img2 = load_image()
        lbl2.config(text="Image 2 Loaded")

    def stitch():
        result = stitch_images(img1, img2)
        if result is not None:
            cv2.imshow("Stitched Image", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    img1 = img2 = None

    root = Tk()
    root.title("Image Stitcher")

    Button(root, text="Load First Image", command=load_first).pack(pady=5)
    lbl1 = Label(root, text="No Image 1")
    lbl1.pack()

    Button(root, text="Load Second Image", command=load_second).pack(pady=5)
    lbl2 = Label(root, text="No Image 2")
    lbl2.pack()

    Button(root, text="Stitch Images", command=stitch).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
