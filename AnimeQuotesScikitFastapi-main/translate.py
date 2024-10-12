from deep_translator import GoogleTranslator

def translate(text, source, target):
    return GoogleTranslator(source=source, target=target).translate(text)

if __name__ == '__main__':
    print(translate("Translate this, robot!", 'en', 'tr'))