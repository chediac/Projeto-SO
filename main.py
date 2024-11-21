import pandas as pd
import time

def execute_simulation(path_to_csv):
    try:
        execution_data = pd.read_csv(path_to_csv, sep=",", header=None, names=["ID", "Page", "Address"])
        print("Arquivo carregado.")
        print("Pré-visualização dos dados:")
        print(execution_data.head())

        physical_memory = {}
        frame_limit = 4
        fault_count = 0
        execution_log = []

        print("\nInício da execução...\n")

        for idx, record in execution_data.iterrows():
            pid = record['ID']
            page_num = record['Page']
            addr = record['Address']

            if (pid, page_num) in physical_memory:
                print(f"[TEMPO {idx}] Página {page_num} do Processo {pid} já está carregada.")
                execution_log.append(f"[TEMPO {idx}] Página {page_num} do Processo {pid} já está carregada.")
            else:
                print(f"[TEMPO {idx}] [FALHA] Página {page_num} do Processo {pid} não está carregada.")
                execution_log.append(f"[TEMPO {idx}] [FALHA] Página {page_num} do Processo {pid} não está carregada.")
                fault_count += 1

                if len(physical_memory) < frame_limit:
                    physical_memory[(pid, page_num)] = addr
                else:
                    evict_page = list(physical_memory.keys())[0]
                    print(f"[TEMPO {idx}] Substituindo Página {evict_page[1]} do Processo {evict_page[0]}.")
                    execution_log.append(f"[TEMPO {idx}] Substituindo Página {evict_page[1]} do Processo {evict_page[0]}.")
                    del physical_memory[evict_page]
                    physical_memory[(pid, page_num)] = addr

            print(f"Estado atual: {physical_memory}")
            execution_log.append(f"Estado atual: {physical_memory}")

            time.sleep(0.5)

        print("\nExecução finalizada.")
        execution_log.append("\nExecução finalizada.")
        execution_log.append(f"Total de falhas de página: {fault_count}")
        print(f"Total de falhas de página: {fault_count}")

        with open("execution_logs.txt", "w") as log_file:
            for line in execution_log:
                log_file.write(line + "\n")
        print("Logs salvos em 'execuções.txt'.")

    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except ValueError as error:
        print(f"Erro no arquivo: {error}")
    except Exception as ex:
        print(f"Erro durante a execução: {ex}")

csv_path = "arquivoso.csv"
execute_simulation(csv_path)
