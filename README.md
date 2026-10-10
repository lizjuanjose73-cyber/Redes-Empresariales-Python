Redes-Empresariales-Python
Aplicación en Python para validar y registrar redes IPv4 empresariales, con su gateway y su VLAN.

¿Qué hace?
Valida que el ID de VLAN esté entre 1 y 4094.
Valida que el CIDR sea una red IPv4 correcta (rechaza direcciones con bits de host, como 10.10.0.5/24).
Valida que el gateway pertenezca a la red y no sea la dirección de red ni la de broadcast.
Rechaza registrar dos redes con la misma VLAN o con el mismo CIDR.
Estado actual
Primera versión, con dos clases:

RedEmpresarial: representa una red y valida sus datos al crearse.
RegistroRedes: guarda las redes y evita duplicados.
Las pruebas son manuales, dentro del bloque .__main__

Limitaciones conocidas
Solo soporta IPv4.
Detecta redes idénticas, pero no redes que se solapan (por ejemplo, /24 y /25).
Aún no hay pruebas automáticas.
Requisitos y ejecución
Python 3.9 o superior, sin dependencias externas.

Python NOMBRE_DE_TU_ARCHIVO.py

Bitácora
Proyecto documentado día a día en LinkedIn.
