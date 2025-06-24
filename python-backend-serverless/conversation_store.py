import redis
import json
import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class ConversationStore(ABC):
    """대화 상태 저장소의 추상 클래스"""

    @abstractmethod
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """대화 상태 조회"""
        pass

    @abstractmethod
    def save(self, conversation_id: str, state: Dict[str, Any]):
        """대화 상태 저장"""
        pass

    @abstractmethod
    def delete(self, conversation_id: str):
        """대화 상태 삭제"""
        pass


class RedisConversationStore(ConversationStore):
    """Redis 기반 대화 상태 저장소 - 서버리스 환경에 적합"""

    def __init__(self):
        redis_url = os.getenv("REDIS_URL") or os.getenv("UPSTASH_REDIS_URL")
        if not redis_url:
            raise ValueError(
                "Redis URL이 필요합니다. 환경변수 REDIS_URL 또는 UPSTASH_REDIS_URL을 설정해주세요."
            )

        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)

        # 연결 테스트
        try:
            self.redis.ping()
            print("✅ Redis 연결 성공")
        except Exception as e:
            print(f"❌ Redis 연결 실패: {e}")
            raise

    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """대화 상태 조회"""
        try:
            data = self.redis.get(f"conversation:{conversation_id}")
            if data:
                return json.loads(data)
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
        except Exception as e:
            print(f"Redis 조회 오류: {e}")
            return None

    def save(self, conversation_id: str, state: Dict[str, Any]):
        """대화 상태 저장 (2시간 TTL 설정)"""
        try:
            # 2시간 후 자동 삭제 (7200초)
            self.redis.setex(
                f"conversation:{conversation_id}",
                7200,  # 2시간 TTL
                json.dumps(state, default=str, ensure_ascii=False)
            )
        except Exception as e:
            print(f"Redis 저장 오류: {e}")

    def delete(self, conversation_id: str):
        """대화 상태 삭제"""
        try:
            self.redis.delete(f"conversation:{conversation_id}")
        except Exception as e:
            print(f"Redis 삭제 오류: {e}")

    def extend_ttl(self, conversation_id: str, ttl_seconds: int = 7200):
        """TTL 연장"""
        try:
            self.redis.expire(f"conversation:{conversation_id}", ttl_seconds)
        except Exception as e:
            print(f"TTL 연장 오류: {e}")


class InMemoryConversationStore(ConversationStore):
    """인메모리 대화 상태 저장소 - 개발/테스트용 폴백"""

    _conversations: Dict[str, Dict[str, Any]] = {}

    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        return self._conversations.get(conversation_id)

    def save(self, conversation_id: str, state: Dict[str, Any]):
        self._conversations[conversation_id] = state

    def delete(self, conversation_id: str):
        self._conversations.pop(conversation_id, None)


def create_conversation_store() -> ConversationStore:
    """환경에 따라 적절한 conversation store 생성"""
    try:
        return RedisConversationStore()
    except ValueError:
        print("⚠️  Redis가 설정되지 않았습니다. 인메모리 저장소를 사용합니다.")
        print("   프로덕션 환경에서는 REDIS_URL 또는 UPSTASH_REDIS_URL을 설정해주세요.")
        return InMemoryConversationStore()
    except Exception as e:
        print(f"⚠️  Redis 연결 실패: {e}")
        print("   인메모리 저장소로 폴백합니다.")
        return InMemoryConversationStore()
