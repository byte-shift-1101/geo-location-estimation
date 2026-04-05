import os
import numpy as np
from sample import constants
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame
from sample.assembly import Assembly

def _to_top_left(px, py, image_height, origin):
  if origin == "top_left":
    return float(px), float(py)
  if origin == "bottom_left":
    return float(px), float(image_height - py)
  raise ValueError("origin must be 'top_left' or 'bottom_left'")


def print_points_dicts_as_numpy(points, actual_origin="top_left", predicted_origin="top_left"):
    """
  Convert a list of point dictionaries into a 2D numpy array and print it.
  Also projects each world point to screen coordinates using assembly.get_screen_point.

    Expected input format:
    [
        {"label": "A", "position": [x, y, z]},
        {"label": "B", "position": [x, y, z]},
    ]

    Output array columns:
    [world_x, world_y, world_z, actual_screen_x, actual_screen_y, screen_error_distance]

    Notes:
    - If a point includes screen_point, it is treated as the actual point.
    - Predicted point is always computed using assembly.get_screen_point.
    - Both actual and predicted points are normalized to top-left origin before error.
    - screen_error_distance is Euclidean pixel distance between actual and predicted.
    - If screen_point is missing, actual is set to predicted and error becomes 0.
    """
    if points is None:
        raise ValueError("points cannot be None")

    assembly = Assembly("sihaag")
    assembly.storage_path = os.path.join(constants.CONFIG_FOLDER, "assembly/sihaag.json")
    assembly.load()
    if assembly.camera is None:
      raise ValueError("Camera is not set for this assembly.")
    image_height = float(assembly.camera.image_height)

    rows = []
    for idx, point in enumerate(points):
        if not isinstance(point, dict):
            raise ValueError(f"Point at index {idx} must be a dictionary")
        if 'position' not in point:
            raise ValueError(f"Point at index {idx} is missing 'position'")

        position = point['position']
        if not isinstance(position, (list, tuple, np.ndarray)) or len(position) != 3:
            raise ValueError(f"Point at index {idx} must have a 3-element 'position'")

        world_x, world_y, world_z = float(position[0]), float(position[1]), float(position[2])
        predicted_screen_x, predicted_screen_y = assembly.get_screen_point((world_x, world_y, world_z))
        predicted_screen_x, predicted_screen_y = _to_top_left(
          predicted_screen_x,
          predicted_screen_y,
          image_height,
          predicted_origin
        )

        if point.get('screen_point') is not None:
            screen_point = point['screen_point']
            if not isinstance(screen_point, (list, tuple, np.ndarray)) or len(screen_point) != 2:
                raise ValueError(f"Point at index {idx} must have a 2-element 'screen_point'")
            actual_screen_x, actual_screen_y = _to_top_left(
              float(screen_point[0]),
              float(screen_point[1]),
              image_height,
              actual_origin
            )
        else:
            actual_screen_x, actual_screen_y = float(predicted_screen_x), float(predicted_screen_y)

        # print(actual_screen_x, actual_screen_y, predicted_screen_x, predicted_screen_y)
        screen_error_distance = float(np.hypot(
            actual_screen_x - float(predicted_screen_x),
            actual_screen_y - float(predicted_screen_y)
        ))
        rows.append([
            idx,
            world_x,
            world_y,
            world_z,
            predicted_screen_x,
            predicted_screen_y,
            screen_error_distance
        ])

    points_2d = np.array(rows, dtype=float)
    print(points_2d)
    return points_2d

def main():
    assembly = Assembly("sihaag")
    assembly.storage_path = os.path.join(constants.CONFIG_FOLDER, "assembly/sihaag.json")
    assembly.load()
    print(assembly)

    print(assembly.camera)
    for rf in assembly.reference_frames:
        print(rf)

    point = (2, 2, 3)
    point_homogeneous = np.append(point, 1)
    for rf in assembly.reference_frames:
        point_homogeneous = rf.conversion_matrix_from_parent_4x4 @ point_homogeneous

    pixel_coords_homogeneous = assembly.camera.intrinsic_matrix_4x4 @ point_homogeneous
    print(f"Pixel coords homogeneous: {pixel_coords_homogeneous}")

    pixel_x, pixel_y = assembly.get_screen_point(point)
    print(f"Screen point: ({pixel_x}, {pixel_y})")

if __name__ == "__main__":
    print_points_dicts_as_numpy(
  [
  {
    "label": "A",
    "position": [
      -7.859446914334361,
      -3.3779612374395676,
      -10.307392177956404
    ],
    "screen_point": [
      372.5896279942472,
      896.5764591924581
    ],
    "projection_status": "ok",
    "distance_to_camera": 16.867096764922124
  },
  {
    "label": "B",
    "position": [
      -15.79912684196854,
      -19.91805126770513,
      -55.70275331004024
    ],
    "screen_point": [
      707.5030162791502,
      869.4362788135235
    ],
    "projection_status": "ok",
    "distance_to_camera": 64.87391525263246
  },
  {
    "label": "C",
    "position": [
      3.8257571627199924,
      -11.704971681208182,
      -19.45028996753691
    ],
    "screen_point": [
      1071.0556961690306,
      1078.62206955122
    ],
    "projection_status": "ok",
    "distance_to_camera": 26.454237315633765
  },
  {
    "label": "D",
    "position": [
      3.328841558289543,
      -2.7782041663503376,
      -5.322850367951151
    ],
    "screen_point": [
      1206.8856298418334,
      1046.5479619784455
    ],
    "projection_status": "ok",
    "distance_to_camera": 9.875453220295705
  },
  {
    "label": "E",
    "position": [
      38.602631070335526,
      -15.334676328499697,
      -39.59822034377789
    ],
    "screen_point": [
      1738.8516325784558,
      899.0477733703603
    ],
    "projection_status": "ok",
    "distance_to_camera": 59.40586876128202
  },
  {
    "label": "F",
    "position": [
      -4.889659178535627,
      1.157171259843847,
      -2.90480650471157
    ],
    "screen_point": [
      79.93966060461776,
      665.9394006731691
    ],
    "projection_status": "ok",
    "distance_to_camera": 8.382433142150687
  },
  {
    "label": "G",
    "position": [
      -0.943525743612786,
      1.4370500235790842,
      -0.474924231116276
    ],
    "screen_point": [
      466.5161837247164,
      682.939553874838
    ],
    "projection_status": "ok",
    "distance_to_camera": 4.021107236077768
  },
  {
    "label": "H",
    "position": [
      3.153578205478857,
      -2.473539168478265,
      -17.626122748472994
    ],
    "screen_point": [
      1052.123622277248,
      731.3646003432364
    ],
    "projection_status": "ok",
    "distance_to_camera": 21.21526317098371
  },
  {
    "label": "I",
    "position": [
      32.47384957978684,
      -9.330246124061096,
      -45.970849518605974
    ],
    "screen_point": [
      1527.0745847246822,
      744.1407295711522
    ],
    "projection_status": "ok",
    "distance_to_camera": 59.30532680271478
  },
  {
    "label": "J",
    "position": [
      19.421265313582115,
      -1.9998095667203906,
      -16.413473423894494
    ],
    "screen_point": [
      1797.2288177554733,
      721.7875036153616
    ],
    "projection_status": "ok",
    "distance_to_camera": 27.059646019555935
  },
  {
    "label": "K",
    "position": [
      -6.26093229959609,
      2.37387870964901,
      -5.450666928958803
    ],
    "screen_point": [
      201.89500348574157,
      500.9637845141477
    ],
    "projection_status": "ok",
    "distance_to_camera": 11.14785605814161
  },
  {
    "label": "L",
    "position": [
      -11.983988440849664,
      7.195107436963381,
      -51.676565128073
    ],
    "screen_point": [
      750.4754806691849,
      456.1657919243754
    ],
    "projection_status": "ok",
    "distance_to_camera": 56.43668905347051
  },
  {
    "label": "M",
    "position": [
      -5.888569806843421,
      -2.115183675814059,
      -55.14571782994104
    ],
    "screen_point": [
      855.470401115396,
      602.4452551155066
    ],
    "projection_status": "ok",
    "distance_to_camera": 58.696777020791906
  },
  {
    "label": "N",
    "position": [
      4.801925102456624,
      2.3862715548555298,
      -13.789296831305897
    ],
    "screen_point": [
      1159.801620437392,
      519.7003674430258
    ],
    "projection_status": "ok",
    "distance_to_camera": 17.218720286028187
  },
  {
    "label": "O",
    "position": [
      68.82954701369647,
      7.992074727317598,
      -74.2561439501288
    ],
    "screen_point": [
      1734.6648412020274,
      471.56596466476674
    ],
    "projection_status": "ok",
    "distance_to_camera": 102.98186338217056
  },
  {
    "label": "P",
    "position": [
      -50.867315796014864,
      26.25579873998803,
      -70.98290189534023
    ],
    "screen_point": [
      341.42784306755755,
      250.72415230197012
    ],
    "projection_status": "ok",
    "distance_to_camera": 93.55229549965023
  },
  {
    "label": "Q",
    "position": [
      -0.8060567633461426,
      3.0815417375234917,
      -1.1320527560881377
    ],
    "screen_point": [
      574.3498589278495,
      309.0566918403029
    ],
    "projection_status": "ok",
    "distance_to_camera": 4.637395124585487
  },
  {
    "label": "R",
    "position": [
      7.709406900690932,
      10.475994763048913,
      -29.639208777759137
    ],
    "screen_point": [
      1141.372928475642,
      310.8715517372965
    ],
    "projection_status": "ok",
    "distance_to_camera": 34.38279479362346
  },
  {
    "label": "S",
    "position": [
      8.971141111292575,
      9.5364426141937,
      -19.773475722418013
    ],
    "screen_point": [
      1268.829754037175,
      248.01197891736865
    ],
    "projection_status": "ok",
    "distance_to_camera": 25.277821392927358
  },
  {
    "label": "T",
    "position": [
      41.5439283239419,
      6.689494534031625,
      -35.026334051554485
    ],
    "screen_point": [
      1900.7393769784815,
      431.1898193228656
    ],
    "projection_status": "ok",
    "distance_to_camera": 55.78354205607656
  },
  {
    "label": "U",
    "position": [
      -0.4220920422678527,
      3.305018322753938,
      0.8581512792537369
    ],
    "screen_point": [
      374.1763917536862,
      2.404317062293302
    ],
    "projection_status": "ok",
    "distance_to_camera": 2.8832160068172934
  },
  {
    "label": "V",
    "position": [
      -12.134313834149166,
      20.4320908970314,
      -31.600956571281515
    ],
    "screen_point": [
      625.0752512000809,
      69.98203853673768
    ],
    "projection_status": "ok",
    "distance_to_camera": 41.34583861016801
  },
  {
    "label": "W",
    "position": [
      0.5771088754578548,
      9.181028527816071,
      -9.155704023504349
    ],
    "screen_point": [
      929.3043799912233,
      18.763894133087607
    ],
    "projection_status": "ok",
    "distance_to_camera": 14.124699923451988
  },
  {
    "label": "X",
    "position": [
      6.445966891427208,
      5.846528934926434,
      -5.5518633918419
    ],
    "screen_point": [
      1521.8782206379674,
      143.1410258863104
    ],
    "projection_status": "ok",
    "distance_to_camera": 10.843832703545056
  }
]
)