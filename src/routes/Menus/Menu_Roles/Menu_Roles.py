class Menu_Roles:
    def mostrarMenu(self):
        print(" *** MENU DE ROLES ***")
        print(" [1] Consultar Roles")
        print(" [2] Agregar nuevo Rol")
        print(" [3] Actualizar Rol")
        print(" [4] Eliminar Rol")
        print(" [5] Salir del Menú")
        print(" Pulse una opción")
        return
    
    def leeropcion(self):
        op = str(input())
        return op
    
    def mensaje(self, _msg):
        print(_msg)
        return