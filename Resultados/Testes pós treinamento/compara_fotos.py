# Often instead of just checking if two faces match or not (True or False), it's helpful to see how similar they are.
# You can do that by using the face_distance function.

# The model was trained in a way that faces with a distance of 0.6 or less should be a match. But if you want to
# be more strict, you can look for a smaller face distance. For example, using a 0.55 cutoff would reduce false
# positive matches at the risk of more false negatives.

# Note: This isn't exactly the same as a "percent match". The scale isn't linear. But you can assume that images with a
# smaller distance are more similar to each other than ones with a larger distance.

import face_recognition


names = [
    "ana", "fatima", "faustao", "gugu", "malandro", "ratinho", "raul", "regina", "sonia", "xuxa"
]

for i in names:
    # Load image to compare against and get enconding for it
    known_image = face_recognition.load_image_file("imagens/" + i +  "1.jpg") 
    known_encoding = face_recognition.face_encodings(known_image)[0]
    known_encodings = [
        known_encoding
    ]
    # Load a test image and get enconding for it
    image_to_test = face_recognition.load_image_file("imagens/" + i + "2.jpg")
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

    # See how far apart the test image is from the known face
    distance = face_recognition.face_distance(known_encodings, image_to_test_encoding)

    print("{}2 has a distance of {:.3} from known image {}1".format(i, distance[0], i))
