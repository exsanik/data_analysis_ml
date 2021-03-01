from functools import reduce
import math

if __name__ == "__main__":
    calls_per_hour = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18]
    detected_freq = [0, 1, 2, 4, 6, 7, 9, 2, 5, 4, 2, 0, 8]

    mid_calls_per_hour = reduce(
        lambda acc, li: acc + (li[0] * li[1]),
        zip(calls_per_hour, detected_freq), 0) / sum(detected_freq)

    mid_calls_per_min = mid_calls_per_hour / 60
    mins_to_serve = 18.5
    stream_intensity = 0.054
    intensity = mins_to_serve * stream_intensity

    members = 7
    team_members = 1
    teams = members / team_members

    prob_chanel_empty = 1 / reduce(lambda acc, it: acc +
                                   ((intensity ** it) / math.factorial(it)),
                                   range(0, int(teams) + 1), 0)
    prob_chanel_busy = (
        intensity ** teams / math.factorial(teams)) * prob_chanel_empty

    teams_busy = intensity * (1 - prob_chanel_busy)

    busy_time = round(prob_chanel_busy * mid_calls_per_min, 3)
    print("Среднее время простоя при полной загрузке", f"{busy_time} мин")

    print("Вероятноe количество загрженых команд: ", round(teams_busy))

    print("Вероятность полной загрузки: ",
          f"{round(prob_chanel_busy * 100, 2)}%")
    print("Вероятность простоя: ", f"{round(prob_chanel_empty * 100, 2)}%")
