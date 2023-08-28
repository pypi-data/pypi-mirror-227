import argparse
import ai_assignment_marker.AssignmentsRunner as AssignmentsRunner

def cli():
  parser = argparse.ArgumentParser(
                    prog='AI assignment marker',
                    description='This marker will go through a directory and mark all of the .cpp submissions using AI to a given grading rubric.',
                    epilog='Text at the bottom of help')
  
  parser.add_argument('path', help='Path to the directory containing the submissions')
  args = parser.parse_args()

  AssignmentsRunner.AssignmentsRunner(args.path).run()
  
if __name__ == "__main__":
  cli()