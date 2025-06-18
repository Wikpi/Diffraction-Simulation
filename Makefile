.PHONY: run clean update help

run:
	@echo "Running Diffraction Simulation..."
	python3 main.py

clean:
	@echo "Cleaning Up Saved Data..."
	rm -rf data/saved/

update:
	@echo "Cannot install required paackages yet"

help:
	@echo "To run the diffraction simulation run (from root project directory):"
	@echo "make run"
	@echo "or:"
	@echo "python3 main.py"
	@echo ""
	@echo "Clean saved data:"
	@echo "make clean"