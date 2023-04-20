from lang_detector import train, test_model

languages = ['cs', 'de', 'en', 'es', 'fr', 'it', 'pl', 'pt', 'ru', 'sk']


# TODO Vhodně doplnte části kódu v souboru lang_detector.py označené ### START CODE HERE ### a ### END CODE HERE ###

def main():
    train()
    test_model('model.bin')


if __name__ == '__main__':
    main()
