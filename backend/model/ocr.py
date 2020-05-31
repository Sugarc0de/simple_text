import cv2
import numpy as np
import read_stardict
import pytesseract
import spacy
import re
import string

class OCR:
    """
    Interface for the class:
    ocr = OCR(filename, hsv_lower, hsv_upper)
    ocr.recognize() returns a list of detected highlighted English words

    hsv_lower and hsv_upper is a list that defines specified hsv color range
    """

    def __init__(self, image_file, hsv_lower, hsv_upper):
        self.image = image_file #cv2.imread(image_file)
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper
        self.dic = read_stardict.Dictionary('stardict-lazyworm-ec-2.4.2/')

        self.rgb = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2RGB)

        # rgb to HSV color spave conversion
        hsv_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        HSV_lower = np.array(hsv_lower, np.uint8)  # Lower HSV value
        HSV_upper = np.array(hsv_upper, np.uint8)  # Upper HSV value

        # Threshold
        frame_threshed = cv2.inRange(hsv_img, HSV_lower, HSV_upper)

        # find connected components
        self.contours, self.hierarchy, = cv2.findContours(frame_threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        self.sp = spacy.load('en_core_web_sm')

    def find_and_format_word(self, word):
        if not word:
            return '', ''
        lemma_word = self.sp(word)
        if lemma_word[0].lemma_ == word:
            chinese_text = self.dic.lookup(word)
        else:
            chinese_text = self.dic.lookup(lemma_word[0].lemma_)
        if chinese_text:
            formated_chinese = chinese_text.replace('\n', ' ')
            return formated_chinese, chinese_text
        return '', ''

    # get the thresholded image
    def threshold_image(self, img, v):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, th = cv2.threshold(gray, v, 255, cv2.THRESH_BINARY)
        return th


    def calc_areas(self):
        areas = []
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            areas.append(area)
        self.areas = np.array(areas)


    def warp_image(self, rgb_image):
        warped_images = []
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            if area > np.mean(self.areas):

                rect = cv2.minAreaRect(cnt)
                big_rect = (rect[0], (1.5 * rect[1][0], 1.5 * rect[1][1]), rect[2])
                box = cv2.boxPoints(big_rect)
                box = np.int0(box)

                width = int(big_rect[1][0])
                height = int(big_rect[1][1])

                src_pts = box.astype("float32")
                # coordinate of the points in box points after the rectangle has been
                # straightened
                dst_pts = np.array([[0, height - 1],
                                    [0, 0],
                                    [width - 1, 0],
                                    [width - 1, height - 1]], dtype="float32")
                # the perspective transformation matrix
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)

                # directly warp the rotated rectangle to get the straightened rectangle
                warped = cv2.warpPerspective(rgb_image, M, (width, height))
                if width < height:
                    warped = np.rot90(warped)
                warped_images.append(warped)
        return warped_images

    def remove_non_english(self, warped, v):
        '''
        Input:
        warped, single bounded image for a potential word
        v is the value for thresholding, can be 120, 150, or 180

        Return,
        a English word from a dictionary or None
        '''
        th = self.threshold_image(warped, v)
        candidate = pytesseract.image_to_string(th)
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        candidate = regex.sub('', candidate)
        words = [] or re.split(r'\—|\s+|\n', candidate)
        print(words)
        longest_word = ''
        definition = ''
        for idx, word in enumerate(words):
            formatted_chinese, chinese = self.find_and_format_word(word)
            if chinese:
                if len(longest_word) < len(word):
                    longest_word = word
                    definition = formatted_chinese
        return longest_word, definition


    def recognize(self):
        v = [120, 150, 180]
        """
        :return: a list of list of English words and their definitions
        """
        ans = []
        self.calc_areas()
        warped_images = self.warp_image(self.rgb)
        for warped in warped_images:
            target_word, target_definition = '', ''
            for val in v:
                word, definition = self.remove_non_english(warped, val)
                if len(target_word) < len(word):
                    target_word = word
                    target_definition = definition
            if target_word != '' and target_definition != '':
                ans.append([target_word, target_definition])
        return ans








