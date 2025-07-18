# Updated imports for Menu_de_sucursales
from Menus.Menu_Sucursal.Menu_Sucursales import Menu_Sucursales
from CRUD_Sucursales.consultar__sucursales import Consultar_Sucursal
from CRUD_Sucursales.insertar_sucursales import Agregar_Sucursal
from CRUD_Sucursales.actualizar_sucursales import Actualizar_Sucursal
from CRUD_Sucursales.eliminar_sucursales import Eliminar_Sucursal

menu = Menu_Sucursales()

while True:
    menu.mostrarMenu()
    opcion = menu.leeropcion()

    if opcion == "1":
        Consultar_Sucursal()
    elif opcion == "2":
        Agregar_Sucursal()
    elif opcion == "3":
        Actualizar_Sucursal()
    elif opcion == "4":
        Eliminar_Sucursal()
    elif opcion == "5":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")