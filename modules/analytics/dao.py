from database.connect import ConnectDataBase
from modules.event.dao import EventDao
from flask import make_response
import json
import pandas as pd
from collections import defaultdict
import re

dao_event = EventDao()

class AnalyticsDao:
  
    _COUNT_ANSWERED_EVENTS = "SELECT COUNT(*) AS total_answered_events FROM event WHERE verb_id = 'http://libramigo.com/expapi/verbs/answered'"
    _COUNT_ACTORS = "SELECT COUNT(*) FROM actor"
    
    _SELECT_RESULTS_BY_ACTOR = """
        SELECT
        e.actor_username,
        a.name AS actor_name,
        r.id AS result_id,
        r.success
        FROM
        event e
        JOIN
        actor a ON e.actor_username = a.username
        JOIN
        result r ON e.result_id = r.id;
    """

    def __init__(self):
      self.database = ConnectDataBase().get_instance()
       
    def get_average_time_by_object(self):
        with open("base_ficticia.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        # Garante que os dados sejam uma lista de eventos
        if not isinstance(data, list):
            data = [data]

        total_time = 0
        answered_count = 0

        for event in data:
            verb = event.get("verb", {}).get("display_en", "")
            if verb == "answered":
                response_time = event.get("result", {}).get("response_time_seconds", 0)
                total_time += response_time
                answered_count += 1

        if answered_count == 0:
            return 0  # Evita divisão por zero

        average_time = total_time / answered_count
        return {"average_time": average_time}

        
        
     
    def get_overall_hit_and_miss_by_object_level(self):
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        result_dict = {
            "levelOne": [],
            "levelTwo": [],
            "levelThree": []
        }

        temp_data = defaultdict(lambda: {"hits": 0, "misses": 0})

        # Função auxiliar para extrair nível e nome do desafio
        def extract_level_and_challenge(url):
            match = re.search(r"nivel(\d+)/desafio(\d+)", url)
            if match:
                level = int(match.group(1))
                challenge = int(match.group(2))
                return level, f"Desafio {challenge}"
            return None, None

        # Processa os dados
        for item in data:
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

        # Monta a estrutura final
        for (key, challenge), values in temp_data.items():
            result_dict[key].append({
                "object": challenge,
                "hits": values["hits"],
                "misses": values["misses"]
            })

        # Ordena os desafios numericamente
        for level_key in result_dict:
            result_dict[level_key].sort(key=lambda x: int(x["object"].split()[-1]))

        return result_dict
    
    def get_overall_hit_and_miss_by_subject(self):
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Extrair os dados relevantes
        filtered = [
            {
                "subject": item["subject"]["name_pt"],
                "success": item["result"]["success"]
            }
            for item in data
            if item["verb"]["id"] == "http://libramigo.com/expapi/verbs/answered"
        ]

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

        # Preparar formato final
        result = []
        for _, row in summary.iterrows():
            result.append({
                "subject": row["subject"],
                "correct_percentage": round(row[True] * 100),
                "incorrect_percentage": round(row[False] * 100),
            })

        # Exibir resultado
        return result


    def get_ranking(self): 
            results = []
            cursor = self.database.cursor()
            cursor.execute(self._SELECT_RESULTS_BY_ACTOR)
            all_results = cursor.fetchall()
            coluns_name = [desc[0] for desc in cursor.description]
            
            for result_query in all_results:
                data = dict(zip(coluns_name, result_query))
                results.append(data)
            
            cursor.close()

            # Converter a lista de resultados em DataFrame
            df = pd.DataFrame(results)

            # Calcular o percentual de acertos por ator
            df_percent = (
                df.groupby("actor_name")
                .agg(total=("success", "count"), acertos=("success", "sum"))
                .reset_index()
            )
            df_percent["value"] = round((df_percent["acertos"] / df_percent["total"]) * 100).astype(int)
            df_percent = df_percent.rename(columns={"actor_name": "label"})

            # Selecionar colunas e ordenar
            ranking_json = (
                df_percent[["label", "value"]]
                .sort_values(by="value", ascending=False)
                .to_dict(orient="records")
            )

            return ranking_json
    
    def get_overall_hit_and_miss_rate(self): 
      import json

      with open("base_ficticia.json", "r", encoding="utf-8") as file:
          data = json.load(file)

      # Initialize counters
      total = 0
      correct = 0
      incorrect = 0

      # Iterate through the records
      for item in data:
          verb = item.get("verb", {})
          verb_id = verb.get("id", "")
          
          # Check if verb ID ends with "/answered"
          if verb_id.endswith("/answered"):
              result = item.get("result", {})
              if "success" in result:
                  total += 1
                  if result["success"]:
                      correct += 1
                  else:
                      incorrect += 1

      # Calculate percentages and return as JSON
      if total > 0:
          correct_percentage = round((correct / total) * 100)
          incorrect_percentage = round((incorrect / total) * 100)
          output = {
              "correct_percentage": correct_percentage,
              "incorrect_percentage": incorrect_percentage
          }
      else:
          output = {
              "correct_percentage": 0,
              "incorrect_percentage": 0
          }

      return output

      # return {"correct_percentage": 70, "incorrect_percentage": 30}
  
    def get_indicators(self):
      indicators = []
      
      higher_error_rate = self.get_higher_error_rate()
      indicators.append(higher_error_rate)
      
      count_answered_events = self.get_count_answered_events()
      indicators.append(count_answered_events)

      count_actors = self.get_count_actors()
      indicators.append(count_actors)
      
      return make_response(indicators)
    
    def get_count_actors(self):
        cursor = self.database.cursor()
        cursor.execute(self._COUNT_ACTORS)
        row = cursor.fetchone()
        cursor.close()
        
        total = row[0] if row else 0
        return {
            "title": "Alunos cadastrados",
            "value": total
        }

      
    
    def get_count_answered_events(self):
        cursor = self.database.cursor()
        cursor.execute(self._COUNT_ANSWERED_EVENTS)
        row = cursor.fetchone()
        cursor.close()
        
        total = row[0] if row else 0
        return {
            "title": "Desafios respondidos",
            "value": total
        }

  
    def get_higher_error_rate(self):
        # Abre o arquivo JSON
        with open('base_ficticia.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)
    
        # Estrutura para armazenar estatísticas por objeto (desafio)
        desafio_stats = defaultdict(lambda: {'total': 0, 'erros': 0})

        # Processar cada entrada
        for entry in data:
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
                # Encontrar o primeiro registro com este ID para pegar o nome
                nome_desafio_pt = next(entry['object']['name_pt'] for entry in data if entry['object']['id'] == desafio_id)
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
              "value": f"Desafio {primeiro_lugar['desafio']} {primeiro_lugar['nivel']} - {primeiro_lugar['taxa_erro']:.1f}%"

            }
        else:
            response_data = {"maior_taxa_erros": "Nenhum dado disponível"}
        
        return response_data