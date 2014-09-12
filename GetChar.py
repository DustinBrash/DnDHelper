__name__ = "GetChar"
import pickle
import CharGen

def get_chars():
    name = raw_input("Which file: ")
    f = open(name, 'r')
    chars = pickle.load(f)
    f.close()
    return chars

def save_chars(chars):
    name = raw_input("Which file: ")
    f = open(name, 'w')
    pickle.dump(chars, f)
    f.close()


