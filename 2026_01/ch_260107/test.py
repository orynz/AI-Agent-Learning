# from typing import List

# class Music:
#     def __init__(self, singer: str, song: str):
#         self.singer = singer  # 가수 이름
#         self.song = song      # 곡 제목

#     def play(self):
#         print(f"Play -> {self.song} / {self.singer}")

# class MusicPlayer:
#     def __init__(self):
#         self.__music_list: List[Music] = []  # 음악 목록을 저장할 리스트

#     def setList(self, music_list: List[Music]):
#         self.__music_list = music_list

#     def play(self):
#         if not self.__music_list:
#             print("No music available in the playlist.")
#             return
        
#         print("Starting playback:")
#         for idx, music in enumerate(self.__music_list, 1):
#             music.play()


# # 예제 사용
# if __name__ == "__main__":
#     music_list: List = [
#         Music("조용필", "창밖의 여자"),
#         Music("이선희", "아~ 옛날이여"),
#         Music("악동뮤지션", "바람의 노래")
#     ]

#     player = MusicPlayer()
#     player.setList(music_list)
#     player.play()
# 클래스 정의


from typing import List

# 1. 클래스 정의 (추상화/캡슐화)
class Music:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"{self.title} - {self.artist}"

class Player:
    def __init__(self, name: str):
        self.name = name
        self.__music_list: List[Music] = []  # 캡슐화: 외부 직통 접근 차단

    # Getter: 리스트 조회
    @property
    def music_list(self):
        return self.__music_list

    # Setter: 리스트 교체 시 검증 로직 (캡슐화)
    @music_list.setter
    def music_list(self, new_list: List[Music]):
        if isinstance(new_list, list):
            print(f"[{self.name}] 재생목록을 업데이트합니다.")
            self.__music_list = new_list
        else:
            print("오류: 올바른 리스트 형식이 아닙니다.")

    def play(self):
        if not self.__music_list:
            print("재생할 곡이 없습니다.")
        else:
            print(f"현재 재생 중: {self.__music_list[0]}")

# 2. 상속 (Inheritance)
class PremiumPlayer(Player):
    def shuffle(self):
        import random
        random.shuffle(self.music_list)
        print("목록을 섞었습니다!")

# --- 실제 사용 ---
# 객체 생성
my_player = PremiumPlayer("나의 플레이어")

# 데이터 준비
songs = [Music("Hype Boy", "NewJeans"), Music("Seven", "Jungkook")]

# Setter 사용 (변수처럼 할당)
my_player.music_list = songs 

# 메서드 실행
my_player.play()
my_player.shuffle()
