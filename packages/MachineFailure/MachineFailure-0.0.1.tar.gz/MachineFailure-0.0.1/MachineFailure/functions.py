import pickle

def load_pickle_object(model_path: str):
    """
        Loading the model
        Args:
            model_path : should be the full path with .pkl extension
    """
    
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
        
    return model
    
    
def predict(model, test_data):
    
    """
        predict the output for given data using given pre trained model
    """
        
    y_pred = model.predict(test_data)
    
    return y_pred
