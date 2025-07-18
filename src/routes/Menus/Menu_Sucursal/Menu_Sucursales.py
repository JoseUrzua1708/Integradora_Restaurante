class Menu_Sucursales:
    def mostrarMenu(self):
        print(" *** MENU DE SUCURSALES ***")
        print(" [1] Consultar Sucursales")
        print(" [2] Insertar Sucursal")
        print(" [3] Actualizar Sucursal")
        print(" [4] Eliminar Sucursal")
        print(" [5] Salir del Menú")
        print(" Pulse una opción")
        return
    
    def leeropcion(self):
        op = str(input())
        return op
    
    def mensaje(self, _msg):
        print(_msg)
        return