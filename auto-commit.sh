#!/bin/bash
# اسکریپت commit خودکار برای به‌روزرسانی تدریجی پروژه (Linux/Mac)
# این اسکریپت تغییرات را به صورت خودکار commit می‌کند

MESSAGE=""
PUSH=false
INTERVAL=0

# پارس کردن آرگومان‌ها
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
            echo "استفاده: $0 [-m MESSAGE] [-p] [-i INTERVAL]"
            exit 1
            ;;
    esac
done

# تابع برای بررسی تغییرات
check_changes() {
    git status --porcelain | grep -q .
}

# تابع برای ایجاد پیام commit
get_commit_message() {
    if [ -n "$MESSAGE" ]; then
        echo "$MESSAGE"
        return
    fi
    
    FILES=$(git status --short | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "Auto-commit: تغییرات در $FILES - $TIMESTAMP"
}

# تابع برای commit تغییرات
commit_changes() {
    echo "در حال بررسی تغییرات..."
    
    if ! check_changes; then
        echo "هیچ تغییراتی برای commit وجود ندارد."
        return 1
    fi
    
    echo "تغییرات پیدا شد. در حال commit..."
    
    # اضافه کردن تمام تغییرات
    git add -A
    
    # ایجاد commit
    COMMIT_MSG=$(get_commit_message)
    git commit -m "$COMMIT_MSG"
    
    if [ $? -eq 0 ]; then
        echo "✓ Commit با موفقیت انجام شد: $COMMIT_MSG"
        
        if [ "$PUSH" = true ]; then
            echo "در حال push به remote..."
            git push
            if [ $? -eq 0 ]; then
                echo "✓ Push با موفقیت انجام شد."
            else
                echo "✗ خطا در push."
            fi
        fi
        
        return 0
    else
        echo "✗ خطا در commit."
        return 1
    fi
}

# اجرای اصلی
if [ "$INTERVAL" -gt 0 ]; then
    echo "حالت نظارت فعال شد. هر $INTERVAL ثانیه یکبار بررسی می‌شود..."
    echo "برای توقف، Ctrl+C را فشار دهید."
    echo ""
    
    while true; do
        commit_changes
        sleep "$INTERVAL"
    done
else
    commit_changes
fi

