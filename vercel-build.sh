#!/bin/sh
# Vercel(회사용) 배포 때만 실행됩니다. GitHub Pages(지인용)는 이 파일을 쓰지 않아요.
# 링크 미리보기(og:title)는 자바스크립트로 바꿀 수 없어서, 배포할 때 글자를 바꿔 넣습니다.
CO_TITLE="신예진 이석종 결혼합니다"   # 링크 미리보기 제목
CO_PAGE="예진 석종 청첩장"          # 브라우저 탭 · 홈 화면 이름
CO_SHORT="예진♥석종"                # 홈 화면 아이콘 아래 짧은 이름

set -e
rm -rf dist && mkdir dist
for f in *; do [ "$f" = dist ] || cp -r "$f" dist/; done
sed -i "s|<meta property=\"og:title\" content=\"[^\"]*\">|<meta property=\"og:title\" content=\"$CO_TITLE\">|" dist/index.html
grep -q "content=\"$CO_TITLE\"" dist/index.html
sed -i "s|<title>[^<]*</title>|<title>$CO_PAGE</title>|" dist/index.html
sed -i "s|\"name\": \"[^\"]*\"|\"name\": \"$CO_PAGE\"|; s|\"short_name\": \"[^\"]*\"|\"short_name\": \"$CO_SHORT\"|" dist/manifest.webmanifest
grep -q "<title>$CO_PAGE</title>" dist/index.html
grep -q "\"name\": \"$CO_PAGE\"" dist/manifest.webmanifest
