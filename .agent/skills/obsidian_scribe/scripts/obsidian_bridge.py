import os
import sys
import subprocess
import json

# --- CONFIGURATION ---
# 1. The absolute path to your Obsidian Vault (The Destination)
VAULT_PATH = os.path.expanduser("~/Documents/My SRE Vault")

# 2. The command to run your Gemini Agent.
AGENT_COMMAND = ["gemini"]

def main():
    # 1. Validation: Ensure we actually got the payload
    if len(sys.argv) < 2:
        print("Error: No JSON payload provided to the bridge script.")
        sys.exit(1)

    payload = sys.argv[1]

    # 2. Validation: Ensure the Vault exists
    if not os.path.exists(VAULT_PATH):
        print(f"Error: Obsidian Vault path not found at {VAULT_PATH}")
        sys.exit(1)

    # 3. Construct the "Context Injection" Prompt
    # We wrap the raw JSON in a clear natural language wrapper for the Scribe Agent
    scribe_prompt = (
        f"Incoming Task from Main Agent.\n"
        f"PAYLOAD: {payload}\n\n"
        f"INSTRUCTIONS: You are the Obsidian Scribe. Read 'GEMINI.md' in this directory "
        f"for rules. Process this payload immediately."
    )

    # 4. Build the command
    # Result: gemini "Incoming Task..."
    full_command = AGENT_COMMAND + [scribe_prompt]

    print(f"🌉 Bridge active. Teleporting agent to: {VAULT_PATH}...")

    try:
        # 5. EXECUTE THE AGENT
        # cwd=VAULT_PATH is the critical part that switches the context
        result = subprocess.run(
            full_command,
            cwd=VAULT_PATH,     # <--- The Magic: Runs inside the Vault
            capture_output=True,
            text=True
        )

        # 6. Return the Agent's Output to Antigravity
        if result.returncode == 0:
            print("\n✅ Scribe Agent Success:")
            print(result.stdout)
        else:
            print("\n❌ Scribe Agent Failed:")
            print(result.stderr)
            print(result.stdout)

    except Exception as e:
        print(f"Critical Bridge Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
