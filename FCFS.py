from Strategy import Strategy

class FCFS(Strategy):
    def ejecutar(self,TCP,TFP ,tiempo,cola_de_terminados ,cola_de_Bloqueados, cola_de_listos, proceso_cargado):
        if cola_de_listos:
            proceso_cargado = cola_de_listos.pop(0)
            tiempo +=TCP
        while proceso_cargado.get_Tiempo_de_Rafaga_Restante() > 0:
            proceso_cargado.Consumir_Rafaga()
            tiempo += 1
        proceso_cargado.Reducir_Rafagas_restantes()
        if proceso_cargado.get_Rafagas_restantes() > 0:
            cola_de_Bloqueados.append(proceso_cargado)
        else:
            cola_de_terminados.append(proceso_cargado)
            