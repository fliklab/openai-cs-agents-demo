# Customer Service Agents - Serverless Redis Demo

A fork of OpenAI's Customer Service Agents Demo, restructured with serverless architecture and Redis state management.

## Redis

This project uses Redis for state management instead of in-memory state. Using Redis provides the following benefits:

- State persistence in serverless environments
- State sharing between multiple instances
- Permanent data storage
- Scalable architecture

---

## 🏗️ 프로젝트 구성

### **백엔드 구조**

```
python-backend-serverless/
├── api.py                   # FastAPI 메인 애플리케이션
├── main.py                  # AI 에이전트 정의 (318줄)
├── conversation_store.py    # Redis/InMemory 상태 관리
├── requirements.txt         # 의존성 패키지
├── vercel.json             # Vercel 배포 설정
├── test_redis.py           # Redis 연결 테스트
└── README.md               # 문서
```

### **프론트엔드 구조**

```
ui/
├── app/                    # Next.js 애플리케이션
├── components/             # React 컴포넌트
│   ├── Chat.tsx           # 채팅 인터페이스
│   ├── agent-panel.tsx    # 에이전트 상태 패널
│   └── seat-map.tsx       # 좌석 선택 지도
└── lib/                   # 유틸리티 함수
```

## 🤖 AI 에이전트 시스템

### **5개의 전문 에이전트**

#### **1. Triage Agent (접수 담당)**

- 고객 문의를 분석하여 적절한 전문 에이전트로 라우팅
- 모든 대화의 시작점 및 중앙 허브 역할

#### **2. Seat Booking Agent (좌석 예약)**

- 좌석 변경 및 예약 처리
- 대화형 좌석 지도 표시 (`display_seat_map`)
- 확인번호 기반 좌석 업데이트

#### **3. Flight Status Agent (항공편 현황)**

- 실시간 항공편 정보 조회
- 게이트 정보, 출발 시간 등 제공

#### **4. FAQ Agent (자주 묻는 질문)**

- 수하물 규정, WiFi, 좌석 정보 등 안내
- 하드코딩된 지식베이스 활용

#### **5. Cancellation Agent (항공편 취소)**

- 항공편 취소 처리
- 확인번호 및 항공편 번호 검증

### **보안 시스템**

- **Relevance Guardrail**: 항공사 관련 질문만 허용
- **Jailbreak Guardrail**: 시스템 프롬프트 우회 시도 차단

## 🛠️ 핵심 기능

### **상태 관리**

- **Redis 기반**: 서버리스 환경에서 세션 지속성
- **자동 폴백**: Redis 실패 시 InMemory로 자동 전환
- **TTL 관리**: 세션 만료 및 자동 정리

### **대화 컨텍스트**

```python
class AirlineAgentContext:
    passenger_name: str | None
    confirmation_number: str | None
    seat_number: str | None
    flight_number: str | None
    account_number: str | None
```

### **도구 (Tools)**

- `faq_lookup_tool`: FAQ 검색
- `update_seat`: 좌석 변경
- `flight_status_tool`: 항공편 조회
- `baggage_tool`: 수하물 정보
- `display_seat_map`: 좌석 지도 표시
- `cancel_flight`: 항공편 취소

## 🚀 배포 및 실행

### **로컬 개발**

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env

# 서버 실행
uvicorn api:app --reload --port 8000
```

### **Vercel 배포**

```bash
# Vercel CLI로 배포
vercel

# 환경변수 설정
vercel env add OPENAI_API_KEY
vercel env add UPSTASH_REDIS_URL
```

### **환경변수**

- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `UPSTASH_REDIS_URL`: Redis 연결 URL (선택사항)
- `ALLOWED_ORIGINS`: CORS 허용 도메인

## 📊 지식베이스

### **하드코딩된 데이터**

현재 모든 지식은 코드(python-backend-serverless/main.py)에 하드코딩되어 있습니다:

- **수하물 규정**: 50파운드, 22x14x9인치 제한
- **좌석 정보**: 120석 (비즈니스 22석, 이코노미 98석)
- **WiFi**: 무료 "Airline-Wifi" 네트워크
- **수하물 요금**: 초과중량 $75
- **항공편 정보**: 가짜 데이터 (게이트 A10 등)

### **개선 포인트**

- 실제 데이터베이스 연동 필요
- 외부 API 통합 (실제 항공편 정보)
- 동적 지식베이스 관리 시스템

## 🌐 API 엔드포인트

- **POST /chat**: 채팅 메시지 처리
- **GET /health**: 서버 상태 확인
- **GET /**: API 정보
- **GET /docs**: OpenAPI 문서

## ⚡ 서버리스 최적화

- **콜드 스타트 최소화**: 필수 임포트만 로드
- **상태 지속성**: Redis를 통한 세션 유지
- **자동 확장**: Vercel의 서버리스 함수 활용
- **글로벌 배포**: 엣지 로케이션 지원
