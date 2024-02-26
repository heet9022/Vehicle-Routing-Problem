We have provided a python script to run your program on the provided training problems. You are not required to use this, but you might find it helpful in validating your submission. Recall, your program should accept a command line argument containing a path to a problem in the format described in the prompt.

To use the evaluation script, run the following in a shell:

python3 evaluateShared.py --cmd {command to run your program} --problemDir {folder containing training problems}

The script will load every problem in the training problem folder, and run the command on each file. The {command to run your program} should NOT include a file directory (as these will be read from the problemDir folder).

For example, if your solution is a python3 script called "mySubmission.py", and you have downloaded the training problems to a folder called "trainingProblems", then run

python3 evaluateShared.py --cmd "python3 mySubmission.py" --problemDir trainingProblems

(Quotes are needed around "python3 mySubmission.py" because of the space.) If your solution is a compiled executable called "mySubmission", then it would be

python3 evaluateShared.py --cmd ./mySubmission --problemDir trainingProblems

The script will check your program for errors and print your score on each problem.