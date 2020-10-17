Requirements.txt contains all the dependencies.
	Linking something such as : 
		https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
	allows a way to install pretrained models for NER or other operations in Python. To train models on our own, look at scikit and sklearn.
	The advantage of using the direct download link is to have everything in the same requirements file, which is easier for the Dockerfile.