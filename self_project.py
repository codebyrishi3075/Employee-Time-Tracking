import time
from datetime import datetime
from copy import copy, deepcopy

class BudgetExceededException(Exception):
    pass

def log_update_message(function_name):
    timing = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG {timing}] Updating data via {function_name}")


class Project:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget

        self.total_hours = 0
        self.employees = {}

    def add_hours(self, employee, hours):
        if employee in self.employees:
            self.employees[employee] += hours
        else:
            self.employees[employee] = hours
        self.total_hours += hours

    def is_greater_than(self, other):
        return self.total_hours > other.total_hours
    
    def display(self):
        return f"Project({self.name}, {self.total_hours}h)"
    


class EmployeeProjectTracker:
    def __init__(self):
        self.projects = {}
        self.project_names = set()

    def add_entry(self, employee, project_name, hours, budget=150):
        log_update_message("add_entry")

        self.project_names.add(project_name)

        if project_name not in self.projects:
            self.projects[project_name] = Project(project_name, budget)

        self.projects[project_name].add_hours(employee, hours)

    def add_multiple_entries(self, *args, **kwargs):
        for i in range(0, len(args), 3):
            if i + 2 < len(args):
                self.add_entry(args[i], args[i+1], args[i+2], **kwargs)

    def get_sorted_projects(self):
        sorted_projects = sorted(
            self.projects.items(), 
            key=lambda x: x[1].total_hours,
            reverse= True
        )
        return [(name, proj.total_hours) for name, proj in sorted_projects]
    
    def project_summary_generator(self):
        for name, project in self.projects.items():
            status = 'BUDGET EXCEEDED' if project.total_hours > project.budget else 'Within Budget'
            yield f'Project: {name} | Total Hours: {project.total_hours} | {status}'
    def check_budget_recursive(self, project_name, employee_list, index=0, accumulated_hours=0):
        if index >= len(employee_list):
            return None
        
        employee, hours = employee_list[index]
        new_accumulated_hours = accumulated_hours + hours
        project = self.projects[project_name]

        if new_accumulated_hours > project.budget and accumulated_hours <= project.budget:
            return employee
        
        return self.check_budget_recursive(project_name, employee_list, index + 1, new_accumulated_hours)
    def get_suggestion(self):
        for proj_name, project in self.projects.items():
            if project.total_hours > project.budget:

                emp_list = sorted(project.employees.items(), key=lambda x: x[1], reverse=True)
                violating_emp = self.check_budget_recursive(proj_name, emp_list)

                if violating_emp:
                    target_project = min(self.projects.items(), key=lambda x: x[1].total_hours)
                    return violating_emp, proj_name, target_project[0]
        return None, None, None
    
    def demonstrate_copy(self):
        print('\n--- COPY DEMONSTRATION ---')

        original = self.projects

        shallow = copy(original)
        print('Shallow copy created - references same Project objects')

        deep = deepcopy(original)
        print('Deep copy created - independent Project objects')
        print("Snapshot Saved (Deep Copy)")

        return deep
    

    def compare_projects(self, proj1_name, proj2_name):
        if proj1_name in self.projects and proj2_name in self.projects:
            proj1 =  self.projects[proj1_name]
            proj2 =  self.projects[proj2_name]
            return proj1.is_greater_than(proj2)
        return None
    

# Take Dynamic Input From The User
def get_user_input():
    print('=== EMPLOYEE PROJECT COST TRACKER ===\n')
    tracker = EmployeeProjectTracker()
    while True:
        print("\n--- MENU ---")
        print("1. Add Employee Entry")
        print("2. View Project Summary")
        print("3. View Sorted Projects (by workload)")
        print("4. Get Reassignment Suggestion")
        print("5. Demonstrate Copy Behavior")
        print("6. Show All Features & Exit")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            try:
                employee = input("Enter Employee Name: ").strip()
                project = input("Enter Project Name: ").strip()
                hours = int(input("Enter Hours Worked: ").strip())
                
                budget_input = input("Enter Project Budget (press Enter for default 150): ").strip()
                budget = int(budget_input) if budget_input else 150
                
                tracker.add_entry(employee, project, hours, budget)
                print(f"✓ Entry added: {employee} -> {project} ({hours}h)")
                
            except ValueError:
                print("Invalid Input! Please Enter Number For Hours And Budget.")
            
        elif choice == "2":
            if not tracker.projects:
                print('No Data Available. Please Add Entry First.')
            else:
                print("\n----PROJECT SUMMARY----")
                for summary in tracker.project_summary_generator():
                    print(summary)
        elif choice == "3":
            if not tracker.projects:
                print("No Data Available! Please Add Entry First.")
            else:
                print("\nSorted by workload (High → Low):")
                sorted_projs = tracker.get_sorted_projects()
                print(sorted_projs)
        elif choice == "4":
            if not tracker.projects:
                print("No Data Available! Please Add Entry First.")
            else:
                emp, from_proj, to_proj = tracker.get_suggestion()
                if emp:
                    print(f'\n✓ Suggestion: Move Employee "{emp}" from {from_proj} to {to_proj}')
                else:
                    print("All Project Are Within The Budget")
        
        elif choice == "5":
            if not tracker.projects:
                print("No Data Available! Please Add Entry First.")
            else:
                tracker.demonstrate_copy()
        elif choice == "6":
            if not tracker.projects:
                print("No Data Available! Please Add Entry First.")
            else:
                display_all_features(tracker)
                break
        
        elif choice == '0':
            print("\n👋 Exiting... Thank you!")
            break
        
        else:
            print("Please! Enter The Valid Options & Try Again.")

def display_all_features(tracker):
    print("\n" + "="*50)
    print("--- PROJECT SUMMARY ---")
    for summary in tracker.project_summary_generator():
        print(summary)

    emp, from_proj, to_proj = tracker.get_suggestion()
    if emp:
        print(f'\nSuggestion: Move Employee "{emp}" from {from_proj} to {to_proj}')

    print("\nSorted by workload (High → Low):")
    sorted_projs = tracker.get_sorted_projects()
    print(sorted_projs)
    
    tracker.demonstrate_copy()
    
    print("\n--- PROJECT COMPARISON DEMO ---")
    proj_list = list(tracker.projects.keys())
    if len(proj_list) >= 2:
        result = tracker.compare_projects(proj_list[0], proj_list[1])
        print(f"{proj_list[0]} has more hours than {proj_list[1]}? {result}")
    
    print("\n--- NESTED DICTIONARY (Comprehension) ---")
    summary_dict = {
        proj_name: {
            'total_hours': proj.total_hours,
            'employees': proj.employees,
            'budget_status': "EXCEEDED" if proj.total_hours > proj.budget else 'OK'
        }
        for proj_name, proj in tracker.projects.items()
    }
    for proj, details in summary_dict.items():
        print(f"{proj}: {details['total_hours']}h - Status: {details['budget_status']}")
    
    print("\n--- PROJECTS EXCEEDING BUDGET (Set Comprehension) ---")
    exceeded = {proj_name for proj_name, proj in tracker.projects.items() 
                if proj.total_hours > proj.budget}
    print(exceeded if exceeded else "None")
    print("="*50)
def demo_mode():
    print("=== RUNNING IN DEMO MODE ===\n")
    tracker = EmployeeProjectTracker()
    
    tracker.add_entry("Alice", "AI Automation", 45, budget=150)
    tracker.add_entry("Bob", "AI Automation", 52, budget=150)
    tracker.add_entry("Sourav", "AI Automation", 95, budget=150)
    
    tracker.add_entry("Charlie", "Backend Refactor", 60, budget=140)
    tracker.add_entry("Dave", "Backend Refactor", 60, budget=140)
    
    tracker.add_entry("Eve", "UI Revamp", 50, budget=100)
    tracker.add_entry("Frank", "UI Revamp", 45, budget=100)

    display_all_features(tracker)

def main():
    print('Choose Mode: ')
    print("1. Interactive Mode (User Input)")
    print("2. Demo Mode (Pre-filled Data)")

    mode = input("\nEnter Choice (1 or 2): ").strip()

    if mode == '1':
        get_user_input()
    elif mode == '2':
        demo_mode()
    else:
        print('Invalid Choice! Running Demo Made Default.')
        demo_mode()


if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
                    


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            