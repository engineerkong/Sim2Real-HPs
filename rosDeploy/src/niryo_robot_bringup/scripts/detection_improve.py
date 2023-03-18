from niryo_robot_vision.markers_detection import *
from niryo_robot_vision.ObjectDetector import *

def find_markers_from_img_thresh_improve(img_thresh, max_dist_between_centers=3, min_radius_circle=4,
                                 max_radius_circle=35, min_radius_marker=7):
    contours = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    list_potential_markers = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if not min_radius_circle < radius < max_radius_circle:
            continue
        center = (int(round(x)), int(round(y)))
        radius = int(radius)
        list_potential_markers.append(PotentialMarker(center, radius, cnt))

    list_potential_markers = sorted(list_potential_markers, key=lambda m: m.x)
    list_good_candidates = []

    for i, potential_marker in enumerate(list_potential_markers):
        if potential_marker.is_merged:
            continue
        marker1 = Marker(potential_marker)
        center_marker = marker1.get_center()

        for potential_marker2 in list_potential_markers[i + 1:]:
            if potential_marker.is_merged:
                continue
            center_potential = potential_marker2.get_center()
            if center_potential[0] - center_marker[0] > max_dist_between_centers:
                break
            dist = euclidean_dist_2_pts(center_marker, center_potential)
            if dist <= max_dist_between_centers:
                marker1.add_circle(potential_marker2)
                center_marker = marker1.get_center()
        if marker1.nb_circles() >= 2 and marker1.radius >= (min_radius_marker-1):
            list_good_candidates.append(marker1)
            marker1.get_id_from_slice(img_thresh)

    return list_good_candidates

def image_preprocess_with_hsv_improve(self, im_work, use_s_prime=False):
        """

        :param im_work:
        :param use_s_prime: Bool -> True if you want to use S channel as S' = S x V else classic
        :return:
        """
        self.actualize_img(im_work)
        list_min_hsv, list_max_hsv, reverse_hue = self.get_hsv_parameters()
        list_min_hsv = [0, 43, 46]
        list_max_hsv = [179, 255, 255]
        reverse_hue = False
        im_thresh = threshold_hsv(im_work, list_min_hsv, list_max_hsv, reverse_hue=reverse_hue, use_s_prime=use_s_prime)
        cv2.imwrite('/home/lingxiao/master/catkin_ws_niryo_ned/test4.jpg', im_thresh)
        self.actualize_im_thresh(im_morph)
        return im_morph

# TODO
def detection_improve():
    # improve the detection to reduce the Markers not Found and Object not Found
    find_markers_from_img_thresh = find_markers_from_img_thresh_improve
    ObjectDetector.image_preprocess_with_hsv = image_preprocess_with_hsv_improve