import streamlit as st

# --- 1. 스토리 노드 정의 (게임의 핵심 데이터) ---
# 각 노드는 'text'와 'choices'를 가짐
# 'choices'는 {선택지 텍스트: 다음 노드 ID} 형태의 딕셔너리
# 특수 키워드: '__END__'는 게임 종료를 의미
#            '__WIN__'은 승리 엔딩을 의미
#            '__LOSE__'는 패배 엔딩을 의미
#            '__ITEM_GET_KEY__': 아이템 획득 조건 ('아이템 이름': '다음 노드 ID')
#            '__ITEM_CHECK_KEY__': 아이템 보유 여부 확인 조건 ('아이템 이름': {'has': '보유 시 노드 ID', 'lacks': '미보유 시 노드 ID'})

story_nodes = {
    "start": {
        "text": "깊은 밤, 당신은 어두운 숲 속 외딴 길을 걷고 있습니다. 저 멀리 희미한 불빛이 보입니다. 당신은 어떻게 하시겠습니까?",
        "choices": {
            "불빛을 향해 간다.": "path_to_light",
            "길을 따라 계속 직진한다.": "continue_straight",
            "숲 속으로 들어가 지름길을 찾는다.": "enter_forest"
        }
    },
    "path_to_light": {
        "text": "불빛에 가까워지자, 낡은 오두막이 보입니다. 문이 살짝 열려 있고, 안에서 작은 소리가 들립니다.",
        "choices": {
            "조심스럽게 문을 열고 들어간다.": "enter_cabin",
            "창문으로 안을 엿본다.": "look_through_window",
            "오두막을 지나쳐 간다.": "continue_straight"
        }
    },
    "enter_cabin": {
        "text": "오두막 안에는 늙은 마녀가 약초를 다듬고 있습니다. 그녀는 당신을 보고 의미심장한 미소를 짓습니다. 그녀의 손에는 오래된 열쇠가 보입니다.",
        "choices": {
            "인사하고 도움을 요청한다.": "talk_to_witch",
            "몰래 열쇠를 훔친다.": "__LOSE__" # 바로 패배 (마녀에게 들킴)
        }
    },
    "talk_to_witch": {
        "text": "마녀는 당신의 사정을 듣더니, '이 숲을 통과하려면 지혜가 필요하다. 이 오래된 '숲의 지혜' 열쇠를 줄테니, 현명하게 사용하거라.' 하며 열쇠를 건넵니다.",
        "choices": {
            "감사히 받고 길을 떠난다.": "__ITEM_GET_KEY__", # 여기서 아이템 획득 로직이 트리거됨
            "더 많은 것을 요구한다.": "__LOSE__" # 탐욕으로 인해 패배
        },
        "item_get": {"숲의 지혜 열쇠": "exit_cabin_with_key"} # 획득할 아이템과 다음 노드
    },
    "exit_cabin_with_key": {
        "text": "열쇠를 얻은 당신은 오두막을 나와 다시 길을 걷습니다. 멀리서 수상한 비명소리가 들립니다.",
        "choices": {
            "비명소리가 나는 곳으로 가본다.": "investigate_scream",
            "무시하고 계속 길을 간다.": "continue_straight_after_cabin"
        }
    },
    "look_through_window": {
        "text": "창문 틈으로 보니, 마녀가 약초를 다듬고 있습니다. 그녀의 옆에는 빛나는 보석이 놓여 있습니다.",
        "choices": {
            "보석을 훔칠 방법을 찾는다.": "__LOSE__", # 들켜서 패배
            "그냥 지나쳐 간다.": "continue_straight"
        }
    },
    "continue_straight": {
        "text": "길을 따라 계속 직진하자, 길이 두 갈래로 나뉩니다. 한쪽은 어두운 동굴 입구이고, 다른 한쪽은 이끼 낀 낡은 다리입니다.",
        "choices": {
            "동굴로 들어간다.": "enter_cave",
            "다리를 건넌다.": "cross_bridge"
        }
    },
    "continue_straight_after_cabin": { # 오두막을 나선 후의 직진
        "text": "오두막을 나선 후 길을 따라 계속 직진하자, 길이 두 갈래로 나뉩니다. 한쪽은 어두운 동굴 입구이고, 다른 한쪽은 이끼 낀 낡은 다리입니다.",
        "choices": {
            "동굴로 들어간다.": "enter_cave",
            "다리를 건넌다.": "cross_bridge"
        }
    },
    "enter_forest": {
        "text": "숲 속으로 들어가자마자 길을 잃었습니다. 어둠 속에서 알 수 없는 소리가 들리고, 당신은 공포에 질립니다.",
        "choices": {
            "소리가 나는 곳으로 숨는다.": "__LOSE__", # 짐승에게 발견됨
            "다시 길을 찾아 숲 밖으로 나간다.": "try_to_exit_forest"
        }
    },
    "try_to_exit_forest": {
        "text": "한참을 헤매다 다행히 길을 찾았지만, 지쳐 쓰러집니다.",
        "choices": {
            "포기한다.": "__LOSE__", # 피로로 쓰러져 사망
            "마지막 힘을 내어 다시 걷는다.": "continue_straight" # 결국 길로 나옴
        }
    },
    "enter_cave": {
        "text": "동굴 속은 매우 어둡고 축축합니다. 깊이 들어갈수록 차가운 바람이 불어옵니다. 앞에는 거대한 바위 문이 당신의 길을 막고 있습니다. 문에는 이상한 문양이 새겨져 있습니다.",
        "choices": {
            "바위 문을 밀어본다.": "__LOSE__", # 문이 움직이지 않음, 동굴에 갇힘
            "문양을 자세히 살펴본다.": "examine_cave_door"
        }
    },
    "examine_cave_door": {
        "text": "문양을 살펴보니, 오래된 퍼즐이 새겨져 있습니다. 그리고 열쇠 구멍이 보입니다.",
        "choices": {
            "열쇠를 사용해본다.": "__ITEM_CHECK_KEY__", # 아이템 확인 로직 트리거
        },
        "item_check": {
            "숲의 지혜 열쇠": {
                "has": "open_cave_door",
                "lacks": "no_key_for_cave"
            }
        }
    },
    "no_key_for_cave": {
        "text": "열쇠가 없어서 문을 열 수 없습니다. 당신은 결국 동굴에 갇히게 됩니다.",
        "choices": {
            "좌절한다.": "__LOSE__"
        }
    },
    "open_cave_door": {
        "text": "숲의 지혜 열쇠를 사용하니, 바위 문이 천천히 열립니다! 그 안에는 밝은 빛이 쏟아져 나오고, 당신은 새로운 세상으로 나아갑니다.",
        "choices": {
            "빛을 향해 나아간다.": "__WIN__"
        }
    },
    "cross_bridge": {
        "text": "이끼 낀 낡은 다리를 조심스럽게 건넙니다. 다리 중간에 오래된 나무 상자가 놓여 있습니다.",
        "choices": {
            "상자를 열어본다.": "open_box_on_bridge",
            "상자를 무시하고 다리를 끝까지 건넌다.": "continue_after_bridge"
        }
    },
    "open_box_on_bridge": {
        "text": "상자 안에는 거미줄이 가득하고, 그 아래 작은 '낡은 지팡이'가 놓여 있습니다.",
        "choices": {
            "지팡이를 줍는다.": "__ITEM_GET_KEY__",
            "그냥 닫고 간다.": "continue_after_bridge"
        },
        "item_get": {"낡은 지팡이": "continue_after_bridge_with_item"}
    },
    "continue_after_bridge": {
        "text": "다리를 무사히 건넌 당신은 넓은 초원에 도착합니다. 저 멀리 거대한 산이 보입니다. 산을 넘어가야 할 것 같습니다.",
        "choices": {
            "산을 향해 간다.": "approach_mountain",
            "다른 길을 찾아본다.": "__LOSE__" # 길을 찾지 못함
        }
    },
    "continue_after_bridge_with_item": {
        "text": "지팡이를 들고 다리를 건넌 당신은 넓은 초원에 도착합니다. 저 멀리 거대한 산이 보입니다. 산을 넘어가야 할 것 같습니다. 지팡이가 당신의 손에서 희미하게 빛납니다.",
        "choices": {
            "산을 향해 간다.": "approach_mountain",
            "다른 길을 찾아본다.": "__LOSE__" # 길을 찾지 못함
        }
    },
    "approach_mountain": {
        "text": "산 기슭에 도착하니, 거대한 돌벽이 당신을 막고 있습니다. 벽에는 고대 문자가 새겨져 있습니다.",
        "choices": {
            "고대 문자를 해독해본다.": "decipher_runes",
            "지팡이를 사용해본다.": "__ITEM_CHECK_KEY__" # 아이템 확인 로직 트리거
        },
        "item_check": {
            "낡은 지팡이": {
                "has": "use_staff_on_mountain",
                "lacks": "no_staff_for_mountain"
            }
        }
    },
    "decipher_runes": {
        "text": "고대 문자는 너무 복잡하여 당신의 지식으로는 해독할 수 없습니다. 길은 막혀 있습니다.",
        "choices": {
            "포기한다.": "__LOSE__"
        }
    },
    "no_staff_for_mountain": {
        "text": "지팡이가 없어서 돌벽을 뚫을 수 없습니다. 산을 넘을 방법이 보이지 않습니다.",
        "choices": {
            "포기한다.": "__LOSE__"
        }
    },
    "use_staff_on_mountain": {
        "text": "낡은 지팡이를 돌벽에 가져다 대니, 지팡이가 강렬하게 빛나며 돌벽에 새로운 문이 생겨납니다. 그 문을 통과하자, 드디어 숲을 벗어나 자유를 얻게 됩니다!",
        "choices": {
            "새로운 세상으로 나아간다.": "__WIN__"
        }
    },
    "investigate_scream": {
        "text": "비명소리가 나는 곳으로 가보니, 작은 동물이 덫에 걸려 있습니다. 덫은 복잡한 구조로 되어 있어 해제하기가 어렵습니다.",
        "choices": {
            "동물을 구해주려 노력한다.": "try_to_save_animal",
            "그냥 지나쳐 간다.": "continue_straight_after_cabin"
        }
    },
    "try_to_save_animal": {
        "text": "덫을 해제하는 데 너무 많은 시간을 소모했고, 결국 숲의 어둠에 갇히고 맙니다.",
        "choices": {
            "운명을 받아들인다.": "__LOSE__"
        }
    },
    "win_ending": {
        "text": "🎊 축하합니다! 당신은 숲 속 모험에서 살아남아 자유를 얻었습니다. 당신의 용기와 지혜가 당신을 승리로 이끌었습니다!",
        "choices": {} # 게임 종료
    },
    "lose_ending": {
        "text": "💀 당신의 모험은 여기서 끝났습니다. 어둠 속에 갇히거나, 예상치 못한 위험에 처하고 말았습니다. 다시 시도해보시겠습니까?",
        "choices": {} # 게임 종료
    }
}

# --- 2. 스트림릿 앱 UI 및 로직 ---

st.set_page_config(page_title="밤 숲 속 모험", layout="centered")

st.title("🌲 밤 숲 속 모험")
st.markdown("당신의 선택이 운명을 결정합니다.")

# 게임 상태 초기화 (세션 상태 사용)
if 'current_node' not in st.session_state:
    st.session_state.current_node = "start"
    st.session_state.inventory = [] # 플레이어가 획득한 아이템 목록
    st.session_state.game_over = False

current_node_id = st.session_state.current_node
current_node = story_nodes[current_node_id]

# --- 게임 로직 ---

# 게임 오버 상태일 경우
if st.session_state.game_over:
    if current_node_id == "__WIN__":
        st.success(story_nodes["win_ending"]["text"])
    elif current_node_id == "__LOSE__":
        st.error(story_nodes["lose_ending"]["text"])
    
    if st.button("새 게임 시작"):
        st.session_state.current_node = "start"
        st.session_state.inventory = []
        st.session_state.game_over = False
        st.experimental_rerun() # 앱을 새로고침하여 초기 상태로 돌아감
    
    st.stop() # 게임 오버 시 더 이상 진행하지 않음

# 현재 스토리 노드 텍스트 표시
st.markdown(f"**{current_node['text']}**")

# 인벤토리 표시 (디버깅 또는 정보 제공용)
if st.session_state.inventory:
    st.sidebar.subheader("나의 인벤토리")
    for item in st.session_state.inventory:
        st.sidebar.markdown(f"- {item}")
else:
    st.sidebar.info("인벤토리가 비어 있습니다.")


# 선택지 버튼 표시
for choice_text, next_node_id in current_node['choices'].items():
    if st.button(choice_text):
        # 특수 키워드 처리
        if next_node_id == "__END__":
            st.session_state.game_over = True
            st.session_state.current_node = "end_node" # 실제 없는 노드이므로 처리 필요
        elif next_node_id == "__WIN__":
            st.session_state.game_over = True
            st.session_state.current_node = "__WIN__"
        elif next_node_id == "__LOSE__":
            st.session_state.game_over = True
            st.session_state.current_node = "__LOSE__"
        elif next_node_id == "__ITEM_GET_KEY__":
            # 아이템 획득 로직
            item_to_get = list(current_node["item_get"].keys())[0] # 첫 번째 아이템만 처리 (간단화)
            next_real_node = current_node["item_get"][item_to_get]
            if item_to_get not in st.session_state.inventory:
                st.session_state.inventory.append(item_to_get)
                st.success(f"아이템 획득! : **{item_to_get}**")
            st.session_state.current_node = next_real_node
        elif next_node_id == "__ITEM_CHECK_KEY__":
            # 아이템 확인 로직
            item_to_check = list(current_node["item_check"].keys())[0] # 첫 번째 아이템만 처리 (간단화)
            if item_to_check in st.session_state.inventory:
                st.session_state.current_node = current_node["item_check"][item_to_check]["has"]
            else:
                st.session_state.current_node = current_node["item_check"][item_to_check]["lacks"]
        else:
            # 일반적인 다음 노드로 이동
            st.session_state.current_node = next_node_id
        
        st.experimental_rerun() # 선택 후 화면 새로고침
