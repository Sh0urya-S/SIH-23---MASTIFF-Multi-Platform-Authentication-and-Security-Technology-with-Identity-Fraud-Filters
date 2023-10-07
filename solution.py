import instaloader
import numpy as np
import os
import cv2

def checkfake(main_string, substrings):
    main_string = main_string.lower()
    for substring in substrings:
        if substring in main_string:
            print("No suspicious keywords found in bio as per recently collected data!")
            return
    print("Suspicious keywords found in bio as per recently collected data")

def compare_images(image1, image2):
  mse = np.mean((image1 - image2)**2)
  similarity = 10 * np.log10(255 * 255 / mse)
  return similarity

loader = instaloader.Instaloader()

inpusername=input("Enter the username of the suspected account:")
realusername=input("Enter the username of the real account:")
loc1 = inpusername
loc2 = realusername

profile = instaloader.Profile.from_username(loader.context, inpusername)

followercount = profile.followers
print("Follower count is:",followercount)

main_str = profile.biography
print(main_str)
substrs = ["invest","click","crypto","free","$","get now"]
checkfake(main_str,substrs)

print("Checking pfp")

loader.download_profile(inpusername, profile_pic_only=True)
loader.download_profile(realusername, profile_pic_only=True)

if os.path.exists(loc1):
    for filename in os.listdir(loc1):
        if filename.endswith(".jpg"):
          fakeimgname1 = filename
            
if os.path.exists(loc2):
    for filename in os.listdir(loc2):
        if filename.endswith(".jpg"):
          realimgname1 = filename
            
fakeimgname = os.path.join(loc1, fakeimgname1)
realimgname = os.path.join(loc2, realimgname1)

image1 = cv2.imread(fakeimgname)
image2 = cv2.imread(realimgname)

similarity = compare_images(image1, image2)

if similarity<20:
    print("Very poor image quality. The two images are very different.")
elif similarity>=20 and similarity<30:
    print("Poor image quality. The two images are somewhat similar, but there are noticeable differences.")
elif similarity>=30 and similarity<40:
    print("Good image quality. The two images are very similar, and the differences are not noticeable to the human eye.")
elif similarity>=40 and similarity<50:
    print("Excellent image quality. The two images are almost identical.")
else:
    print("The two images are indistinguishable to the human eye.")
