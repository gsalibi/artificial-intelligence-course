import dlib


training_xml_path = "train_cleaned.xml"
testing_xml_path = "test_cleaned.xml"
model_name = "predictor.dat"


# seta parâmetros
options = dlib.shape_predictor_training_options()
options.tree_depth = 2
options.nu = 0.1
options.cascade_depth = 5
options.feature_pool_size = 150  
options.num_test_splits = 20
options.be_verbose = True


# treina modelo
dlib.train_shape_predictor(training_xml_path, model_name, options)


# imprime saída
print("\nTraining accuracy: {}".format( dlib.test_shape_predictor(training_xml_path, model_name)))
print("Testing accuracy: {}".format(dlib.test_shape_predictor(testing_xml_path, model_name)))
