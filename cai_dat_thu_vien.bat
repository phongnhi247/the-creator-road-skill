@echo off
chcp 65001 >nul
echo ============================================================
echo   Đang tự động cài đặt thư viện cho The Creator Road...
echo ============================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Máy tính của bạn chưa cài đặt Python hoặc chưa bật "Add Python to PATH"!
    echo Vui lòng tải và cài đặt Python từ https://www.python.org/downloads/
    echo (Nhớ tích chọn "Add python.exe to PATH" khi cài).
    echo.
    pause
    exit /b 1
)

pip install -r requirements.txt

echo.
echo ============================================================
echo   HOÀN TẤT CÀI ĐẶT! Bạn có thể sử dụng bộ công cụ ngay.
echo ============================================================
pause
