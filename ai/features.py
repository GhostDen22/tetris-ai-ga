def get_column_heights(board_grid):
    if not board_grid:
        return []

    height = len(board_grid)
    width = len(board_grid[0])
    heights = []

    for x in range(width):
        column_height = 0

        for y in range(height):
            if board_grid[y][x] != 0:
                column_height = height - y
                break

        heights.append(column_height)

    return heights


def count_holes(board_grid):
    if not board_grid:
        return 0

    height = len(board_grid)
    width = len(board_grid[0])
    holes = 0

    for x in range(width):
        found_block = False

        for y in range(height):
            if board_grid[y][x] != 0:
                found_block = True
            elif found_block:
                holes += 1

    return holes


def calculate_bumpiness(heights):
    bumpiness = 0

    for i in range(len(heights) - 1):
        bumpiness += abs(heights[i] - heights[i + 1])

    return bumpiness


def extract_features(board_grid, lines_cleared=0):
    heights = get_column_heights(board_grid)

    aggregate_height = sum(heights)
    max_height = max(heights) if heights else 0
    holes = count_holes(board_grid)
    bumpiness = calculate_bumpiness(heights)

    return {
        "holes": holes,
        "aggregate_height": aggregate_height,
        "max_height": max_height,
        "bumpiness": bumpiness,
        "lines_cleared": lines_cleared,
    }
