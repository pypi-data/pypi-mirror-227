import subprocess
import sys


def checkForOutdatedPackages():
	cmd = ["poetry", "show", "--outdated"]
	result = subprocess.run(cmd, capture_output=True, text=True)
	return result.stdout.strip().split("\n")[1:]


def cli():
	outdatedPackages = checkForOutdatedPackages()
	if outdatedPackages:
		print("Outdated packages (powered by poetry):")
		for package in outdatedPackages:
			print(package)
	else:
		print("No outdated packages.")

	sys.exit(1 if outdatedPackages else 0)
