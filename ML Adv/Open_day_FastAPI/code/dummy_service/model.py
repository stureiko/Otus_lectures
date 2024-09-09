class Model:
    """Test dummy model for testng API
    """
    def __init__(self, name='') -> None:
        self.name = name

    def fit(self, example='')-> bool:
        if example == None:
            return False
        else:
            return True
        
    def predict(self, example='')-> int:
        if example == None:
            return False
        else:
            return len(example)
    
def main():
    model = Model('dummy_model')
    model.predict('test')

if __name__ == '__main__':
    main()