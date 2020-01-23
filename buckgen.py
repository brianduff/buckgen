#!/usr/bin/env python3

# A super simple script that runs buck audit classpath, scrobbles the
# output and squirts it into Eclipse projects that VSCode is happy with.
# Author: bduff@fb.com

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser("Buck project generator")
parser.add_argument(
    "-s",
    "--sourcepath",
    help="comma separated list of sourcepath entries to add",
    default=".",
    type=lambda s: s.split(","),
)
args, targets = parser.parse_known_args()

if not targets:
    sys.exit("Must specify at least one buck target")

classpath = (
    subprocess.check_output(["buck", "audit", "classpath"] + targets)
    .decode(sys.stdout.encoding)
    .split()
)

project_template = """<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>graphs_a0b7f002</name>
	<comment></comment>
	<projects>
	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.jdt.core.javabuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>org.eclipse.jdt.core.javanature</nature>
	</natures>
</projectDescription>
"""

classpath_template = """<?xml version="1.0" encoding="UTF-8"?>
<classpath>
  <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/>
  <classpathentry kind="output" path="bin"/>
</classpath>
"""

root = ET.fromstring(classpath_template)
for source_entry in args.sourcepath:
    ET.SubElement(root, "classpathentry", {"kind": "src", "path": source_entry})

for classpath_entry in classpath:
    ET.SubElement(root, "classpathentry", {"kind": "lib", "path": classpath_entry})


ET.ElementTree(root).write(".classpath", encoding=sys.stdout.encoding)
ET.ElementTree(ET.fromstring(project_template)).write(
    ".project", encoding=sys.stdout.encoding
)

print("👷 Built .classpath and .project. Enjoy!")