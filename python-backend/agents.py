from agents import Agent, handoff, RunContextWrapper
from context import DeveloperProfileContext
from tools import (
    about_me, list_awards, list_certifications, summarize_portfolio,
    list_projects, list_experiences, describe_strengths, show_tech_stack, show_portfolio, faq_lookup_tool
)
from guardrails import relevance_guardrail, jailbreak_guardrail

# 자기소개 에이전트
about_me_agent = Agent[DeveloperProfileContext](
    name="자기소개 에이전트",
    model="gpt-4.1",
    handoff_description="개발자 본인의 자기소개를 제공합니다.",
    instructions="""
    당신은 개발자 본인의 자기소개를 자연스럽게 설명하는 에이전트입니다.
    """,
    tools=[about_me],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 수상경력 에이전트
awards_agent = Agent[DeveloperProfileContext](
    name="수상경력 에이전트",
    model="gpt-4.1",
    handoff_description="수상경력 목록을 제공합니다.",
    instructions="""
    당신은 개발자 본인의 수상경력을 소개하는 에이전트입니다.
    """,
    tools=[list_awards],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 자격증 에이전트
certifications_agent = Agent[DeveloperProfileContext](
    name="자격증 에이전트",
    model="gpt-4.1",
    handoff_description="자격증 목록을 제공합니다.",
    instructions="""
    당신은 개발자 본인의 자격증을 소개하는 에이전트입니다.
    """,
    tools=[list_certifications],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 포트폴리오 요약 에이전트
portfolio_summary_agent = Agent[DeveloperProfileContext](
    name="포트폴리오 요약 에이전트",
    model="gpt-4.1",
    handoff_description="포트폴리오 전체를 간단히 요약합니다.",
    instructions="""
    당신은 개발자 본인의 포트폴리오 전체를 간단히 요약해주는 에이전트입니다.
    """,
    tools=[summarize_portfolio],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 프로젝트 설명 에이전트
project_agent = Agent[DeveloperProfileContext](
    name="프로젝트 설명 에이전트",
    model="gpt-4.1",
    handoff_description="주요 프로젝트를 소개합니다.",
    instructions="""
    당신은 개발자 본인의 주요 프로젝트를 상세히 소개하는 에이전트입니다.
    """,
    tools=[list_projects],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 경력/회사 설명 에이전트
experience_agent = Agent[DeveloperProfileContext](
    name="경력 설명 에이전트",
    model="gpt-4.1",
    handoff_description="경력 및 근무한 회사 정보를 설명합니다.",
    instructions="""
    당신은 개발자 본인의 경력과 일한 회사, 직무를 소개하는 에이전트입니다.
    """,
    tools=[list_experiences],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 성격/강점 에이전트
strength_agent = Agent[DeveloperProfileContext](
    name="강점/성격 에이전트",
    model="gpt-4.1",
    handoff_description="성격적 강점과 협업 스타일을 설명합니다.",
    instructions="""
    당신은 개발자 본인의 성격적 강점, 협업 스타일, 장점을 소개하는 에이전트입니다.
    """,
    tools=[describe_strengths],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 기술스택/포트폴리오 에이전트
tech_agent = Agent[DeveloperProfileContext](
    name="기술스택/포트폴리오 에이전트",
    model="gpt-4.1",
    handoff_description="주요 기술스택과 포트폴리오를 소개합니다.",
    instructions="""
    당신은 개발자 본인의 기술스택과 포트폴리오, 깃허브를 소개하는 에이전트입니다.
    """,
    tools=[show_tech_stack, show_portfolio],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# FAQ/자유질문 에이전트
faq_agent = Agent[DeveloperProfileContext](
    name="FAQ 에이전트",
    model="gpt-4.1",
    handoff_description="개발자 본인에 대해 자주 묻는 질문에 답변합니다.",
    instructions="""
    당신은 개발자 본인에 대해 자주 묻는 질문에 답변하는 에이전트입니다.
    """,
    tools=[faq_lookup_tool],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 트리아지(분배) 에이전트
triage_agent = Agent[DeveloperProfileContext](
    name="트리아지 에이전트",
    model="gpt-4.1",
    handoff_description="질문을 적절한 에이전트로 분배합니다.",
    instructions="""
    사용자의 질문을 분석해 자기소개, 수상경력, 자격증, 포트폴리오 요약, 프로젝트, 경력, 강점, 기술스택, FAQ 등 적합한 에이전트로 연결하세요.
    """,
    handoffs=[
        about_me_agent,
        awards_agent,
        certifications_agent,
        portfolio_summary_agent,
        project_agent,
        experience_agent,
        strength_agent,
        tech_agent,
        faq_agent,
    ],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

# 각 에이전트에 트리아지 핸드오프 추가 (확장성 고려)
about_me_agent.handoffs.append(triage_agent)
awards_agent.handoffs.append(triage_agent)
certifications_agent.handoffs.append(triage_agent)
portfolio_summary_agent.handoffs.append(triage_agent)
project_agent.handoffs.append(triage_agent)
experience_agent.handoffs.append(triage_agent)
strength_agent.handoffs.append(triage_agent)
tech_agent.handoffs.append(triage_agent)
faq_agent.handoffs.append(triage_agent)
