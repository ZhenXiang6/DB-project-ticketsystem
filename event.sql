SELECT setval('event_e_id_seq', 200, TRUE);

-- INSERT EVENT :(
INSERT INTO EVENT (e_name, c_id, o_id, e_datetime, e_location)
-- ["Concert","Musical","Exhibition","Drama","Music","Dance","Family","Sports","Others"]
VALUES 
-- concert 1
('ASKA CONCERT TOUR 2025 WHO is ASKA ⁉ in TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-1 19:30:00', '台北國際會議中心TICC'),
('2025 Ado世界巡迴演場會-台北站 Ado WORLD TOUR 2025＂Hibana＂Powered by Crunchyroll in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-05-11 18:00:00', '國立體育大學綜合體育館'),
('戴佩妮 2025「雙生火焰」台北小巨蛋演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-22 19:30:00', '台北小巨蛋'),
('Phantom Siita 1ST WORLD TOUR＂Moth to a flame＂Phantom Siita 首次世界巡迴演唱會-台北站', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-16 20:00:00', 'Legacy Taipei'),
('SIGUR RÓS 2025 台北演唱會SIGUR RÓS WITH NATIONAL SYMPHONY ORCHESTRA', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-22 20:00:00', '臺北國際會議中心大會堂'),
('民歌50高峰會 最終場', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-22 20:00:00', '台中中興大學惠蓀堂'),
('TRASH《幸福的末班車》15週年演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-24 19:30:00', '台北小巨蛋'),
('Official髭男dism 2024 Rejoice亞洲巡迴演唱會－台北站', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-15 18:00:00', '台北小巨蛋'),
('2025羅志祥 30巡迴演唱會 高雄站', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-31 19:30:00', '高雄巨蛋'),
('Gracie Abrams：The Secret of Us Tour in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-4-17 19:30:00', 'TICC Taipe'),
('RUSSELL PETERS RELAX WORLD TOUR', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-4-9 19:30:00', '台北國際會議中心TICC'),
('keshi：REQUIEM TOUR IN TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-28 19:30:00', '國立體育大學綜合體育館'),
('事後菸樂團 Cigarettes After Sex：X’s World Tour MESSE TAOYUAN CONCERT 2025', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-22 19:30:00', '桃園會展中心'),
('Kylie Minogue：Tension Tour 2025', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-15 19:30:00', '高雄巨蛋'),
('Mogwai LIVE IN TAIPEI 2025', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-14 19:30:00', 'Zepp New Taipei'),
('Kehlani – CRASH WORLD TOUR', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-10 19:30:00', 'Zepp New Taipei'),
('Human Musical Group Sensations GLASS ANIMALS：TOUR OF EARTH in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-2 19:30:00', 'Legacy Taipei'),
('大誠保經 x 麋先生 MIXER〈馬戲團運動 CircUs〉世界巡迴演唱會 高雄站', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-3-1 19:30:00', '高雄巨蛋'),
('KIRE presents EROS 愛神', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-22 19:30:00', 'Legacy Taipei'),
('星展銀行獨家冠名贊助 蘇打綠《二十年一刻》巡迴演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-22 19:30:00', '台北小巨蛋'),
('NIKI： Buzz World Tour', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-20 19:30:00', '台北國際會議中心TICC'),
('Maroon 5 Asia 2025 – Kaohsiung', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-14 19:30:00', '高雄國家體育場(世運主場館)'),
('2024-25 2NE1 ASIA TOUR [WELCOME BACK] IN TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-8 19:30:00', '國立體育大學綜合體育館'),
('wave to earth 0.03 World Tour in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-2-7 19:30:00', 'Zepp New Taipei'),
('DAY6 3RD WORLD TOUR ＜FOREVER YOUNG＞ in KAOHSIUNG', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-18 19:30:00', '高雄流行音樂中心'),
('2024 Just Love It 一路向東演唱會 火車專車旅遊專案', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-18 19:30:00', '多個表演場地'),
('Solar’s TALK CONCERT [Topic Check] in TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-12 19:30:00', 'Legacy TERA'),
('The Jesus And Mary Chain： 40+0.5 Years IN TAIPEI 2025', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-8 19:30:00', 'Legacy Taipei'),
('Angel High School 2024 Fan Party  in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-29 19:30:00', 'Clapper Studio'),
('MAYDAY #5525 LIVE TOUR 五月天 [ 回到那一天 ] 25週年巡迴演唱會 新年特別版 玉山卡友專區', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-28 19:30:00', '樂天桃園棒球場'),
('DPR - The Dream Reborn World Tour 2024 in TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-28 19:30:00', 'Legacy TERA'),
('國泰世華銀行《ASMR Maxxx @ Taipei Dome 世界巡迴演唱會》', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-21 19:30:00', '臺北大巨蛋'),
('JUNG SO MIN FANMEETING［LOVE SO SWEET］in TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-15 19:30:00', 'Zepp New Taipei'),
('曾立馨《轉來》專場巡迴', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-12-15 19:30:00', '多個表演場地'),
('HWANG IN YOUP FANMEETING TOUR [IN LOVE] in TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-14 19:30:00', 'Zepp New Taipei'),
('TAEYANG 2024 TOUR [THE LIGHT YEAR] IN TAIPEI', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-14 19:30:00', '臺北流行音樂中心表演廳'),
('Porter Robinson SMILE!：D World Tour in Taipei', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-10 19:30:00', 'Zepp New Taipei'),
('PARK JIHOON WINTER FANMEETING IN TAIPEI《Opening》', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-8 19:30:00', 'Legacy TERA'),
('蕭秉治Xiao Bing Chih《活著Alive》小巨蛋演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-7 19:30:00', '台北小巨蛋'),
('周杰倫 嘉年華 世界巡迴演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-5 19:30:00', '臺北大巨蛋'),
('周杰倫 嘉年華 世界巡迴演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-6 19:30:00', '臺北大巨蛋'),
('周杰倫 嘉年華 世界巡迴演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-7 18:00:00', '臺北大巨蛋'),
('周杰倫 嘉年華 世界巡迴演唱會', 1, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-8 18:00:00', '臺北大巨蛋'),
-- Exhibition 3
('《梵谷：尋光之路》特展', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-8-24 9:00:00', '富邦美術館'),
('田中達也特展－大師眼中的微型組合', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-10 19:30:00', '中正紀念堂1展廳'),
('AI繪動的畫特展', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-27 10:00:00', '國立台灣科學教育館'),
('AI SPORT', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-24 10:00:00', '國立臺灣科學教育館'),
('侏羅紀X恐龍光影展 高雄站', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-24 19:30:00', '高雄駁二藝術特區'),
('CWT－68台灣同人誌販售會．台北場．單日票', 3, 8, '2024-12-14 10:30:00', '國立臺灣大學綜合體育館'),
('CWT－68台灣同人誌販售會．台北場．雙日票', 3, 8, '2024-12-14 10:30:00', '國立臺灣大學綜合體育館'),
('CWT－K46台灣同人誌販售會．高雄場．雙日票', 3, 8, '2024-12-21 10:30:00', '高雄市立社會教育館-綜合體育館'),
('CWT－K46台灣同人誌販售會．高雄場．單日票', 3, 8, '2024-12-21 10:30:00', '高雄市立社會教育館-綜合體育館'),
('GJ32動漫創作展', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-28 10:30:00', '逢甲大學育樂館'),
('國家地理女性經典影像展', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-21 10:30:00', '松山文創園區-1號倉庫'),
('「新藝術運動」光影藝術展 從高第到慕夏、克林姆', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-30 19:30:00', '華山文創園區'),
('Animage雜誌和吉卜力展', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2025-1-8 10:00:00', '華山1914文創園區'),
('小魔女DoReMi 25週年展．一般票', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-25 10:30:00', '華山1914文化創意產業園區'),
('雙展套票‧2024 甜蜜生活日Ｘ心願交易所', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-13 10:30:00', '華山1914文創產業園區'),
('《幻隱光靈：仙蹤》沉浸式互動實境解謎', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-29 13:00:00', '光復南路133號 南向製菸工廠'),
('松菸實境解謎包—時光1937保管箱的秘密', 3, (SELECT o_id FROM ORGANIZER ORDER BY RANDOM() LIMIT 1), '2024-12-31 00:00:00', '台北市信義區光復南路133號'),
('奇美博物館．畫師們尼德蘭繪畫時代特展．二人同行票', 3, 6, '2024-10-26 9:30:00', '奇美博物館'),
('奇美博物館．畫師們尼德蘭繪畫時代特展．一般票', 3, 6, '2024-10-26 9:30:00', '奇美博物館'),
('奇美博物館．畫師們尼德蘭特展＆常設展．雙展套票', 3, 6, '2024-10-26 9:30:00', '奇美博物館'),
('奇美博物館．2024聖誕週末．華麗盛宴＆特展聯票', 3, 6, '2024-12-14 14:30:00', '奇美博物館'),
('奇美博物館．2024聖誕週末．華麗盛宴', 3, 6, '2024-12-14 14:30:00', '奇美博物館'),
('奇美博物館常設展', 3, 6, '2024-7-1 9:30:00', '奇美博物館'),
('奇美博物館．穿越時空的航海家實境遊戲．需到館取貨', 3, 6, '2024-3-1 19:30:00', '奇美博物館'),
('昨日列車-台北捷運一日解謎旅行(唯一台北捷運公司官方聯名)', 3, 6, '2024-11-1 00:00:00', '台北捷運任一站點集合'),
-- Sport 8
('D1 GRAND PRIX TAIWAN RD1＆2 台南府城 2024', 8, 7, '2024-12-13 8:00:00', 'ICC TAINAN 大台南會展中心旁'),
('D1 GRAND PRIX TAIWAN RD1＆2 台南府城 2024', 8, 7, '2024-12-14 8:00:00', 'ICC TAINAN 大台南會展中心旁'),
('D1 GRAND PRIX TAIWAN RD1＆2 台南府城 2024', 8, 7, '2024-12-15 8:00:00', 'ICC TAINAN 大台南會展中心旁'),
('2024-2025 PLG桃園璞園領航猿主場', 8, 3, '2024-12-14 17:00:00', '桃園市立綜合體育館(桃園巨蛋)'),
('2024-2025 PLG桃園璞園領航猿主場', 8, 3, '2024-12-15 17:00:00', '桃園市立綜合體育館(桃園巨蛋)'),
('2024-2025 PLG桃園璞園領航猿主場', 8, 3, '2024-12-17 19:00:00', '桃園市立綜合體育館(桃園巨蛋)'),
('2024-2025 PLG桃園璞園領航猿主場', 8, 3, '2024-12-21 17:00:00', '桃園市立綜合體育館(桃園巨蛋)'),
('2024-2025 PLG桃園璞園領航猿主場', 8, 3, '2024-12-22 17:00:00', '桃園市立綜合體育館(桃園巨蛋)'),
('TPBL例行賽　福爾摩沙夢想家主場', 8, 8, '2024-12-11 8:00:00', '臺中洲際迷你蛋'),
('TPBL例行賽　福爾摩沙夢想家主場', 8, 8, '2024-12-13 8:00:00', '臺中洲際迷你蛋'),
('TPBL例行賽　福爾摩沙夢想家主場', 8, 8, '2024-12-27 8:00:00', '臺中洲際迷你蛋'),
('2024年亞洲冬季棒球聯盟', 8, 5, '2024-12-14 12:05:00', '雲林縣立斗六棒球場'),
('2024年亞洲冬季棒球聯盟', 8, 5, '2024-12-14 18:05:00', '雲林縣立斗六棒球場'),
('2024年亞洲冬季棒球聯盟', 8, 5, '2024-12-15 12:05:00', '雲林縣立斗六棒球場'),
('2024年亞洲冬季棒球聯盟', 8, 5, '2024-12-15 18:05:00', '雲林縣立斗六棒球場');


SELECT setval('organizer_o_id_seq', 20, TRUE);
-- ORGANIZER
INSERT INTO ORGANIZER (o_name, contact_info)
VALUES 
('寬宏藝術', 'khamtw@gmail.com'),
('杰威爾音樂有限公司', 'jvrservice@jvrmusic.com');

SELECT setval('venue_v_id_seq', 30, TRUE);
INSERT INTO VENUE (v_name, address, capacity, contact_info)
VALUES
    ('台北國際會議中心TICC', '台北市信義路五段1號', 3000, '0227255200'),
	('Zepp New Taipei', '新北市新莊區新北大道四段3號8樓', 2000, '0285228553'),
    ('台北小巨蛋', '台北市南京東路四段2號', 15000, '0225783536'),
	('台北大巨蛋', '台北市信義區忠孝東路四段515號', 15000, '0227228811'),
    ('高雄展覽館', '高雄市前鎮區成功二路39號', 5000, '0712345678'),
    ('台中國家歌劇院', '台中市西屯區惠來路二段101號', 2000, '0487654321'),
    ('國父紀念館演藝廳', '台北市忠孝東路四段505號', 1000, '0255667788'),
    ('中正紀念堂自由廣場音樂廳', '台北市中正區中山南路21號', 2000, '0233445566'),
    ('花蓮文化創意產業園區', '花蓮市中正路99號', 500, '0322334455'),
    ('台東藝術中心', '台東市中興路100號', 800, '0891234567'),
    ('宜蘭演藝廳', '宜蘭市復興路三段36號', 1200, '0377889900'),
    ('新竹文化局演藝廳', '新竹市東區中正路17號', 1500, '0311223344'),
	('國立體育大學綜合體育館', '桃園市龜山區文化一路250號', 15000, '033283201'),
	('高雄巨蛋', '高雄市左營區博愛二路757號', 15000, '079749888'),
	('Legacy Taipei', '台北市中正區八德路一段1號華山1914創意文化園區中5A館', 1500, '0223956660');




-- select * from "ORDER"
-- select * from customer
-- select * from category
-- select * from event
-- select * from event_venue
-- select * from order_detail
-- select * from organizer
-- select * from payment
-- select * from ticket
-- select * from venue
