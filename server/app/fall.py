import cv2
import time
from fastapi import APIRouter, UploadFile
from fastapi.param_functions import File

video_source = 0
cap = cv2.VideoCapture(video_source)

# OpenPose 설정
proto_file = "C:/Users/user/PycharmProjects/AI/model/openpose_pose_coco.proto"
model_file = "C:/Users/user/PycharmProjects/AI/model/pose_iter_440000.caffemodel"

net = cv2.dnn.readNetFromCaffe(proto_file, model_file)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# 추락 감지 기준
threshold = 0.3

BODY_PARTS_COCO = {0: "Nose", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                   5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "RHip", 9: "RKnee",
                   10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "REye",
                   15: "LEye", 16: "REar", 17: "LEar", 18: "Background"}

fall_router = APIRouter()


def fall_detection(points):
    # 배와 골반 사이의 높이를 기준으로 추락 감지
    fall_threshold = 0.7

    if None in (points[1], points[8], points[11]):
        return False

    hip_height_diff = abs(points[8][1] - points[11][1])
    neck_to_hip_height = abs(points[1][1] - (points[8][1] + points[11][1]) / 2)
    normalized_height = hip_height_diff / neck_to_hip_height

    return normalized_height > fall_threshold


# # 원 색상, 크기 및 두께 설정
# point_color = (0, 255, 0)  # Green color
# point_radius = 3
# point_thickness = -1  # A filled circle
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     h, w = frame.shape[:2]
#     inp = cv2.dnn.blobFromImage(frame, 1.0 / 255, (w, h), (0, 0, 0), swapRB=False, crop=False)
#     net.setInput(inp)
#     output = net.forward()
#
#     H = output.shape[2]
#     W = output.shape[3]
#     points = []
#
#     for i in range(output.shape[1]):
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(output[0, i, :, :])
#         if max_val > threshold:
#             x = w * max_loc[0] / W
#             y = h * max_loc[1] / H
#             points.append((int(x), int(y)))
#         else:
#             points.append(None)
#
#     print(points)
#
#     if points[8] is not None and points[11] is not None:
#         if fall_detection(points):
#             print(time.strftime('%H:%M:%S'))
#
#     # 각 점에 대한 원 그리기
#     for point in points:
#         if point is not None:
#             cv2.circle(frame, point, point_radius, point_color, point_thickness)
#
#     cv2.imshow("Human Fall Detection", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
# cap.release()
# cv2.destroyAllWindows()


@fall_router.post("/fall")
def predict_image(image: UploadFile = File(...)):
    pass
