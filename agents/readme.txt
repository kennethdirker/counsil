Python virtual environment:
	sudo apt install pip3
	python -m venv env
	. env/bin/activate
	pip install -f requirements.txt

Note:
	CUDA and thus also torch versions are GPU dependent - installing requirements.txt is probably not enough to install the correct Python libraries.
Fix: CUDA/Torch versions
	
