FROM python:3.9-slim

WORKDIR /Harmonix

COPY src/ /Harmonix/src/
COPY sample_input/ /Harmonix/sample_input/
COPY sample_output/ /Harmonix/sample_output/
COPY runner_output/ /Harmonix/runner_output/

ENTRYPOINT ["python", "/Harmonix/src/scanner_runner.py"]
