# CUBRID Lab 브랜드 시스템

이 저장소는 CUBRID Lab의 로고·아이콘·기하 규칙·언어별 색상·저장소 매핑을 관리하는 정본입니다.

> CUBRID Lab은 독립적인 커뮤니티 오픈소스 프로젝트이며 CUBRID Corporation 또는 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없습니다. CUBRID 명칭은 데이터베이스 호환성을 설명하기 위해 사용합니다.

## 핵심 규칙

- **형태 = 기술적 역할**
- **색상 = 구현 언어**

첫 승인 대상은 Driver 심볼입니다. 서로 반전된 두 기하 모듈이 중앙의 데이터 채널을 사이에 두고 맞물리는 형태로, 애플리케이션 런타임과 CUBRID를 연결하는 Driver의 역할을 표현합니다.

ORM은 이후 **수직 계층/추상화** 형태로 별도 설계하여 Driver와 실루엣부터 구분합니다.

언어 토큰:

- Python — `#3776AB`
- TypeScript — `#3178C6`
- Go — `#00ADD8`
- Rust — `#CE422B`

이 색상들은 **CUBRID Lab 내부 디자인 토큰**이며 CUBRID의 공식 브랜드 색상이라고 주장하지 않습니다.

## 현재 매핑

Driver 승인:

- `pycubrid` — Python
- `cubrid-client` — TypeScript
- `cubrid-go` — Go
- `cubrid-rs` — Rust

역할 심볼 승인 대기:

- ORM/Dialect: `sqlalchemy-cubrid`, `drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`
- MCP: `cubrid-mcp-server` — Python
- Cookbook: `cubrid-cookbook-python` — Python
- Benchmark: `cubrid-benchmark` — 다중 언어
- Operator: `cubrid-kubernetes-operator` — Go

법적·상표 검토가 완료되기 전에는 이 저장소의 디자인 승인 상태를 비침해 확인으로 해석하지 않습니다.

Refs #1.
