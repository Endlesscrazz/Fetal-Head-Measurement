import math

import numpy as np

from src.evaluation.metrics import dice_score, hd95, iou_score


def test_dice_and_iou_are_one_for_identical_masks():
    mask = np.zeros((16, 16), dtype=np.uint8)
    mask[4:12, 4:12] = 1

    assert dice_score(mask, mask) == 1.0
    assert iou_score(mask, mask) == 1.0


def test_hd95_is_zero_for_identical_masks():
    mask = np.zeros((16, 16), dtype=np.uint8)
    mask[4:12, 4:12] = 1

    assert hd95(mask, mask) == 0.0


def test_hd95_is_infinite_for_one_empty_mask():
    mask = np.zeros((16, 16), dtype=np.uint8)
    mask[4:12, 4:12] = 1
    empty = np.zeros((16, 16), dtype=np.uint8)

    assert math.isinf(hd95(mask, empty))
