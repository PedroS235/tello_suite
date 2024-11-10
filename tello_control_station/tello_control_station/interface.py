import pygame
import sys
from cv_bridge import CvBridge
import cv2
from tello_control_station.video_container import VideoContainer

matching_keys = {
    "j": pygame.K_j,
    "k": pygame.K_k,
    "t": pygame.K_t,
    "l": pygame.K_l,
    "q": pygame.K_q,
    "e": pygame.K_e,
    "h": pygame.K_h,
    "f": pygame.K_f,
    "m": pygame.K_m,
    "w": pygame.K_w,
    "s": pygame.K_s,
    "a": pygame.K_a,
    "d": pygame.K_d,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
}


class Interface:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joysticks = []
        self.is_clicked = False

        self.display = pygame.display.set_mode((960, 720))
        self.display.fill((200, 230, 240))
        pygame.display.flip()

        self.cv_bridge = CvBridge()
        self.video_container = VideoContainer(self.display)

    def tick(self):
        self.video_container.update_image_frame()

        mouse_clicked = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.JOYDEVICEADDED:
                print("joystick added")
                self.joysticks.append(pygame.joystick.Joystick(0))
                continue

            elif event.type == pygame.JOYDEVICEREMOVED:
                print("joystick removed")
                self.joysticks.pop(0)
                continue

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        self.is_clicked = (
            True if mouse_clicked and not self.is_clicked else False
        )

    def get_key_pressed(self):
        return pygame.key.get_pressed()

    def get_joysticks(self):
        return self.joysticks

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def update_display_mode(self, mode):
        self.video_container.display_mode = mode

    def update_battery(self, battery_level):
        self.video_container.update_battery(battery_level)

    def update_bg_image(self, image):
        image = self.cv_bridge.imgmsg_to_cv2(image, "rgb8")

        opencv_image = image[:, :, ::-1]
        shape = image.shape[1::-1]
        self.video_container.update_bg_image(
            pygame.image.frombuffer(opencv_image.tostring(), shape, "BGR")
        )

    def update_boxes(self, info, is_selected_face, nose=None):
        if is_selected_face:
            self.video_container.update_selected_face_box(
                pygame.Rect(
                    info.face.x, info.face.y, info.face.w, info.face.h
                ),
                nose,
            )
        else:
            self.video_container.update_face_boxes(
                [
                    pygame.Rect(el.face.x, el.face.y, el.face.w, el.face.h)
                    for el in info
                ]
            )

    def update_skeleton_layer(self, layer):
        image = self.cv_bridge.imgmsg_to_cv2(layer)
        self.video_container.update_skeleton_layer(
            pygame.image.frombuffer(
                image.tostring(), image.shape[1::-1], "RGB"
            )
        )