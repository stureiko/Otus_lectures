class Model:
    """Test dummy model for testng FlaskAPI and FastAPI
    """
    def __init__(self, name='') -> None:
        self.name = name

    def fit(self, example='')-> int:
        return len(example)
        
    def predict(self, example='')-> str:
        return 'dummy_predict: ' + example
    
def main():
    model = Model('dummy_model')
    model.predict('test')

if __name__ == '__main__':
    main()