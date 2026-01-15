import os
import sys

def reset_memory():
    state_file = "state.json"
    if os.path.exists(state_file):
        print(f"Deleting {state_file}...")
        os.remove(state_file)
        print("✅ Memory reset successfully. The agent will re-discover all insights on the next run.")
    else:
        print(f"ℹ️ {state_file} not found. Memory is already fresh (or in a different directory).")

    # Also check if running from within src
    if os.path.exists(os.path.join("src", state_file)):
        print(f"Deleting src/{state_file}...")
        os.remove(os.path.join("src", state_file))
        print("✅ Memory reset successfully.")

if __name__ == "__main__":
    reset_memory()
