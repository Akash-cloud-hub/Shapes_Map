import cv2
import utility
import numpy as np

drawing = False
points = []
mask = None
img1 = cv2.imread('monkey-nft.png')
dots = None


def main():
    global mask
    clone = img1.copy()

    mask = np.zeros_like(img1)  # Initialize the mask here
    dots = np.zeros_like(img1)

    # (x1,y1,x2,y2) = cv2.selectROI("img1",img1,fromCenter= False,showCrosshair=True)
    #
    # selected_area = clone[y1:y1+y2,x1:x1+x2]
    # utility.show_img("selected_area",selected_area)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_callback)

    while True:
        combined_img = cv2.addWeighted(img1, 0.7, mask, 0.3, 0)
        combined_img = cv2.addWeighted(combined_img,0.7,dots,0.3 , 0) # continuosly displays orignal image , mask and dots.
        cv2.imshow("image", combined_img)

        key = cv2.waitKey(1)
        if key == ord('x'):
            points = []
            shapes = []
            mask = np.zeros_like(img1)  # Clear the mask
            dots = np.zeros_like(img1)
        elif key == 27 or key == ord("q"):  # Escape key to exit
            break
        elif key == ord("c"):
            if len(points) == 2:
                radius = int(cv2.norm(np.array(points[1]) - np.array(points[0])))
                cv2.circle(mask , points[0] , radius , (255,255,255) , -1)

    selected_area = cv2.bitwise_and(img1, mask)
    utility.show_img("image", selected_area)

    cv2.destroyAllWindows()


def draw_freehand(event, x, y, flags, param):
    global drawing, points, mask

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]  # Start collecting points
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))  # Add points during drawing
            cv2.polylines(mask, [np.array(points)], isClosed=False, color=(255,255,255), thickness=2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append((x, y))  # Finalize the drawing
        cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))  # Fill the polygon

def mouse_callback(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONUP:
        points.append([x,y])
        cv2.circle(dots , (x,y) , 5 , (0,0,255) , thickness=-1 )


if __name__ == '__main__':
    main()
