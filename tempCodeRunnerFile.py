import speech_recognition as sr
         except sr.UnknownValueError:
             print("Sorry, I could not understand the audio.")
         except sr.RequestError:
             print("Sphinx error;{0}".format(e))