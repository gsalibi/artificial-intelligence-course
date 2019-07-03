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
