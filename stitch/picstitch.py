import Image

# Size of Image to be stitched. We keep this constant
# so that we can add the snap img if there are an
# odd number of images
ROWS = 640
COLS = 480


# REQUIRES: All images are 640 x 480
# ENSURES : Stitched image in order of input
def stitch(urls):
  pixels = [Image.open(url).load() for url in urls]
  pixels_len = len(pixels)


  if (pixels_len % 2 == 1):
    # TODO: Add snap img here
    print "odd number.. aborting"
    pixels_len = pixels_len + 1
    return

  # Assuming even if it gets here we have an even # of images

  # Array of tuples that represent [r,c] such that the
  # the [r,c] value at idx 'i' represents the position of the top-left
  # pixel in the 'i'-th image in the urls array
  rc_starts = [[]] * pixels_len
  for i in range(pixels_len):
    rc = [0] * 2
    if i % 2 == 0:
      # Left Column
      rc[0] = (i / 2) * ROWS #row
      rc[1] = 0

    else:
      # Right Column
      rc[0] = ((i-1) / 2) * ROWS 
      rc[1] = COLS

    rc_starts[i] = rc

  # Each stitched picture is an X by 2 array, where X is
  # the number of rows necessary (ie, pixels_len / 2)
  res_img = Image.new("RGB", (ROWS * (pixels_len / 2), COLS * 2), "Black")
  res_pxls = res_img.load()

  for r in range(ROWS):
    for c in range(COLS):
      for i in range(pixels_len):
        startR = rc_starts[i][0]
        startC = rc_starts[i][1]

        res_pxls[r + startR, c + startC] = pixels[i][r,c]

  res_img.save("res.jpg", "JPEG")

stitch(["temp/yolo_2014-04-29_07-03-17.jpg",
  "temp/yolo_2014-04-29_07-03-17.jpg",
  "temp/yolo_2014-04-29_07-03-17.jpg",
  "temp/yolo_2014-04-29_07-03-17.jpg"])

