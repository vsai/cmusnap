import Image

# REQUIRES: All images are the same dimensions
# ENSURES : Stitched image in order - img1 topleft, img2 topright, img3 bottomleft, img4 bottomright
def stitch(img1_url, img2_url, img3_url, img4_url):
  img1 = Image.open(img1_url)

  pxl1 = Image.open(img1_url).load()
  pxl2 = Image.open(img2_url).load()
  pxl3 = Image.open(img3_url).load()
  pxl4 = Image.open(img4_url).load()

  rows = img1.size[0]
  cols = img1.size[1]

  res_img = Image.new("RGB", (rows * 2, cols * 2))
  res_pxls = res_img.load()


  for i in range(rows):
    for j in range(cols):
      res_pxls[i,j] = pxl1[i,j]
      res_pxls[i,j+cols] = pxl2[i,j]
      res_pxls[i+rows,j] = pxl3[i,j]
      res_pxls[i+rows,j+cols] = pxl4[i,j]

  
  res_img.show()
  print "yolo"

stitch("frame.jpg", "frame.jpg", "frame.jpg", "frame.jpg")