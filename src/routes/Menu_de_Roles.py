from Menus.Menu_Roles.Menu_Roles import Menu_Roles
from CRUD_Rol.consultar_rol import Consultar_Rol
from CRUD_Rol.insertar_rol import insertar_rol
from CRUD_Rol.actualizar_rol import actualizar_rol
from CRUD_Rol.eliminar_rol import eliminar_rol

menu = Menu_Roles()

while True:
    menu.mostrarMenu()
    opcion = menu.leeropcion()

    if opcion == "1":
        Consultar_Rol()
    elif opcion == "2":
        insertar_rol
    elif opcion == "3":
        actualizar_rol
    elif opcion == "4":
        eliminar_rol
    elif opcion == "5":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")