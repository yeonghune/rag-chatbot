# 🤖 RAG Chatbot

이 프로젝트는 **Retrieval-Augmented Generation (RAG)** 기반의 개인 챗봇을 구축하는 것을 목표로 합니다.  
**LangChain**을 활용해 문서 임베딩, 벡터 검색, LLM 응답 생성을 파이프라인화하였습니다.

---
## 🧩 주요 기술 스택
- **Frontend**: React(Vite)
- **Backend**: FastAPI
- **DB**: PostgreSQL
- **Vector DB**: Chroma
- **LLM/Embedding**: gemini-2.5-flash, models/embedding-001 (fallback: HuggingFace)
- **RAG Framework**: LangChain
- **Infra**: Docker, NGINX, GitHub Actions

---

## 🎯 애플리케이션 주요 목표
- LLM 기반 챗봇 구현
- 문서 임베딩 RAG 파이프라인 구축
- FastAPI 공식문서 기반 벡터스토어 구축

---

## ⚙️ 백엔드 목표
- **ID/PASSWORD 기반 로그인** 구현  
  - Access Token + Refresh Token 전략
  - HttpOnly + Secure 쿠키 적용
  - RBAC(Role-Based Access Control) 적용
- **RAG 파이프라인 구축**
  - 문서 업로드 → 청킹 → 임베딩 → Vector Store 등록
  - Retriever를 통한 관련 문서 검색 및 컨텍스트 구성
- **API 설계**
  - Auth, Chat, RAG 등 모듈화
  - Layered Architecture (Router → Service → Repository → Model)
- **SSE 스트리밍**
    - FastAPI → 클라이언트로 직접 스트림 전송

---

## 💻 프론트엔드 목표
- **React(Vite) 기반 SPA 구성**
  - 로그인 / 회원가입 / 로그아웃 화면
  - 채팅 인터페이스 및 SSE 기반 실시간 응답 표시
- **UI/UX**
  - 최소한의 디자인으로 직관적인 구조 유지
  - 추후 관리자용 인터페이스로 확장 가능

---

## 🧱 개발 및 배포
- **개발 환경**: Docker Compose 기반 로컬 환경 구성
- **배포 자동화**: GitHub Actions를 이용한 CI/CD 구축
- **NGINX**: HTTPS 리버스 프록시 및 정적 리소스 서빙