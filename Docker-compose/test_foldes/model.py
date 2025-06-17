from datetime import datetime
import os

class Model:
    """Test dummy model for testng FlaskAPI and FastAPI
    """
    def __init__(self, name='') -> None:
        self.name = name

    def fit(self, example='')-> int:
        # os.makedirs('data', exist_ok=True)
        with open('data/test.txt', 'a') as f:
            s = example + ' - ' + str(datetime.now()) + '\n'
            f.writelines(s)

        return len(example)
        
    def predict(self)-> str:
        res = ''
        with open('data/test.txt', 'r') as f:
            # res = f.readline(-1)
            for x in f:
                res = x
            
        return 'dummy_predict: ' + res
    
def main():
    model = Model('dummy_model')
    model.fit('test')
    print(model.predict())

if __name__ == '__main__':
    main()