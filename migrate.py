#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Migration Management Script
سكريبت إدارة Migrations لقاعدة البيانات
"""
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run alembic command"""
    alembic_path = Path(__file__).parent / "venv" / "Scripts" / "alembic.exe"
    full_cmd = [str(alembic_path)] + cmd
    result = subprocess.run(full_cmd, cwd=Path(__file__).parent)
    return result.returncode

def show_help():
    """Show help message"""
    print("=" * 60)
    print("🗄️  Database Migration Manager - إدارة Migrations")
    print("=" * 60)
    print()
    print("الاستخدام:")
    print("  python migrate.py <command>")
    print()
    print("الأوامر المتاحة:")
    print("  create <message>  - إنشاء migration جديد")
    print("  upgrade           - تطبيق جميع migrations")
    print("  downgrade         - التراجع عن آخر migration")
    print("  current           - عرض الإصدار الحالي")
    print("  history           - عرض تاريخ migrations")
    print("  help              - عرض هذه الرسالة")
    print()
    print("أمثلة:")
    print("  python migrate.py create 'Add user profile table'")
    print("  python migrate.py upgrade")
    print("  python migrate.py downgrade")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ خطأ: يجب تحديد رسالة للـ migration")
            print("مثال: python migrate.py create 'Add new table'")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        print(f"📝 إنشاء migration جديد: {message}")
        return run_command(["revision", "--autogenerate", "-m", message])
    
    elif command == "upgrade":
        print("⬆️  تطبيق migrations...")
        return run_command(["upgrade", "head"])
    
    elif command == "downgrade":
        print("⬇️  التراجع عن آخر migration...")
        return run_command(["downgrade", "-1"])
    
    elif command == "current":
        print("📍 الإصدار الحالي:")
        return run_command(["current"])
    
    elif command == "history":
        print("📜 تاريخ Migrations:")
        return run_command(["history"])
    
    else:
        print(f"❌ أمر غير معروف: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
