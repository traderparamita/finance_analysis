#!/usr/bin/env bash
# bootstrap.sh — finance-analysis 플러그인 셋업 도우미
# - Python 3.10+ 확인
# - 가상환경 생성 (.venv)
# - 의존성 설치
# - 한글 폰트 가용성 점검
#
# 사용법:
#   ./bootstrap.sh
#
# 비대화형(자동 yes)으로 실행:
#   FINANCE_BOOTSTRAP_YES=1 ./bootstrap.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}ℹ${NC}  $*"; }
ok()      { echo -e "${GREEN}✓${NC}  $*"; }
warn()    { echo -e "${YELLOW}⚠${NC}  $*"; }
err()     { echo -e "${RED}✗${NC}  $*" >&2; }

# ── 1) Python 버전 확인 ────────────────────────────────
info "Python 3.10+ 확인 중..."
if ! command -v python3 >/dev/null 2>&1; then
    err "python3 명령을 찾을 수 없습니다. Python 3.10+ 설치 후 다시 시도하세요."
    exit 1
fi

PY_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJOR="$(python3 -c 'import sys; print(sys.version_info.major)')"
PY_MINOR="$(python3 -c 'import sys; print(sys.version_info.minor)')"

if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
    err "Python ${PY_VERSION} 발견 — 3.10 이상 필요"
    exit 1
fi
ok "Python ${PY_VERSION}"

# ── 2) 가상환경 생성 ────────────────────────────────────
if [[ -d .venv ]]; then
    info ".venv 이미 존재 — 스킵"
else
    info ".venv 가상환경 생성 중..."
    python3 -m venv .venv
    ok ".venv 생성 완료"
fi

# ── 3) 의존성 설치 ─────────────────────────────────────
info "requirements.txt 의존성 설치 중..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt
ok "의존성 설치 완료 (yfinance, reportlab, matplotlib, ...)"

# ── 4) 한글 폰트 점검 ───────────────────────────────────
info "한글 폰트 가용성 점검 중..."
FONT_FOUND=$(.venv/bin/python - <<'EOF' 2>/dev/null
import sys, os
sys.path.insert(0, os.getcwd())
from shared.pdf_utils import _FONT_REGISTERED, FONT
print(f"{_FONT_REGISTERED}|{FONT}")
EOF
)

REGISTERED="${FONT_FOUND%|*}"
FONT_NAME="${FONT_FOUND#*|}"

if [[ "$REGISTERED" == "True" ]]; then
    ok "한글 폰트 등록 (${FONT_NAME})"
else
    warn "한글 폰트를 찾지 못했습니다. PDF에서 한글이 깨질 수 있습니다."
    case "$(uname -s)" in
        Linux*)
            echo ""
            echo "  Linux 사용자: 다음 중 하나를 실행하세요:"
            echo "    sudo apt install fonts-noto-cjk-extra fonts-nanum"
            echo "    sudo dnf install google-noto-sans-cjk-fonts nanum-fonts"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo ""
            echo "  Windows 사용자: 보통 Malgun Gothic이 자동 설치되어 있습니다."
            echo "  못 찾을 경우 환경변수로 지정:"
            echo "    set FINANCE_KOREAN_FONT=C:\\path\\to\\font.ttf"
            ;;
        *)
            echo ""
            echo "  환경변수로 직접 지정 가능:"
            echo "    export FINANCE_KOREAN_FONT=/path/to/your-korean-font.ttf"
            ;;
    esac
fi

# ── 5) 셋업 완료 안내 ───────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════"
ok "셋업 완료!"
echo ""
echo "다음 명령으로 보고서를 생성할 수 있습니다:"
echo ""
echo "  ${BLUE}.venv/bin/python run.py 펨트론${NC}              # 풀 보고서"
echo "  ${BLUE}.venv/bin/python run.py 펨트론 --brief${NC}      # 1~2 페이지 브리프"
echo "  ${BLUE}.venv/bin/python run.py --all${NC}                # 모든 종목"
echo ""
echo "또는 Claude Code 안에서:"
echo "  ${BLUE}/finance-report 종목명${NC}"
echo "  ${BLUE}/finance-brief 종목명${NC}"
echo ""
echo "stocks/ 디렉토리는 ${BLUE}\$FINANCE_STOCKS_DIR${NC} 환경변수로 위치 변경 가능."
echo "════════════════════════════════════════════════════════"
