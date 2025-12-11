# Incremental Commit System Guide

This system helps you automatically commit project changes incrementally to Git.

## 📋 Created Files

1. **`auto-commit.ps1`**: PowerShell script for Windows
2. **`auto-commit.sh`**: Bash script for Linux/Mac
3. **`.git/hooks/post-commit`**: Git hook that displays information after each commit

## 🚀 Usage

### Method 1: Manual Commit (One-time)

#### Windows (PowerShell):
```powershell
# Commit with default message
.\auto-commit.ps1

# Commit with custom message
.\auto-commit.ps1 -Message "Add new feature"

# Commit and push simultaneously
.\auto-commit.ps1 -Push

# Commit with message and push
.\auto-commit.ps1 -Message "Update" -Push
```

#### Linux/Mac (Bash):
```bash
# Grant execute permission
chmod +x auto-commit.sh

# Commit with default message
./auto-commit.sh

# Commit with custom message
./auto-commit.sh -m "Add new feature"

# Commit and push simultaneously
./auto-commit.sh -p

# Commit with message and push
./auto-commit.sh -m "Update" -p
```

### Method 2: Auto Commit (Continuous Monitoring)

This method automatically checks and commits changes every few seconds.

#### Windows:
```powershell
# Check every 30 seconds
.\auto-commit.ps1 -Interval 30

# Check every 60 seconds with auto push
.\auto-commit.ps1 -Interval 60 -Push
```

#### Linux/Mac:
```bash
# Check every 30 seconds
./auto-commit.sh -i 30

# Check every 60 seconds with auto push
./auto-commit.sh -i 60 -p
```

Press `Ctrl+C` to stop monitoring.

## 📝 Usage Examples

### Example 1: Commit after small changes
```powershell
# After each small code change, run this command
.\auto-commit.ps1 -Message "Code improvement"
```

### Example 2: Continuous monitoring during development
```powershell
# Run in a separate terminal
.\auto-commit.ps1 -Interval 120  # Checks every 2 minutes
```

### Example 3: Commit and push simultaneously
```powershell
.\auto-commit.ps1 -Message "Complete feature X" -Push
```

## ⚙️ Advanced Configuration

### Using Task Scheduler (Windows)

You can configure the script in Windows Task Scheduler to run automatically:

1. Open Task Scheduler
2. Select Create Basic Task
3. Set trigger to "When I log on" or "Daily"
4. Set action to "Start a program"
5. Program: `powershell.exe`
6. Arguments: `-File "C:\path\to\auto-commit.ps1" -Interval 300`

### Using Cron (Linux/Mac)

You can configure the script in crontab:

```bash
# Open crontab
crontab -e

# Add the following line to run every 5 minutes
*/5 * * * * cd /path/to/project && ./auto-commit.sh
```

## 🔍 Status Check

To check Git status:

```bash
# View changes
git status

# View commit history
git log --oneline -10

# View differences
git diff
```

## ⚠️ Important Notes

1. **Always check before committing**: Use `git status` to see which files will be committed.

2. **Use clear messages**: Even if using default messages, try to write custom messages sometimes.

3. **Push with caution**: Before pushing, make sure your changes are ready.

4. **Use .gitignore**: Place temporary and unnecessary files in `.gitignore`.

## 🛠️ Troubleshooting

### Issue: Script doesn't run

**Windows:**
```powershell
# Check Execution Policy
Get-ExecutionPolicy

# If it's Restricted, change it
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**
```bash
# Grant execute permission
chmod +x auto-commit.sh
```

### Issue: Git hook doesn't work

```bash
# Check file permissions
ls -la .git/hooks/post-commit

# Grant execute permission (Linux/Mac)
chmod +x .git/hooks/post-commit
```

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [PowerShell Scripting](https://docs.microsoft.com/powershell/)

---

**Note**: This system is designed to help with incremental commits. Always review changes before pushing to remote.
