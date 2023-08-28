import os
from ai_assignment_marker.AssignmentMarker import AssignmentMarker

class AssignmentsRunner:
    def __init__(self, assignments_path):
        self.assignments_path = assignments_path

    def run(self):
        for assignment in self.get_assignments():
            print(f"Running assignment {assignment}...")

            AssignmentMarker(assignment).process()

            print(f"Completed assignment {assignment}.")

    def get_assignments(self):
        
        return [os.path.join(self.assignments_path, file) for file in os.listdir(self.assignments_path)]