from database.DB_connect import DBConnect
from model.player import Player


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getNodi(goal):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.* 
                    from premierleague.players p ,(
                    select a.PlayerID ,avg(a.Goals) AvgGoal
                    from premierleague.actions a 
                    group by a.PlayerID 
                    having AvgGoal > %s) a
                    where a.PlayerID=p.PlayerID """

        cursor.execute(query, (goal,))

        for row in cursor:
            result.append(Player(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(goal):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=False)
        query = """select  a1.PlayerID, a2.PlayerID , (sum(a2.timeP) - sum(a1.timeP)) as diff
                    from (
                    select distinctrow a2.*, a.Starts , a.TeamID,a.MatchID, a.TimePlayed timeP
                    from premierleague.actions a ,(
                    select a.PlayerID ,avg(a.Goals) g
                    from premierleague.actions a
                    group by a.PlayerID
                    having g > %s
                    order by a.PlayerID) a2
                    where a.PlayerID =a2.PlayerID
                    and a.Starts =1
                    ) a1,
                    (select distinctrow a2.*, a.Starts , a.TeamID,a.MatchID, a.TimePlayed timeP
                    from premierleague.actions a ,(
                    select a.PlayerID ,avg(a.Goals) g
                    from premierleague.actions a
                    group by a.PlayerID
                    having g > %s
                    order by a.PlayerID) a2
                    where a.PlayerID =a2.PlayerID
                    and a.Starts =1
                    ) a2
                    where a1.MatchID = a2.MatchID
                    and a1.TeamId<>a2.TeamID
                    and a1.PlayerID<a2.PlayerID
                    group by a1.PlayerID, a2.PlayerID
                    having diff<>0"""

        cursor.execute(query, (goal,goal,))

        for a in cursor:
            result.append(a)

        cursor.close()
        conn.close()
        return result

