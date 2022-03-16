import os
import math
import sys
import cv2
import numpy as np

if len(sys.argv) < 2:
    print(
        'Missing arguments. Please provide a path to the image folder.\n'
        'The folder should contain both images (.jpg) and landmarks (.txt)\n'
        'Usage example: python average.py ./images\n'
    )
    exit()

def main():
    w = 170
    h = 240

    if len(sys.argv) == 3:
        if str.isdigit(sys.argv[2]):
            w = int(sys.argv[2])
        if str.isdigit(sys.argv[3]):
            h = int(sys.argv[3])

    path = sys.argv[1]


    all_points = read_points(path)

    images = read_images(path)

    eyecorner_dst = [
        (np.int(0.3 * w), np.int(h / 3)),
        (np.int(0.7 * w), np.int(h / 3))
    ]

    images_norm = []
    points_norm = []


    boundary_pts = np.array([
        (0, 0), (w / 2, 0), (w - 1, 0), (w - 1, h / 2),
        (w - 1, h - 1), (w / 2, h - 1), (0, h - 1), (0, h / 2)
    ])


    points_avg = np.array(
        [(0, 0)] * (len(all_points[0]) + len(boundary_pts)),
        np.float32()
    )

    num_images = len(images)
    print(num_images)

    for i in range(0, num_images):
        print(i)
        points1 = all_points[i]


        eyecorner_src = [all_points[i][36], all_points[i][45]]


        tform = similarity_transform(eyecorner_src, eyecorner_dst)


        img = cv2.warpAffine(images[i], tform, (w, h))
        cv2.imwrite("C:/Users/Uzivatel/Documents/CroppedAlignedFace" + "/" + str(i) + ".jpg",img*255)


        points2 = np.reshape(np.array(points1), (68, 1, 2))
        points = cv2.transform(points2, tform)
        points = np.float32(np.reshape(points, (68, 2)))


        points = np.append(points, boundary_pts, axis=0)


        points_avg = points_avg + points / num_images

        points_norm.append(points)
        images_norm.append(img)


    rect = (0, 0, w, h)
    tri = calculate_triangles(rect, np.array(points_avg))


    output = np.zeros((h, w, 3), np.float32())


    for i in range(0, len(images_norm)):
        img = np.zeros((h, w, 3), np.float32())

        for j in range(0, len(tri)):
            t_in = []
            t_out = []

            for k in range(0, 3):
                p_in = points_norm[i][tri[j][k]]
                p_in = constrain_point(p_in, w, h)

                p_out = points_avg[tri[j][k]]
                p_out = constrain_point(p_out, w, h)

                t_in.append(p_in)
                t_out.append(p_out)

            warp_triangle(images_norm[i], img, t_in, t_out)


        output = output + img


    output = output / num_images


    cv2.imwrite( "average_face.jpg", 255 * output)
  

def read_points(path):

    points_array = []


    for file_path in sorted(os.listdir(path)):
        print(file_path)

        if file_path.endswith('.txt'):

            points = []


            with open(os.path.join(path, file_path)) as f:
                for line in f:
                    x, y = line.split()
                    points.append((int(x), int(y)))


            points_array.append(points)

    return points_array


def read_images(path):

    images_array = []


    for file_path in sorted(os.listdir(path)):
        if file_path.endswith('.jpg'):
            # Read image found.
            img = cv2.imread(os.path.join(path, file_path))

            # Convert to float_ing point
            img = np.float32(img) / 255.0

            # Add to array of images
            images_array.append(img)

    return images_array



def similarity_transform(in_points, out_points):
    s60 = math.sin(60 * math.pi / 180)
    c60 = math.cos(60 * math.pi / 180)

    in_pts = np.copy(in_points).tolist()
    out_pts = np.copy(out_points).tolist()

    xin = c60 * (in_pts[0][0] - in_pts[1][0]) - s60 * \
        (in_pts[0][1] - in_pts[1][1]) + in_pts[1][0]
    yin = s60 * (in_pts[0][0] - in_pts[1][0]) + c60 * \
        (in_pts[0][1] - in_pts[1][1]) + in_pts[1][1]

    in_pts.append([np.int(xin), np.int(yin)])

    xout = c60 * (out_pts[0][0] - out_pts[1][0]) - s60 * \
        (out_pts[0][1] - out_pts[1][1]) + out_pts[1][0]
    yout = s60 * (out_pts[0][0] - out_pts[1][0]) + c60 * \
    (out_pts[0][1] - out_pts[1][1]) + out_pts[1][1]

    out_pts.append([np.int(xout), np.int(yout)])

    tform = cv2.estimateAffinePartial2D(np.array([in_pts]), np.array([out_pts]));
    
    return tform[0]


def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def calculate_triangles(rect, points):

    subdiv = cv2.Subdiv2D(rect)


    for p in points:
        subdiv.insert((p[0], p[1]))


    triangle_list = subdiv.getTriangleList()

    delaunay_tri = []

    for t in triangle_list:
        pt = []

        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3):
            ind = []
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0:
                        ind.append(k)
            if len(ind) == 3:
                delaunay_tri.append((ind[0], ind[1], ind[2]))

    return delaunay_tri

def constrain_point(p, w, h):
    p = (min(max(p[0], 0), w - 1), min(max(p[1], 0), h - 1))

    return p


def apply_affine_transform(src, src_tri, dst_tri, size):


    warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))


    dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), None,
        flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    return dst


def warp_triangle(img1, img2, t1, t2):


    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1_rect = []
    t2_rect = []
    t2_rect_int = []

    for i in range(0, 3):
        t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2_rect_int.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])

    img2_rect = apply_affine_transform(img1_rect, t1_rect, t2_rect, size)
    img2_rect = img2_rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * ((1.0, 1.0, 1.0) - mask)
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2_rect

if __name__ == '__main__':
    main()
