from database.connect import ConnectDataBase
from modules.event.dao import EventDao
from modules.actor.dao import ActorDao
from flask import make_response
import json
import pandas as pd
from collections import defaultdict
import re

dao_event = EventDao()
dao_actor = ActorDao()

class IndividualAnalyticsDao:
  
    # _COUNT_ANSWERED_EVENTS = "SELECT COUNT(*) AS total_answered_events FROM event WHERE verb_id = 'http://libramigo.com/expapi/verbs/answered'"
    

    def __init__(self, username):
    #   self.database = ConnectDataBase().get_instance()
      self.username = username
    
    ## CRIAR ANALISE PARA ASSUNTO MAIOR DIFICULDADE E EVOLUÇÃO DE ACERTOS
    def get_individual_analysis(self):
        actor = dao_actor.get_by_username(self.username)
        actor_data = actor.get_data_dict()
        
        average_time = self.get_average_time_by_object()
        
        higher_error_rate = self.get_higher_error_rate()
        
        hit_miss_rate = self.get_hit_and_miss_rate()
        
        hit_and_miss_by_subject = self.get_hit_and_miss_by_subject()
        
        hit_and_miss_by_object_level = self.get_hit_and_miss_by_object_level()
        
        individual_evolution = self.get_individual_evolution()
        
        answered_events = self.get_count_answered_events()
        
        most_difficult_subject = self.get_most_difficult_subject()
        
        individual_analysis =  {
            "actor": actor_data,
            "individual_indicators": {
                "average_time": {"seconds": average_time},
                "desempenho": "Bom",
                "most_difficult_subject": most_difficult_subject,
                "maior_taxa_erros": higher_error_rate,
                "count_answered_events": answered_events 
            },
            "hit_miss_rate": hit_miss_rate,
            "hit_and_miss_by_subject": hit_and_miss_by_subject,
            "hit_and_miss_by_object_level": hit_and_miss_by_object_level,
            "individual_evolution": individual_evolution
        }
        

        return individual_analysis
    
    #USANDO
    def get_most_difficult_subject(self):
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)
                # Transforma a lista de eventos em um DataFrame
        df = pd.json_normalize(data)

        # Filtra os eventos com verb "answered" e do usuário desejado
        answered_df = df[
            (df["verb.display_en"] == "answered") &
            (df["actor_username.username"] == self.username)
        ]

        if answered_df.empty:
            return None  # Nenhum evento respondido encontrado para o usuário

        # Agrupa por subject e calcula a taxa de erro (1 - taxa de acerto)
        erro_por_subject = (
            answered_df.groupby("subject.name_pt")["result.success"]
            .apply(lambda x: 1 - x.mean())
            .sort_values(ascending=False)
        )

        # Retorna o nome do subject com maior taxa de erro
        return erro_por_subject.index[0] if not erro_por_subject.empty else None
    
    #USANDO - OK
    def get_individual_evolution(self):
        
        # Load the JSON file (adjust the filename if needed)
        with open("base_ficticia.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # If the JSON is a single entry instead of a list
        if isinstance(data, dict):
            data = [data]  # convert to list if it's a single dictionary

        # Convert to DataFrame
        df = pd.json_normalize(data)

        # Set the username to filter
        username = self.username

        # Filter only entries with verb "answered" and matching username
        filtered_df = df[
            (df["verb.display_en"] == "answered") &
            (df["actor_username.username"] == username)
        ]

        # Convert the date column to datetime and extract only the date
        filtered_df["date"] = pd.to_datetime(filtered_df["date_time"]).dt.date

        # Group by date and calculate the number of answers and correct answers
        result = (
            filtered_df
            .groupby("date")
            .agg(total_answers=("result.success", "count"),
                correct_answers=("result.success", "sum"))
            .reset_index()
        )

        # Calculate accuracy percentage per day
        result["accuracy"] = (result["correct_answers"] / result["total_answers"] * 100).round(0).astype(int)

        # Format the result for the line chart
        result["attempts"] = ["Dia " + str(i + 1) for i in range(len(result))]
        chart_data = result[["attempts", "accuracy"]].to_dict(orient="records")

        # Display the result
        return chart_data

    #USANDO - OK        
    def get_average_time_by_object(self):
        with open("base_ficticia.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        # Garante que os dados sejam uma lista de eventos
        if not isinstance(data, list):
            data = [data]

        total_time = 0
        answered_count = 0

        for event in data:
            # Verifica se o evento pertence ao usuário desejado
            username = event.get("actor_username", {}).get("username", "")
            if username != self.username:
                continue

            # Considera apenas eventos do tipo "answered"
            verb = event.get("verb", {}).get("display_en", "")
            if verb == "answered":
                response_time = event.get("result", {}).get("response_time_seconds", 0)
                total_time += response_time
                answered_count += 1

        if answered_count == 0:
            return 0  # Evita divisão por zero

        average_time = total_time / answered_count
        return round(average_time, 1)

    #USANDO - OK
    def get_hit_and_miss_by_object_level(self):
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        result_dict = {
            "levelOne": [],
            "levelTwo": [],
            "levelThree": []
        }

        temp_data = defaultdict(lambda: {"hits": 0, "misses": 0})

        def extract_level_and_challenge(url):
            match = re.search(r"nivel(\d+)/desafio(\d+)", url)
            if match:
                level = int(match.group(1))
                challenge = int(match.group(2))
                return level, f"Desafio {challenge}"
            return None, None

        for item in data:
            # Filtrar pelo username
            if item.get("actor_username", {}).get("username") != self.username:
                continue

            if item.get("verb", {}).get("id") != "http://libramigo.com/expapi/verbs/answered":
                continue

            object_url = item.get("object", {}).get("id", "")
            success = item.get("result", {}).get("success", False)
            level, challenge_name = extract_level_and_challenge(object_url)

            if level is None:
                continue

            key = f"level{level}"
            if key == "level1":
                key = "levelOne"
            elif key == "level2":
                key = "levelTwo"
            elif key == "level3":
                key = "levelThree"

            temp_data[(key, challenge_name)]["hits" if success else "misses"] += 1

        for (key, challenge), values in temp_data.items():
            result_dict[key].append({
                "object": challenge,
                "hits": values["hits"],
                "misses": values["misses"]
            })

        for level_key in result_dict:
            result_dict[level_key].sort(key=lambda x: int(x["object"].split()[-1]))

        return result_dict

        
    #USANDO - OK
    def get_hit_and_miss_by_subject(self):
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Filtrar apenas os registros do usuário e verb "answered"
        filtered = [
            {
                "subject": item["subject"]["name_pt"],
                "success": item["result"]["success"]
            }
            for item in data
            if item["verb"]["id"] == "http://libramigo.com/expapi/verbs/answered"
            and item["actor_username"]["username"] == self.username
        ]

        # Se não houver registros, retorna lista vazia
        if not filtered:
            return []

        # Converter para DataFrame
        df = pd.DataFrame(filtered)

        # Agrupar por subject e calcular % de acertos e erros
        summary = (
            df.groupby("subject")["success"]
            .value_counts(normalize=True)
            .unstack(fill_value=0)
            .reset_index()
        )

        # Garantir colunas para True/False
        summary[True] = summary.get(True, 0)
        summary[False] = summary.get(False, 0)

        # Preparar resultado final
        result = []
        for _, row in summary.iterrows():
            result.append({
                "subject": row["subject"],
                "correct_percentage": round(row[True] * 100),
                "incorrect_percentage": round(row[False] * 100),
            })

        return result



    #USANDO - OK
    def get_hit_and_miss_rate(self): 

        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Inicializa contadores
        total = 0
        correct = 0
        incorrect = 0

        for item in data:
            # Filtra pelo username
            username = item.get("actor_username", {}).get("username", "")
            if username != self.username:
                continue

            # Verifica se o verbo é "answered"
            verb_id = item.get("verb", {}).get("id", "")
            if verb_id.endswith("/answered"):
                result = item.get("result", {})
                if "success" in result:
                    total += 1
                    if result["success"]:
                        correct += 1
                    else:
                        incorrect += 1

        # Calcula os percentuais
        if total > 0:
            correct_percentage = round((correct / total) * 100)
            incorrect_percentage = round((incorrect / total) * 100)
        else:
            correct_percentage = 0
            incorrect_percentage = 0

        return {
            "correct_percentage": correct_percentage,
            "incorrect_percentage": incorrect_percentage
        }


      # return {"correct_percentage": 70, "incorrect_percentage": 30}
  
    #USANDO - OK
    def get_count_answered_events(self):
        import json

        with open('base_ficticia.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Garante que a base seja uma lista
        if isinstance(data, dict):
            data = [data]

        # Filtra eventos com verb "answered" e username correspondente
        count = sum(
            1 for item in data
            if item.get("verb", {}).get("display_en") == "answered"
            and item.get("actor_username", {}).get("username") == self.username
        )

        return {
            "title": "Desafios respondidos",
            "value": count
        }


    ## USANDO - OK
    def get_higher_error_rate(self):
        # Abre o arquivo JSON
        with open('base_ficticia.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)

        # Estrutura para armazenar estatísticas por objeto (desafio)
        desafio_stats = defaultdict(lambda: {'total': 0, 'erros': 0})

        # Processar cada entrada
        for entry in data:
            # Filtrar por usuário
            if entry['actor_username']['username'] != self.username:
                continue

            # Verificar se é uma ação de resposta (answered ou completed)
            if entry['verb']['display_pt'] in ['respondeu', 'concluiu']:
                desafio_id = entry['object']['id']
                desafio_stats[desafio_id]['total'] += 1
                if not entry['result']['success']:
                    desafio_stats[desafio_id]['erros'] += 1

        # Calcular taxa de erro para cada desafio
        taxas_erro = []
        for desafio_id, stats in desafio_stats.items():
            if stats['total'] > 0:
                taxa = (stats['erros'] / stats['total']) * 100
                # Extrair nível e nome do desafio do ID
                nivel = desafio_id.split('/')[-2]  # Ex: 'nivel1'
                # Encontrar o primeiro registro com este ID e com o mesmo usuário
                nome_desafio_pt = next(
                    entry['object']['name_pt'] for entry in data
                    if entry['object']['id'] == desafio_id and entry['actor_username']['username'] == self.username
                )
                taxas_erro.append({
                    'nivel': nivel,
                    'desafio': nome_desafio_pt,
                    'desafio_id': desafio_id,
                    'taxa_erro': taxa,
                    'total_tentativas': stats['total'],
                    'total_erros': stats['erros']
                })

        # Ordenar por taxa de erro (maior primeiro)
        taxas_erro.sort(key=lambda x: x['taxa_erro'], reverse=True)

        # Preparar resposta com apenas o primeiro lugar
        if taxas_erro:
            primeiro_lugar = taxas_erro[0]
            response_data = {
                "title": "Maior taxa de erros",
                "value": f"Desafio {primeiro_lugar['desafio']} {primeiro_lugar['nivel']} - {primeiro_lugar['taxa_erro']:.2f}%"
            }
        else:
            response_data = {"title": "Maior taxa de erros", "value": "Nenhum dado disponível"}

        return response_data