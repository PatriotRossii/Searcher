def get_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = [float(e) for e in envelope["lowerCorner"].split()]
    upper_corner = [float(e) for e in envelope["upperCorner"].split()]

    delta_x = upper_corner[0] - lower_corner[0]
    delta_y = upper_corner[1] - lower_corner[1]

    return str(delta_x), str(delta_y)


def get_size_from_points(lower_corner, upper_corner):
    delta_x = upper_corner[0] - lower_corner[0]
    delta_y = upper_corner[1] - lower_corner[1]

    return str(delta_x), str(delta_y)
