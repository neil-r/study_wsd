import nltk

def download_datasets():
    # Download SemCor dataset if not already downloaded
    nltk.download('semcor')
    nltk.download('wordnet')

if __name__ == "__main__":
    download_datasets()
