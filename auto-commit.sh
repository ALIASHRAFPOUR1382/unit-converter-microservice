#!/bin/bash
# Auto-commit script for gradual project updates (Linux/Mac)
# This script automatically commits changes

MESSAGE=""
PUSH=false
INTERVAL=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--message)
            MESSAGE="$2"
            shift 2
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [-m MESSAGE] [-p] [-i INTERVAL]"
            exit 1
            ;;
    esac
done

# Function to check for changes
check_changes() {
    git status --porcelain | grep -q .
}

# Function to generate commit message
get_commit_message() {
    if [ -n "$MESSAGE" ]; then
        echo "$MESSAGE"
        return
    fi
    
    FILES=$(git status --short | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "Auto-commit: Changes in $FILES - $TIMESTAMP"
}

# Function to commit changes
commit_changes() {
    echo "Checking for changes..."
    
    if ! check_changes; then
        echo "No changes to commit."
        return 1
    fi
    
    echo "Changes found. Committing..."
    
    # Add all changes
    git add -A
    
    # Create commit
    COMMIT_MSG=$(get_commit_message)
    git commit -m "$COMMIT_MSG"
    
    if [ $? -eq 0 ]; then
        echo "Commit successful: $COMMIT_MSG"
        
        if [ "$PUSH" = true ]; then
            echo "Pushing to remote..."
            git push
            if [ $? -eq 0 ]; then
                echo "Push successful."
            else
                echo "Push failed."
            fi
        fi
        
        return 0
    else
        echo "Commit failed."
        return 1
    fi
}

# Main execution
if [ "$INTERVAL" -gt 0 ]; then
    echo "Monitoring mode activated. Checking every $INTERVAL seconds..."
    echo "Press Ctrl+C to stop."
    echo ""
    
    while true; do
        commit_changes
        sleep "$INTERVAL"
    done
else
    commit_changes
fi
