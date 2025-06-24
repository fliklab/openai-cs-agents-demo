from pydantic import BaseModel
from typing import List, Optional


class Project(BaseModel):
    name: str
    description: str
    tech_stack: List[str]
    link: Optional[str] = None


class Experience(BaseModel):
    company: str
    position: str
    period: str
    description: Optional[str] = None


class Award(BaseModel):
    title: str
    issuer: str
    year: str
    description: Optional[str] = None


class Certification(BaseModel):
    name: str
    issuer: str
    year: str
    description: Optional[str] = None


class DeveloperProfileContext(BaseModel):
    name: str = "홍길동"
    email: Optional[str] = "hong.dev@email.com"
    phone: Optional[str] = "010-1234-5678"
    github: Optional[str] = "https://github.com/hongdev"
    tech_stack: List[str] = ["Python", "TypeScript", "React", "AWS"]
    about_me: str = "안녕하세요, 5년차 백엔드/풀스택 개발자 홍길동입니다. 다양한 스타트업과 IT기업에서 실무 경험을 쌓았으며, 문제 해결과 협업을 즐깁니다."
    projects: List[Project] = [
        Project(
            name="AI 챗봇 플랫폼",
            description="기업용 AI 챗봇 플랫폼 설계 및 개발",
            tech_stack=["Python", "FastAPI", "React"],
            link="https://github.com/hongdev/ai-chatbot"
        ),
        Project(
            name="실시간 데이터 대시보드",
            description="대용량 실시간 데이터 시각화 대시보드 개발",
            tech_stack=["TypeScript", "Next.js", "D3.js"]
        )
    ]
    experiences: List[Experience] = [
        Experience(
            company="ABC Tech",
            position="백엔드 개발자",
            period="2021-2023",
            description="AI/데이터 파이프라인 구축 및 운영"
        ),
        Experience(
            company="스타트업 XYZ",
            position="풀스택 개발자",
            period="2019-2021"
        )
    ]
    strengths: List[str] = ["문제 해결력", "책임감", "협업과 소통"]
    personality: str = "적극적이고 논리적인 커뮤니케이션을 선호하며, 새로운 기술 학습을 즐깁니다."
    awards: List[Award] = [
        Award(
            title="우수 개발자상",
            issuer="ABC Tech",
            year="2022",
            description="AI 챗봇 프로젝트의 성공적 런칭 기여"
        )
    ]
    certifications: List[Certification] = [
        Certification(
            name="정보처리기사",
            issuer="한국산업인력공단",
            year="2018"
        )
    ]
    portfolio_url: Optional[str] = "https://hongdev.dev"
    # TODO: 필요에 따라 자기소개, 수상경력, 자격증 등 추가 가능
