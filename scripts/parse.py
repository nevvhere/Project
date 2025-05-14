import requests
import pandas as pd
import time

def parse_soundcloud_tracks():
    # Вставляем API
    client_id = "AXHkknI02RnaQ0vVJ3FK3pVcoToTlmFK"
    
    # Список тегов для сбора треков
    tags = ['hip-hop', 'jazz', 'chill', 'trap', 'indi', 'pop']
    all_tracks = []
    
    # По 25 треков на каждый тег
    for tag in tags:
        print(f"Загружаем треки для тега: {tag}")
        
        url = f"https://api-v2.soundcloud.com/search/tracks?q={tag}&client_id={client_id}&limit=25"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Ошибка при запросе для тега {tag}: {response.status_code}")
            continue
        
        data = response.json()

        for track in data.get("collection", []):
            all_tracks.append({
                "Тег": tag,
                "Название трека": track.get("title"),
                "Прослушивания": track.get("playback_count"),
                "Лайки": track.get("likes_count"),
                "Комментарии": track.get("comment_count"),
                "Теги из трека": track.get("tag_list")
            })
        
        time.sleep(1)  # Не перегружаем API
    
    # Создание DataFrame
    df = pd.DataFrame(all_tracks)
    
    # Сохраняем таблицу в CSV
    df.to_csv("soundcloud_tracks.csv", index=False)
    print("Данные успешно сохранены в soundcloud_tracks.csv")

if __name__ == "__main__":
    parse_soundcloud_tracks()
