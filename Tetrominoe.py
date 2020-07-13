class Tetrominoe(object):

    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),  # z-shape
        ((0, -1), (0, 0), (1, 0), (1, 1)),  # s-shape
        ((0, -1), (0, 0), (0, 1), (0, 2)),  # l-shape
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),  # SquareShape
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1)),
        # ((0, -2), (0, -1), (0, 0), (0, 1), (0, 2)), # long l-shape
        ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)),  # x-shape
        ((-1, 0), (1, -1), (0, -1), (2, 0), (0, 0), (1, 0)) # trapezoid-shape
    )

    NoShape = 0
    # ZShape = 1
    # SShape = 2
    # LineShape = 3
    # TShape = 4
    # SquareShape = 5
    # LShape = 6
    # MirroredLShape = 7
    # roundShapr = 8