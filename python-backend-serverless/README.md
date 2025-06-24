# Customer Service Agents - Serverless Backend

이 폴더는 OpenAI Agents SDK를 사용한 고객 서비스 에이전트 백엔드의 **서버리스 버전**입니다.

## 🌟 주요 특징

- ✅ **서버리스 환경 최적화** (Vercel, AWS Lambda 등)
- ✅ **Redis 기반 상태 관리** (세션 지속성)
- ✅ **자동 폴백 시스템** (Redis 실패 시 InMemory)
- ✅ **헬스체크 엔드포인트** (웜업용)
- ✅ **환경변수 기반 설정**

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd python-backend-serverless
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 API 키와 Redis URL 설정
```

### 3. 로컬 실행

```bash
uvicorn api:app --reload --port 8000
```

## 🔧 배포 방법

### Vercel 배포

1. **Upstash Redis 설정**

   ```bash
   # upstash.com에서 무료 Redis 인스턴스 생성
   # Connection URL 복사
   ```

2. **Vercel CLI로 배포**

   ```bash
   npm i -g vercel
   vercel
   # 환경변수 설정
   vercel env add OPENAI_API_KEY
   vercel env add UPSTASH_REDIS_URL
   ```

3. **또는 GitHub 연동**
   - GitHub에 푸시
   - vercel.com에서 Import
   - 환경변수 설정

### Render 배포

1. **render.com에서 Web Service 생성**
2. **설정:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
3. **환경변수 추가:**
   - `OPENAI_API_KEY`
   - `UPSTASH_REDIS_URL`

### Railway 배포

```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway variables set OPENAI_API_KEY=your_key
railway variables set UPSTASH_REDIS_URL=your_redis_url
```

## 📊 Redis 서비스 옵션

### 무료 옵션

- **Upstash Redis** (추천): 10,000 commands/day 무료
- **Redis Cloud**: 30MB 무료
- **Railway Redis**: $5 크레딧으로 시작

### 유료 옵션

- **Upstash Pro**: 사용량 기반 (월 $1-5)
- **Railway Redis**: 월 $3-5
- **AWS ElastiCache**: 월 $15+

## 🔍 API 엔드포인트

### 주요 엔드포인트

- `POST /chat` - 대화 API
- `GET /health` - 헬스체크
- `GET /` - API 정보
- `GET /docs` - Swagger 문서

### 사용 예시

```bash
# 헬스체크
curl https://your-app.vercel.app/health

# 새 대화 시작
curl -X POST https://your-app.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "좌석을 변경하고 싶어요"}'

# 기존 대화 이어가기
curl -X POST https://your-app.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "abc123",
    "message": "14A로 바꿔주세요"
  }'
```

## 🏗️ 아키텍처

### 상태 관리

```
Client Request → FastAPI → Redis (상태 저장/조회) → OpenAI Agents → Response
```

### 폴백 시스템

```
Redis 연결 성공 ✅ → RedisConversationStore 사용
Redis 연결 실패 ❌ → InMemoryConversationStore 폴백
```

### TTL 관리

- 기본 TTL: 2시간
- 활성 대화 시 자동 연장
- 비활성 대화는 자동 정리

## 🔧 커스터마이징

### 새 에이전트 추가

1. `main.py`에서 에이전트 정의
2. `api.py`의 `_get_agent_by_name()`에 추가
3. `_build_agents_list()`에 포함

### TTL 변경

```python
# conversation_store.py에서
self.redis.setex(key, 3600, data)  # 1시간으로 변경
```

### CORS 설정

```python
# 환경변수로 제어
ALLOWED_ORIGINS=https://mydomain.com,https://anotherdomain.com
```

## 🐛 트러블슈팅

### Redis 연결 오류

```bash
# 연결 테스트
python -c "
import redis, os
from dotenv import load_dotenv
load_dotenv()
r = redis.Redis.from_url(os.getenv('UPSTASH_REDIS_URL'))
print(r.ping())
"
```

### 환경변수 확인

```bash
# 로컬에서
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

### 로그 확인

- Vercel: `vercel logs`
- Render: 웹 대시보드
- Railway: `railway logs`

## 📚 추가 리소스

- [OpenAI Agents SDK 문서](https://openai.github.io/openai-agents-python/)
- [Upstash Redis 문서](https://docs.upstash.com/redis)
- [Vercel Python 런타임](https://vercel.com/docs/functions/runtimes/python)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

## 🤝 기여

버그 신고나 기능 제안은 GitHub Issues를 통해 부탁드립니다.

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](../LICENSE) 파일을 참조하세요.
