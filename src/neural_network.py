
def choose_action(bird, pipe):
    """
    Temporary AI controller.
    Returns True when the bird should flap.
    """

    gap_center = pipe.top_height + pipe.gap / 2

    # If the bird is below the center of the gap,
    # flap to move upward.
    if bird.y > gap_center:
        return True

    return False
