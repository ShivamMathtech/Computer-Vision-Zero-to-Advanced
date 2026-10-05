"""Desktop paint/trackbar and webcam demonstrations; not used by headless notebooks."""

import argparse

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["paint", "webcam"])
    parser.add_argument("--camera", type=int, default=0)
    args = parser.parse_args()
    capture = None
    try:
        cv2.namedWindow("CV Zero")
        if args.mode == "paint":
            canvas = np.full((480, 640, 3), 255, np.uint8)
            cv2.createTrackbar("Blue", "CV Zero", 0, 255, lambda _: None)
            cv2.createTrackbar("Green", "CV Zero", 80, 255, lambda _: None)
            cv2.createTrackbar("Red", "CV Zero", 240, 255, lambda _: None)

            def draw(event, x, y, flags, _):
                if event == cv2.EVENT_LBUTTONDOWN or (
                    event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON
                ):
                    color = tuple(
                        cv2.getTrackbarPos(c, "CV Zero") for c in ("Blue", "Green", "Red")
                    )
                    cv2.circle(canvas, (x, y), 5, color, -1)

            cv2.setMouseCallback("CV Zero", draw)
            print("Drag to paint. C clears. S saves paint.png. Escape quits.")
        else:
            capture = cv2.VideoCapture(args.camera)
            if not capture.isOpened():
                raise RuntimeError(
                    "Webcam unavailable. Check permissions/device index or use the generated-video notebooks."
                )
        while True:
            if capture:
                ok, canvas = capture.read()
                if not ok:
                    raise RuntimeError("Camera frame read failed.")
            cv2.imshow("CV Zero", canvas)
            key = cv2.waitKey(16) & 255
            if key == 27:
                break
            if key == ord("c") and args.mode == "paint":
                canvas[:] = 255
            if key == ord("s"):
                if not cv2.imwrite("paint.png", canvas):
                    raise RuntimeError("Could not write paint.png.")
                print("Saved paint.png")
    except cv2.error as exc:
        parser.exit(
            2,
            "OpenCV GUI unavailable. Use a desktop environment and replace opencv-python-headless with opencv-python in a separate environment.\n"
            + str(exc)
            + "\n",
        )
    except RuntimeError as exc:
        parser.exit(2, str(exc) + "\n")
    finally:
        if capture is not None:
            capture.release()
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass


if __name__ == "__main__":
    main()
