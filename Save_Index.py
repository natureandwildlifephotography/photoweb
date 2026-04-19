import subprocess

def save_to_github():
    try:
        # Initial status check
        print("Checking initial git status:")
        subprocess.run(["git", "status"], check=True)
        print("-" * 30)

        # Stage all modified files
        print("Executing: git add .")
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        print('Executing: git commit -m "Updated website files on GitHub"')
        subprocess.run(["git", "commit", "-m", "Updated website files on GitHub"], check=True)
        
        # Push to the remote repository
        print("Executing: git push")
        subprocess.run(["git", "push"], check=True)
        
        print("-" * 30)
        # Final status check
        print("Checking final git status:")
        subprocess.run(["git", "status"], check=True)

        print("\nSuccessfully pushed changes to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"\nError during git operations: {e}")

if __name__ == "__main__":
    save_to_github()
