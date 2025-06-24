# 개발자 본인 소개/PR 챗봇 메인 엔트리포인트
# 관심사 분리: context.py, tools.py, guardrails.py, agents.py 참고
# triage_agent를 엔트리포인트로 사용

from context import DeveloperProfileContext
from agents import triage_agent, about_me_agent, awards_agent, certifications_agent, portfolio_summary_agent, project_agent, experience_agent, strength_agent, tech_agent, faq_agent

# 예시: 새로운 대화 컨텍스트 생성
# 실제 서비스에서는 사용자별로 컨텍스트를 관리해야 함


def create_initial_context() -> DeveloperProfileContext:
    return DeveloperProfileContext()

# triage_agent를 통해 대화 시작/진행
# 예시:
# result = await triage_agent.run(input, context)

# 확장 가이드:
# - context.py: DeveloperProfileContext에 필드 추가/수정
# - tools.py: function_tool로 신규 툴 추가
# - guardrails.py: input_guardrail로 신규 가드레일 추가
# - agents.py: Agent 인스턴스 추가/수정/확장
