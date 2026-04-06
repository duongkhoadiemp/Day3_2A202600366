import requests
from typing import List

def get_synonyms(word: str) -> List[str]:
    """
    Sử dụng Datamuse API để lấy danh sách các từ đồng nghĩa.
    Đây là API công cộng, không yêu cầu API Key cho các tác vụ thông thường.
    
    Args:
        word (str): Từ tiếng Anh cần tìm từ đồng nghĩa.
        
    Returns:
        List[str]: Danh sách các từ đồng nghĩa.
    """
    # Endpoint của Datamuse: rel_syn tìm các từ đồng nghĩa (synonyms)
    api_url = f"https://api.datamuse.com/words?rel_syn={word}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        # Dữ liệu trả về có dạng: [{"word": "cheerful", "score": 1234}, ...]
        data = response.json()
        
        # Trích xuất chỉ lấy phần chữ (word) từ danh sách kết quả
        synonyms = [item['word'] for item in data]
        
        return synonyms

    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối API: {e}")
        return []


# if __name__ == "__main__":
#     search_word = str(input())
#     result = get_synonyms(search_word)
    
#     if result:
#         print(f"Các từ đồng nghĩa của '{search_word}':")
#         print(result)
#     else:
#         print(f"Không tìm thấy từ đồng nghĩa nào cho '{search_word}'.")