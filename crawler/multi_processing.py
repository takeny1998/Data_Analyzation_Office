from multiprocessing import Process
from database.db_handler import DBHandler
from crawler import Crawler
import time

def political_worker(db_handler):
    political = Crawler('POLITICAL')
    p_json = political.nouns()
    db_handler.insert_crawling_data('P', p_json)
    print("POLITICAL done!")


def economy_worker(db_handler):
    economy = Crawler('ECONOMY')
    e_json = economy.nouns()
    db_handler.insert_crawling_data('E', e_json)
    print("ECONOMY done!")


def social_worker(db_handler):
    social = Crawler('SOCIAL')
    s_json = social.nouns()
    db_handler.insert_crawling_data('S', s_json)
    print("SOCIAL done!")


def life_culture_worker(db_handler):
    life_cluture = Crawler('LIFE/CULTURE')
    c_json = life_cluture.nouns()
    db_handler.insert_crawling_data('C', c_json)
    print("LIFE/CULTURE done!")


def world_worker(db_handler):
    world = Crawler('WORLD')
    w_json = world.nouns()
    db_handler.insert_crawling_data('W', w_json)
    print("WORLD done!")


def it_science_worker(db_handler):
    it_science = Crawler('IT/SCIENCE')
    i_json = it_science.nouns()
    db_handler.insert_crawling_data('I', i_json)
    print("IT/SCIENCE done!")


if __name__ == '__main__':
    start = time.time()  # 시작 시간 저장
    db_handler = DBHandler()

    pc_process = Process(target=political_worker, args=(db_handler,))
    eco_process = Process(target=economy_worker, args=(db_handler,))
    sc_process = Process(target=social_worker, args=(db_handler,))
    lc_process = Process(target=life_culture_worker, args=(db_handler,))
    wd_process = Process(target=world_worker, args=(db_handler,))
    is_process = Process(target=it_science_worker, args=(db_handler,))

    pc_process.start()
    eco_process.start()
    sc_process.start()
    lc_process.start()
    wd_process.start()
    is_process.start()

    pc_process.join()
    eco_process.join()
    sc_process.join()
    lc_process.join()
    wd_process.join()
    is_process.join()

    db_handler.close()
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간