#!/usr/bin/env python3
"""
Redis 연결 테스트 스크립트
서버리스 배포 전에 Redis 설정이 올바른지 확인합니다.
"""

import os
import sys
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


def test_redis_connection():
    """Redis 연결 테스트"""
    print("🔍 Redis 연결 테스트 시작...")

    try:
        import redis
    except ImportError:
        print("❌ redis 패키지가 설치되지 않았습니다.")
        print("   pip install redis 로 설치해주세요.")
        return False

    # Redis URL 확인
    redis_url = os.getenv("REDIS_URL") or os.getenv("UPSTASH_REDIS_URL")
    if not redis_url:
        print("❌ Redis URL이 설정되지 않았습니다.")
        print("   환경변수 REDIS_URL 또는 UPSTASH_REDIS_URL을 설정해주세요.")
        return False

    print(f"📡 Redis URL: {redis_url[:30]}...")

    try:
        # Redis 연결
        r = redis.Redis.from_url(redis_url, decode_responses=True)

        # Ping 테스트
        result = r.ping()
        if result:
            print("✅ Redis 연결 성공!")
        else:
            print("❌ Redis ping 실패")
            return False

        # 기본 읽기/쓰기 테스트
        test_key = "test:connection"
        test_value = "hello_redis"

        # 쓰기 테스트
        r.setex(test_key, 60, test_value)
        print("✅ Redis 쓰기 테스트 성공")

        # 읽기 테스트
        retrieved = r.get(test_key)
        if retrieved == test_value:
            print("✅ Redis 읽기 테스트 성공")
        else:
            print(f"❌ Redis 읽기 테스트 실패: 예상 '{test_value}', 실제 '{retrieved}'")
            return False

        # 정리
        r.delete(test_key)
        print("✅ 테스트 데이터 정리 완료")

        return True

    except redis.ConnectionError as e:
        print(f"❌ Redis 연결 오류: {e}")
        print("   Redis URL이 올바른지 확인해주세요.")
        return False
    except redis.AuthenticationError as e:
        print(f"❌ Redis 인증 오류: {e}")
        print("   Redis 비밀번호가 올바른지 확인해주세요.")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False


def test_conversation_store():
    """ConversationStore 테스트"""
    print("\n🔍 ConversationStore 테스트 시작...")

    try:
        from conversation_store import create_conversation_store

        # 스토어 생성
        store = create_conversation_store()
        print(f"✅ ConversationStore 생성 성공: {type(store).__name__}")

        # 테스트 데이터
        test_conversation_id = "test_conversation_123"
        test_state = {
            "input_items": [
                {"content": "테스트 메시지", "role": "user"},
                {"content": "테스트 응답", "role": "assistant"}
            ],
            "context": {"test": "data"},
            "current_agent": "test_agent"
        }

        # 저장 테스트
        store.save(test_conversation_id, test_state)
        print("✅ 상태 저장 테스트 성공")

        # 조회 테스트
        retrieved_state = store.get(test_conversation_id)
        if retrieved_state:
            print("✅ 상태 조회 테스트 성공")

            # 데이터 일치 확인
            if retrieved_state.get("current_agent") == "test_agent":
                print("✅ 데이터 일치 확인 성공")
            else:
                print("❌ 데이터 불일치 발견")
                return False
        else:
            print("❌ 상태 조회 실패")
            return False

        # 정리
        if hasattr(store, 'delete'):
            store.delete(test_conversation_id)
            print("✅ 테스트 데이터 정리 완료")

        return True

    except Exception as e:
        print(f"❌ ConversationStore 테스트 실패: {e}")
        return False


def test_environment():
    """환경변수 테스트"""
    print("\n🔍 환경변수 테스트 시작...")

    # OpenAI API 키 확인
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...")
    else:
        print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   실제 배포 시에는 필수입니다.")

    # Redis URL 확인
    redis_url = os.getenv("REDIS_URL") or os.getenv("UPSTASH_REDIS_URL")
    if redis_url:
        print(f"✅ Redis URL: {redis_url[:30]}...")
    else:
        print("⚠️  Redis URL이 설정되지 않았습니다.")
        print("   서버리스 환경에서는 권장됩니다.")

    # CORS 설정 확인
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    print(f"✅ ALLOWED_ORIGINS: {allowed_origins}")

    return True


def main():
    """메인 테스트 실행"""
    print("🚀 서버리스 백엔드 설정 테스트")
    print("=" * 50)

    tests = [
        ("환경변수", test_environment),
        ("Redis 연결", test_redis_connection),
        ("ConversationStore", test_conversation_store),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 오류: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약:")

    all_passed = True
    for test_name, passed in results:
        status = "✅ 성공" if passed else "❌ 실패"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 모든 테스트 통과! 서버리스 배포 준비 완료.")
        return 0
    else:
        print("\n⚠️  일부 테스트 실패. 설정을 확인해주세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
