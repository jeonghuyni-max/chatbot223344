import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 및 제목 한글화
st.set_page_config(page_title="✈️ 여행 도우미 챗봇", page_icon="📍")
st.title("✈️ 나만의 여행 가이드")
st.write(
    "어디로 떠나고 싶으신가요? 맛집, 코스 추천, 여행 꿀팁까지 무엇이든 물어보세요! "
    "\n\n이 앱을 사용하려면 [OpenAI API 키](https://platform.openai.com/account/api-keys)가 필요합니다."
)

# 2. API 키 입력 섹션
openai_api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

if not openai_api_key:
    st.info("서비스 이용을 위해 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)

    # 3. 세션 상태에 메시지 저장 (대화 기록 유지)
    if "messages" not in st.session_state:
        # 시스템 프롬프트를 추가하여 여행 전문가의 정체성을 부여합니다.
        st.session_state.messages = [
            {"role": "system", "content": "당신은 친절하고 전문적인 여행 가이드입니다. 한국어로 답변하며, 사용자의 여행 계획에 맞춰 맛집, 관광지, 교통수단 등을 구체적으로 추천해 주세요."}
        ]

    # 4. 기존 대화 내용 표시 (시스템 메시지는 제외하고 표시)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 5. 사용자 입력창
    if prompt := st.chat_input("예: 2월에 가기 좋은 일본 여행지 추천해줘!"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 6. OpenAI API를 이용한 답변 생성
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini", # 가성비와 성능이 좋은 최신 모델로 변경
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        
        # 답변을 세션 상태에 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
