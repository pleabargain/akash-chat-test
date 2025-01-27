import subprocess
import sys
import os

def run_command(command):
    """Execute a git command and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        return None

def check_git_repo():
    """Check if current directory is a git repository."""
    if not os.path.exists('.git'):
        print("Error: Not a git repository")
        sys.exit(1)

def get_current_branch():
    """Get the name of the current branch."""
    return run_command("git rev-parse --abbrev-ref HEAD")

def get_all_branches():
    """Get list of all branches."""
    branches = run_command("git branch")
    if branches:
        return [b.strip('* ') for b in branches.split('\n')]
    return []

def has_uncommitted_changes():
    """Check for uncommitted changes."""
    status = run_command("git status --porcelain")
    return bool(status)

def fetch_latest():
    """Fetch latest changes from remote."""
    print("Fetching latest changes from remote...")
    run_command("git fetch --all")

def merge_branches(source_branch, target_branch):
    """Merge source branch into target branch."""
    current = get_current_branch()
    
    # Checkout target branch
    print(f"Checking out {target_branch}...")
    if run_command(f"git checkout {target_branch}") is None:
        print(f"Error: Could not checkout {target_branch}")
        return False
    
    # Pull latest changes
    print(f"Pulling latest changes for {target_branch}...")
    if run_command(f"git pull origin {target_branch}") is None:
        print(f"Error: Could not pull latest changes for {target_branch}")
        return False
    
    # Merge source branch
    print(f"Merging {source_branch} into {target_branch}...")
    merge_result = run_command(f"git merge {source_branch}")
    
    if merge_result is None:
        print("Merge conflict detected!")
        print("\nTo resolve conflicts:")
        print("1. Fix conflicts in conflicted files")
        print("2. git add <resolved-files>")
        print("3. git commit -m 'Merge conflict resolved'")
        print("4. git push origin", target_branch)
        return False
    
    # Push changes
    print("Pushing changes...")
    if run_command(f"git push origin {target_branch}") is None:
        print(f"Error: Could not push to {target_branch}")
        return False
    
    # Return to original branch
    if current != target_branch:
        print(f"Returning to {current}...")
        run_command(f"git checkout {current}")
    
    return True

def main():
    check_git_repo()
    
    # Check for uncommitted changes
    if has_uncommitted_changes():
        print("Error: You have uncommitted changes. Please commit or stash them first.")
        sys.exit(1)
    
    # Fetch latest changes
    fetch_latest()
    
    # Get branches
    branches = get_all_branches()
    if not branches:
        print("Error: No branches found")
        sys.exit(1)
    
    # Print available branches
    print("\nAvailable branches:")
    for i, branch in enumerate(branches, 1):
        print(f"{i}. {branch}")
    
    # Get source branch
    while True:
        try:
            source_idx = int(input("\nEnter number of source branch to merge from: ")) - 1
            if 0 <= source_idx < len(branches):
                source_branch = branches[source_idx]
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Get target branch
    while True:
        try:
            target_idx = int(input("Enter number of target branch to merge into: ")) - 1
            if 0 <= target_idx < len(branches) and target_idx != source_idx:
                target_branch = branches[target_idx]
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Confirm merge
    print(f"\nReady to merge '{source_branch}' into '{target_branch}'")
    confirm = input("Continue? (y/n): ").lower()
    
    if confirm != 'y':
        print("Merge cancelled")
        sys.exit(0)
    
    # Perform merge
    if merge_branches(source_branch, target_branch):
        print(f"\nSuccessfully merged {source_branch} into {target_branch}")
    else:
        print("\nMerge was not completed. Please resolve any conflicts and try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
